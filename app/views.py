from datetime import datetime
import pytz
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.constants import OPEN_WEATHER_MAP_API, OPEN_WEATHER_MAP_API_KEY
from app.models import Weather
from app.serializers.WeatherSerializer import (
    WeatherResponseSerializer,
    WeatherSerializer,
)


class WeatherAPIView(APIView):
    @method_decorator(cache_page(1))
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

        if not city or not country:
            return Response(
                {"message": "City and country parameters are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(country) != 2:
            return Response(
                {"message": "Country code must be a 2-character string"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        weather_request = requests.get(
            f"{OPEN_WEATHER_MAP_API}/data/2.5/weather?q={city},{country}&appid={OPEN_WEATHER_MAP_API_KEY}"
        )

        if weather_request.status_code != 200:
            return Response(
                {"message": "Failed to fetch weather data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            weather_response = weather_request.json()
            weather: Weather = Weather.objects.get(id=weather_response["id"])

            serializer = WeatherSerializer(data=weather_response)
            if serializer.is_valid():
                weather.update(
                    **serializer.validated_data, updated_at=datetime.now(tz=pytz.utc)
                )
                weather = weather.reload()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Weather.DoesNotExist:
            serializer = WeatherSerializer(data=weather_response)
            if serializer.is_valid():
                weather = Weather.objects.create(**serializer.validated_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        weather_dict = weather.to_mongo()
        weather_dict["id"] = weather_dict["_id"]
        response_serializer = WeatherResponseSerializer(data=weather_dict)

        if not response_serializer.is_valid():
            return Response(
                response_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"data": response_serializer.data}, status=status.HTTP_200_OK)
