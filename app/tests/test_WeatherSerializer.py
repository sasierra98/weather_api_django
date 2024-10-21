import pytest
import pytz
from app.serializers.WeatherSerializer import WeatherResponseSerializer
from datetime import datetime


@pytest.fixture
def instance():
    return {
        "coord": {"lon": 139, "lat": 35},
        "weather": [
            {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01n"}
        ],
        "base": "stations",
        "main": {
            "temp": 293.15,
            "feels_like": 293.15,
            "temp_min": 293.15,
            "temp_max": 293.15,
            "pressure": 1013,
            "humidity": 53,
            "sea_level": 1013,
            "grnd_level": 1009,
        },
        "visibility": 10000,
        "wind": {"speed": 1.5, "deg": 350},
        "clouds": {"all": 1},
        "dt": 1560350192,
        "sys": {
            "type": 1,
            "id": 8074,
            "country": "JP",
            "sunrise": 1560281377,
            "sunset": 1560333478,
        },
        "timezone": 32400,
        "id": 1851632,
        "name": "Shuzenji",
        "cod": 200,
    }


@pytest.fixture
def serializer():
    return WeatherResponseSerializer()


def test_get_location_name(serializer, instance):
    result = serializer.get_location_name(instance)
    assert result == "Shuzenji, JP"


def test_get_temperature(serializer, instance):
    result = serializer.get_temperature(instance)
    assert result == "20°C"


def test_get_beaufort_scale(serializer):
    result = serializer.get_beaufort_scale(1.5)
    assert result == "Light air"


def test_get_wind_direction(serializer):
    result = serializer.get_wind_direction(350)
    assert result == "North-Northwest"


def test_get_wind(serializer, instance):
    result = serializer.get_wind(instance)
    assert result == "Light air, 1.5 m/s, North-Northwest"


def test_get_cloudiness(serializer, instance):
    result = serializer.get_cloudiness(instance)
    assert result == "Clear sky"


def test_get_pressure(serializer, instance):
    result = serializer.get_pressure(instance)
    assert result == "1013 hPa"


def test_get_humidity(serializer, instance):
    result = serializer.get_humidity(instance)
    assert result == "53%"


def test_get_local_time(serializer):
    timestamp = 1560350192
    timezone_offset = 32400
    result = serializer.get_local_time(timestamp, timezone_offset)
    assert result == "11:36 PM"


def test_get_sunrise(serializer, instance):
    result = serializer.get_sunrise(instance)
    assert result == "04:29 AM"


def test_get_sunset(serializer, instance):
    result = serializer.get_sunset(instance)
    assert result == "06:57 PM"


def test_geo_coordinates(serializer, instance):
    result = serializer.geo_coordinates(instance)
    assert result == "[35, 139]"


@pytest.mark.parametrize("mock_datetime", [(datetime.now(pytz.utc))])
def test_request_time(mocker, serializer, mock_datetime):
    mocker.patch("app.serializers.WeatherSerializer.WeatherResponseSerializer")
    WeatherResponseSerializer.request_time = mock_datetime.strftime("%Y-%m-%d %H:%M:%S")
    result = serializer.request_time
    assert result == mock_datetime.strftime("%Y-%m-%d %H:%M:%S")


def test_to_representation(serializer, instance):
    result = serializer.to_representation(instance)
    print(result)
    expected = {
        "location_name": "Shuzenji, JP",
        "temperature": "20°C",
        "wind": "Light air, 1.5 m/s, North-Northwest",
        "cloudiness": "Clear sky",
        "pressure": "1013 hPa",
        "humidity": "53%",
        "sunrise": "04:29 AM",
        "sunset": "06:57 PM",
        "geo_coordinates": "[35, 139]",
        "requested_time": serializer.request_time,
    }
    assert result == expected
