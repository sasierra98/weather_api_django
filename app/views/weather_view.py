from datetime import datetime
from typing import Any, Dict
import pytz
import traceback
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine.errors import DoesNotExist

from app.constants import (
    OPEN_WEATHER_MAP_API,
    OPEN_WEATHER_MAP_API_KEY,
    OPEN_WEATHER_MAP_ONE_CALL_KEY,
)
from app.models import Weather
from app.models.enums import TemperatureUnit
from app.serializers.weather_serializer import (
    WeatherResponseSerializer,
    WeatherSerializer,
)


class WeatherAPIView(APIView):
    @method_decorator(cache_page(60 * 2))  # 2 minutes
    def get(self, request):
        """
        Handles GET requests to fetch weather data for a specified city and country.
        Args:
            request (Request): The HTTP request object containing query parameters.
        Returns:
            Response: A DRF Response object containing weather data or error messages.
        Query Parameters:
            city (str): The name of the city for which to fetch weather data.
            country (str): The 2-character country code for the specified city.
        Responses:
            200 OK: Returns weather data for the specified city and country.
            400 Bad Request: If city or country parameters are missing, or if the country code is not a 2-character string.
            500 Internal Server Error: If there is an error fetching weather data from the external API.
        """

        city = request.query_params.get("city", "")
        country = request.query_params.get("country", "")
        unit = request.query_params.get("unit", TemperatureUnit.CELSIUS.value)

        weather_api_key = request.headers.get("X-Open-Weather-Key")
        forecast_api_key = request.headers.get("X-Open-Weather-Call-Key")

        try:
            if not self._validate_params(city, country):
                return Response(
                    {"message": "City and country parameters are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            weather_data = self._fetch_weather_data(city, country, weather_api_key)
            weather_forecast_data = self._fetch_weather_forecast(
                weather_data, forecast_api_key
            )
            weather_response = self._format_weather_response(
                weather_data, weather_forecast_data
            )

            try:
                weather: Weather = Weather.objects.get(id=weather_response["id"])

                serializer = WeatherSerializer(data=weather_response)
                if serializer.is_valid():
                    weather.update(
                        **serializer.validated_data,
                        updated_at=datetime.now(tz=pytz.utc),
                    )
                    weather = weather.reload()
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            except DoesNotExist:
                serializer = WeatherSerializer(data=weather_response)
                if serializer.is_valid():
                    weather = Weather.objects.create(**serializer.validated_data)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            weather_dict = weather.to_mongo()
            weather_dict["id"] = weather_dict["_id"]
            response_serializer = WeatherResponseSerializer(
                data=weather_dict, context={"unit": unit}
            )

            if not response_serializer.is_valid():
                return Response(
                    response_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"data": response_serializer.data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _validate_params(self, city: str, country: str) -> bool:
        """
        Validates the provided city and country parameters.
        Args:
            city (str): The name of the city.
            country (str): The country code, expected to be a 2-character string.
        Returns:
            bool: True if both parameters are valid, False otherwise.
        """

        if not city or not country:
            return False
        if len(country) != 2:
            return False
        return True

    def _fetch_weather_data(
        self, city: str, country: str, weather_api_key: str
    ) -> Dict[str, Any]:
        """
        Fetches weather data for a given city and country using the OpenWeatherMap API.
        Args:
            city (str): The name of the city to fetch weather data for.
            country (str): The country code of the city.
            weather_api_key (str): The API key to use for the request. If not provided, a default key will be used.
        Returns:
            Dict[str, Any]: The weather data in JSON format if the request is successful.
            Response: An error response with a message if the request fails.
        """

        api_key = OPEN_WEATHER_MAP_API_KEY if not weather_api_key else weather_api_key
        weather_request = requests.get(
            f"{OPEN_WEATHER_MAP_API}/data/2.5/weather?q={city},{country}&appid={api_key}"
        )

        if weather_request.status_code != 200:
            return Response(
                {"message": "Failed to fetch weather data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return weather_request.json()

    def _fetch_weather_forecast(
        self, weather_response: Dict[str, Any], forecast_api_key: str
    ) -> Dict[str, Any]:
        """
        Fetches the weather forecast for a given location using the OpenWeatherMap One Call API.
        Args:
            weather_response (Dict[str, Any]): The response from the initial weather API call containing location data.
            forecast_api_key (str): The API key to use for the forecast request. If not provided, a default key will be used.
        Returns:
            Dict[str, Any]: The JSON response from the One Call API containing the weather forecast data.
        Raises:
            Response: If the API request fails, a response with an error message and HTTP 500 status is returned.
        """

        city_lat = weather_response["coord"]["lat"]
        city_lon = weather_response["coord"]["lon"]
        api_key = (
            OPEN_WEATHER_MAP_ONE_CALL_KEY if not forecast_api_key else forecast_api_key
        )

        weather_one_call_request = requests.get(
            f"{OPEN_WEATHER_MAP_API}/data/2.5/onecall?lat={city_lat}&lon={city_lon}&appid={api_key}"
        )

        if weather_one_call_request.status_code != 200:
            return Response(
                {"message": "Failed to fetch weather data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return weather_one_call_request.json()

    def _format_weather_response(
        self, weather_data: Dict[str, Any], weather_forecast_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Formats the weather response by combining current weather data with forecast data.
        Args:
            weather_data (Dict[str, Any]): The current weather data.
            weather_forecast_response (Dict[str, Any]): The weather forecast data.
        Returns:
            Dict[str, Any]: The combined weather data with forecast information.
        """

        daily_forecast_list = []
        for daily_forecast in weather_forecast_response["daily"]:
            daily_forecast["timezone"] = weather_data["timezone"]
            daily_forecast_list.append(daily_forecast)
        weather_data["forecast"] = daily_forecast_list
        return weather_data
