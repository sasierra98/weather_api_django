from typing import Any, Dict
import pytz
from rest_framework import serializers

from datetime import datetime, timedelta


class CoordSerializer(serializers.Serializer):
    lon = serializers.FloatField()
    lat = serializers.FloatField()


class WeatherDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    main = serializers.CharField()
    description = serializers.CharField()
    icon = serializers.CharField()


class MainSerializer(serializers.Serializer):
    temp = serializers.FloatField()
    feels_like = serializers.FloatField()
    temp_min = serializers.FloatField()
    temp_max = serializers.FloatField()
    pressure = serializers.IntegerField()
    humidity = serializers.IntegerField()
    sea_level = serializers.IntegerField(required=False)
    grnd_level = serializers.IntegerField(required=False)


class WindSerializer(serializers.Serializer):
    speed = serializers.FloatField()
    deg = serializers.IntegerField()


class CloudsSerializer(serializers.Serializer):
    all = serializers.IntegerField()


class SysSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=False)
    id = serializers.IntegerField(required=False)
    country = serializers.CharField()
    sunrise = serializers.IntegerField()
    sunset = serializers.IntegerField()


class WeatherSerializer(serializers.Serializer):
    coord = CoordSerializer()
    weather = serializers.ListField(child=WeatherDetailSerializer())
    base = serializers.CharField()
    main = MainSerializer()
    visibility = serializers.IntegerField()
    wind = WindSerializer()
    clouds = CloudsSerializer()
    dt = serializers.IntegerField()
    sys = SysSerializer()
    timezone = serializers.IntegerField()
    id = serializers.IntegerField()
    name = serializers.CharField()
    cod = serializers.IntegerField()


