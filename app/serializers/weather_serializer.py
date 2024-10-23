from typing import Any, Dict
import pytz
from rest_framework import serializers

from datetime import datetime, timedelta

from app.models.enums import BeaufortScale, TemperatureUnit, WindDirection
from app.utils.formatters import parse_temperature


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
    forecast = serializers.ListField(child=serializers.DictField(), required=False)


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

    def get_temperature(self, instance: Dict[str, Any], forecast: bool = False) -> str:
        """
        Retrieves the temperature from the given instance.
        Args:
            instance (Dict[str, Any]): The data instance containing temperature information.
            forecast (bool, optional): Flag indicating if the temperature data is for a forecast. Defaults to False.
        Returns:
            str: The temperature in Celsius. If forecast is True, returns a dictionary with temperatures for different times of the day.
        """

        unit = self.context.get("unit", TemperatureUnit.CELSIUS.value)
        if forecast:
            return {
                "day": parse_temperature(instance["temp"]["day"], unit),
                "min": parse_temperature(instance["temp"]["min"], unit),
                "max": parse_temperature(instance["temp"]["max"], unit),
                "night": parse_temperature(instance["temp"]["night"], unit),
                "eve": parse_temperature(instance["temp"]["eve"], unit),
                "morn": parse_temperature(instance["temp"]["morn"], unit),
            }
        return parse_temperature(instance["main"]["temp"], unit)

    def get_beaufort_scale(self, wind_speed: float) -> str:
        """
        Determine the Beaufort scale description based on the wind speed.
        Args:
            wind_speed (float): The speed of the wind in meters per second.
        Returns:
            str: The description of the wind speed according to the Beaufort scale.
        """

        return BeaufortScale.get_description(wind_speed)

    def get_wind_direction(self, wind_deg: float) -> str:
        """
        Converts a wind direction in degrees to a compass direction.
        Args:
            wind_deg (float): The wind direction in degrees.
        Returns:
            str: The compass direction corresponding to the given wind degree.
        """

        directions = [direction.value for direction in WindDirection]
        return directions[int(wind_deg / 22.5) % 16]

    def get_wind(self, instance: Dict[str, Any], forecast: bool = False) -> str:
        """
        Retrieves the wind information from the given instance and formats it as a string.
        Args:
            instance (Dict[str, Any]): The data instance containing wind information.
            forecast (bool, optional): Flag indicating whether the instance is a forecast. Defaults to False.
        Returns:
            str: A formatted string containing the wind type, speed, and direction.
        """

        if forecast:
            wind_type = self.get_beaufort_scale(instance["wind_speed"])
            wind_speed = str(instance["wind_speed"]) + " m/s"
            wind_direction = self.get_wind_direction(instance["wind_deg"])
        else:
            wind_type = self.get_beaufort_scale(instance["wind"]["speed"])
            wind_speed = str(instance["wind"]["speed"]) + " m/s"
            wind_direction = self.get_wind_direction(instance["wind"]["deg"])
        return f"{wind_type}, {wind_speed}, {wind_direction}"

    def get_cloudiness(self, instance: Dict[str, Any], forecast: bool = False) -> str:
        """
        Retrieves the cloudiness description from the weather instance.
        Args:
            instance (Dict[str, Any]): The weather data instance containing weather details.
            forecast (bool, optional): Flag indicating if the data is a forecast. Defaults to False.
        Returns:
            str: The capitalized description of the cloudiness.
        """

        return instance["weather"][0]["description"].capitalize()

    def get_pressure(self, instance: Dict[str, Any], forecast: bool = False) -> str:
        """
        Retrieve the pressure from the given instance.
        Args:
            instance (Dict[str, Any]): The data instance containing pressure information.
            forecast (bool, optional): Flag indicating whether the instance is a forecast. Defaults to False.
        Returns:
            str: The pressure value as a string with " hPa" appended.
        """

        if forecast:
            return str(instance["pressure"]) + " hPa"
        return str(instance["main"]["pressure"]) + " hPa"

    def get_humidity(self, instance: Dict[str, Any], forecast: bool = False) -> str:
        """
        Retrieve the humidity from the given instance.
        Args:
            instance (Dict[str, Any]): The data instance containing humidity information.
            forecast (bool, optional): Flag indicating whether the instance is a forecast. Defaults to False.
        Returns:
            str: The humidity value as a percentage string.
        """

        if forecast:
            return str(instance["humidity"]) + "%"
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

    def get_sunrise(self, instance: Dict[str, Any], forecast: bool = False) -> str:
        """
        Retrieves the local sunrise time from the given instance.
        Args:
            instance (Dict[str, Any]): The data instance containing sunrise and timezone information.
            forecast (bool, optional): Flag indicating whether the instance is a forecast. Defaults to False.
        Returns:
            str: The local sunrise time as a string.
        """

        if forecast:
            return self.get_local_time(instance["sunrise"], instance["timezone"])
        return self.get_local_time(instance["sys"]["sunrise"], instance["timezone"])

    def get_sunset(self, instance: Dict[str, Any], forecast: bool = False) -> str:
        """
        Retrieves the sunset time from the given instance.
        Args:
            instance (Dict[str, Any]): A dictionary containing weather data.
            forecast (bool, optional): A flag indicating whether the data is a forecast. Defaults to False.
        Returns:
            str: The local time of the sunset.
        """

        if forecast:
            return self.get_local_time(instance["sunset"], instance["timezone"])
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
            "forecast": [
                {
                    "temperature": self.get_temperature(forecast_instance, True),
                    "wind": self.get_wind(forecast_instance, True),
                    "cloudiness": self.get_cloudiness(forecast_instance, True),
                    "pressure": self.get_pressure(forecast_instance, True),
                    "humidity": self.get_humidity(forecast_instance, True),
                    "sunrise": self.get_sunrise(forecast_instance, True),
                    "sunset": self.get_sunset(forecast_instance, True),
                }
                for forecast_instance in instance["forecast"]
            ],
        }
