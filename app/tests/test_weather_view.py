import pytest
from mongoengine import connect, disconnect
import mongomock
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from app.models.weather import Weather
from app.serializers.weather_serializer import (
    WeatherSerializer,
    WeatherResponseSerializer,
)


@pytest.fixture(scope="module", autouse=True)
def mongoengine_connection():
    disconnect()
    connect(
        "mongoenginetest",
        host="mongodb://localhost",
        mongo_client_class=mongomock.MongoClient,
        uuidRepresentation="standard",
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def weather_data():
    return {
        "coord": {"lon": -74.0817, "lat": 4.6097},
        "weather": [
            {"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04n"}
        ],
        "base": "stations",
        "main": {
            "temp": 286.88,
            "feels_like": 286.76,
            "temp_min": 286.88,
            "temp_max": 286.88,
            "pressure": 1017,
            "humidity": 94,
            "sea_level": 1017,
            "grnd_level": 738,
        },
        "visibility": 10000,
        "wind": {"speed": 1.54, "deg": 0},
        "clouds": {"all": 75},
        "dt": 1729570140,
        "sys": {
            "type": 1,
            "id": 8582,
            "country": "CO",
            "sunrise": 1729507253,
            "sunset": 1729550432,
        },
        "timezone": -18000,
        "id": 3688689,
        "name": "Bogota",
        "cod": 200,
    }


@pytest.fixture
def weather_instance(weather_data):
    weather = Weather(**weather_data)
    weather.save()
    return weather


@pytest.fixture
def weather_response():
    return {
        "data": {
            "location_name": "Bogota, CO",
            "temperature": "14°C",
            "wind": "Light breeze, 1.54 m/s, North",
            "cloudiness": "Broken clouds",
            "pressure": "1017 hPa",
            "humidity": "94%",
            "sunrise": "05:40 AM",
            "sunset": "05:40 PM",
            "geo_coordinates": "[4.6097, -74.0817]",
            "requested_time": "2024-10-22 04:27:16",
        }
    }


def test_get_weather_success(mocker, api_client, weather_data, weather_instance):
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = weather_data

    url = reverse("weather")
    response = api_client.get(url, {"city": "Test City", "country": "TC"})

    assert response.status_code == status.HTTP_200_OK
    assert "data" in response.data


def test_get_weather_missing_params(mocker, api_client):
    url = reverse("weather")
    response = api_client.get(url, {"city": "Test City"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["message"] == "City and country parameters are required"


def test_get_weather_invalid_country_code(mocker, api_client):
    url = reverse("weather")
    response = api_client.get(url, {"city": "Test City", "country": "TCC"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["message"] == "Country code must be a 2-character string"


def test_get_weather_api_country_failure(mocker, api_client):
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 500

    url = reverse("weather")
    response = api_client.get(url, {"city": "Test City", "country": "TCA"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_weather_create_new_weather(
    mocker, api_client, weather_data, weather_response
):
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = weather_data

    url = reverse("weather")
    response = api_client.get(url, {"city": "Bogota", "country": "CO"})

    weather_serializer = WeatherSerializer(data=weather_data)
    assert weather_serializer.is_valid()

    weather_response_serializer = WeatherResponseSerializer(
        data=weather_serializer.data
    )
    assert weather_response_serializer.is_valid()

    assert response.status_code == status.HTTP_200_OK
    assert "data" in response.data

    weather_response_data = weather_response_serializer.data.copy()
    weather_response_data.pop("requested_time", None)

    expected_response_data = weather_response["data"].copy()
    expected_response_data.pop("requested_time", None)

    assert weather_response_data == expected_response_data


def test_get_weather_update_existing_weather(
    mocker, api_client, weather_data, weather_instance, weather_response
):
    weather_data["id"] = weather_instance.id
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = weather_data

    url = reverse("weather")
    response = api_client.get(url, {"city": "Bogota", "country": "co"})

    weather_serializer = WeatherSerializer(data=weather_data)
    assert weather_serializer.is_valid()

    weather_response_serializer = WeatherResponseSerializer(
        data=weather_serializer.data
    )
    assert weather_response_serializer.is_valid()

    assert response.status_code == status.HTTP_200_OK
    assert "data" in response.data

    weather_response_data = weather_response_serializer.data.copy()
    weather_response_data.pop("requested_time", None)

    expected_response_data = weather_response["data"].copy()
    expected_response_data.pop("requested_time", None)