class WeatherResponseSerializer(WeatherSerializer):
    def get_location_name(self, instance: Dict[str, Any]) -> str:
        """
        Retrieves the location name from the given instance.
        Args:
            instance (Dict[str, Any]): A dictionary containing weather data.
        Returns:
            str: The location name in the format "name, country".
        """

        return instance["name"] + ", " + instance["sys"]["country"]

    def get_temperature(self, instance: Dict[str, Any]) -> str:
        """
        Converts the temperature from Kelvin to Celsius and returns it as a string with a degree symbol.
        Args:
            instance (Dict[str, Any]): A dictionary containing weather data.
        Returns:
            str: The temperature in Celsius, rounded to the nearest whole number, followed by the degree symbol "°C".
        """

        return str(round(instance["main"]["temp"] - 273.15)) + "°C"

    def get_beaufort_scale(self, wind_speed: float) -> str:
        """
        Determine the Beaufort scale description based on the wind speed.
        Args:
            wind_speed (float): The speed of the wind in meters per second.
        Returns:
            str: The description of the wind speed according to the Beaufort scale.
        """

        scales = (
            (0.2, "Calm"),
            (1.5, "Light air"),
            (3.3, "Light breeze"),
            (5.4, "Gentle breeze"),
            (7.9, "Moderate breeze"),
            (10.7, "Fresh breeze"),
            (13.8, "Strong breeze"),
            (17.1, "Near gale"),
            (20.7, "Gale"),
            (24.4, "Strong gale"),
            (28.4, "Storm"),
            (32.6, "Violent storm"),
        )
        for limit, description in scales:
            if wind_speed <= limit:
                return description
        return "Hurricane"

    def get_wind_direction(self, wind_deg: float) -> str:
        """
        Converts a wind direction in degrees to a compass direction.
        Args:
            wind_deg (float): The wind direction in degrees.
        Returns:
            str: The compass direction corresponding to the given wind degree.
        """

        directions = [
            "North",
            "North-Northeast",
            "Northeast",
            "East-Northeast",
            "East",
            "East-Southeast",
            "Southeast",
            "South-Southeast",
            "South",
            "South-Southwest",
            "Southwest",
            "West-Southwest",
            "West",
            "West-Northwest",
            "Northwest",
            "North-Northwest",
        ]
        return directions[int(wind_deg / 22.5) % 16]

    def get_wind(self, instance: Dict[str, Any]) -> str:
        """
        Retrieves the wind information from the given instance.
        Args:
            instance (Dict[str, Any]): A dictionary containing wind data.
        Returns:
            str: A formatted string containing the wind type, wind speed, and wind direction.
        """

        wind_type = self.get_beaufort_scale(instance["wind"]["speed"])
        wind_speed = str(instance["wind"]["speed"]) + " m/s"
        wind_direction = self.get_wind_direction(instance["wind"]["deg"])
        return f"{wind_type}, {wind_speed}, {wind_direction}"

    def get_cloudiness(self, instance: Dict[str, Any]) -> str:
        """
        Retrieves the cloudiness description from the weather data.
        Args:
            instance (Dict[str, Any]): A dictionary containing weather data.
        Returns:
            str: The capitalized description of the cloudiness.
        """

        return instance["weather"][0]["description"].capitalize()

    def get_pressure(self, instance: Dict[str, Any]) -> str:
        """
        Retrieve the atmospheric pressure from the given instance.
        Args:
            instance (Dict[str, Any]): A dictionary containing weather data.
        Returns:
            str: The atmospheric pressure in hectopascals (hPa) as a string.
        """

        return str(instance["main"]["pressure"]) + " hPa"

    def get_humidity(self, instance: Dict[str, Any]) -> str:
        """
        Retrieve the humidity value from the given instance and format it as a percentage string.
        Args:
            instance (Dict[str, Any]): A dictionary containing weather data.
        Returns:
            str: The humidity value formatted as a percentage string.
        """

        return str(instance["main"]["humidity"]) + "%"

    def get_local_time(self, timestamp: int, timezone_offset: int) -> str:
        """
        Converts a given UTC timestamp to local time based on the provided timezone offset.
        Args:
            timestamp (int): The UTC timestamp to be converted.
            timezone_offset (int): The offset from UTC in seconds.
        Returns:
            str: The local time in the format "HH:MM AM/PM".
        """

        hours = timezone_offset / 3600
        local_time = datetime.fromtimestamp(timestamp, pytz.UTC) + timedelta(
            hours=hours
        )
        return local_time.strftime("%I:%M %p")

    def get_sunrise(self, instance: Dict[str, Any]) -> str:
        """
        Converts the sunrise time from UTC to local time based on the provided timezone.
        Args:
            instance (Dict[str, Any]): A dictionary containing weather data.
        Returns:
            str: The local time of sunrise as a string.
        """

        return self.get_local_time(instance["sys"]["sunrise"], instance["timezone"])

    def get_sunset(self, instance: Dict[str, Any]) -> str:
        """
        Retrieves the local sunset time from the given instance data.
        Args:
            instance (Dict[str, Any]): A dictionary containing weather data.
        Returns:
            str: The local sunset time as a string.
        """

        return self.get_local_time(instance["sys"]["sunset"], instance["timezone"])

    def geo_coordinates(self, instance: Dict[str, Any]) -> str:
        """
        Extracts the latitude and longitude from the given instance and returns them as a string.
        Args:
            instance (Dict[str, Any]): A dictionary containing weather data.
        Returns:
            str: A string representation of the latitude and longitude in the format '[lat, lon]'.
        """

        lat = instance["coord"]["lat"]
        lon = instance["coord"]["lon"]
        return str([lat, lon])

    @property
    def request_time(self) -> str:
        """
        Returns the current date and time in UTC timezone as a formatted string.
        The format of the returned string is "YYYY-MM-DD HH:MM:SS".
        Returns:
            str: The current date and time in UTC timezone.
        """

        return datetime.now(tz=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")

    def to_representation(self, instance):
        return {
            "location_name": self.get_location_name(instance),
            "temperature": self.get_temperature(instance),
            "wind": self.get_wind(instance),
            "cloudiness": self.get_cloudiness(instance),
            "pressure": self.get_pressure(instance),
            "humidity": self.get_humidity(instance),
            "sunrise": self.get_sunrise(instance),
            "sunset": self.get_sunset(instance),
            "geo_coordinates": self.geo_coordinates(instance),
            "requested_time": self.request_time,
        }
