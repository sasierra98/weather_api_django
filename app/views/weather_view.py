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

from app.constants import OPEN_WEATHER_MAP_API, OPEN_WEATHER_MAP_API_KEY
from app.models.weather import Weather
from app.serializers.weather_serializer import (
    WeatherResponseSerializer,
    WeatherSerializer,
)


class WeatherAPIView(APIView):
    @method_decorator(cache_page(60 * 2))
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
        try:
            if not self._validate_params(city, country):
                return Response(
                    {"message": "City and country parameters are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            weather_data = self._fetch_weather_data(city, country)
            weather_forecast_data = self._fetch_weather_forecast(weather_data)
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
            response_serializer = WeatherResponseSerializer(data=weather_dict)

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

    def _fetch_weather_data(self, city: str, country: str) -> Dict[str, Any]:
        """
        Fetches weather data for a specified city and country from the OpenWeatherMap API.
        Args:
            city (str): The name of the city for which to fetch weather data.
            country (str): The country code of the city.
        Returns:
            Dict[str, Any]: A dictionary containing the weather data if the request is successful.
            Response: A DRF Response object with an error message if the request fails.
        """

        weather_request = requests.get(
            f"{OPEN_WEATHER_MAP_API}/data/2.5/weather?q={city},{country}&appid={OPEN_WEATHER_MAP_API_KEY}"
        )

        if weather_request.status_code != 200:
            return Response(
                {"message": "Failed to fetch weather data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return weather_request.json()

    def _fetch_weather_forecast(
        self, weather_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fetches the weather forecast for a given location using the OpenWeatherMap API.
        Args:
            weather_response (Dict[str, Any]): A dictionary containing weather data,
                                               including coordinates of the city.
        Returns:
            Dict[str, Any]: A dictionary containing the weather forecast data if the request is successful.
                            If the request fails, returns a Response object with an error message and
                            HTTP 500 status code.
        """

        city_lat = weather_response["coord"]["lat"]
        city_lon = weather_response["coord"]["lon"]

        weather_one_call_request = requests.get(
            f"{OPEN_WEATHER_MAP_API}/data/2.5/onecall?lat={city_lat}&lon={city_lon}&appid=5796abbde9106b7da4febfae8c44c232"
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
