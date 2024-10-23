from enum import Enum


class BeaufortScale(Enum):
    CALM = (0.2, "Calm")
    LIGHT_AIR = (1.5, "Light air")
    LIGHT_BREEZE = (3.3, "Light breeze")
    GENTLE_BREEZE = (5.4, "Gentle breeze")
    MODERATE_BREEZE = (7.9, "Moderate breeze")
    FRESH_BREEZE = (10.7, "Fresh breeze")
    STRONG_BREEZE = (13.8, "Strong breeze")
    NEAR_GALE = (17.1, "Near gale")
    GALE = (20.7, "Gale")
    STRONG_GALE = (24.4, "Strong gale")
    STORM = (28.4, "Storm")
    VIOLENT_STORM = (32.6, "Violent storm")
    HURRICANE = (float("inf"), "Hurricane")

    @classmethod
    def get_description(cls, wind_speed: float) -> str:
        for scale in cls:
            if wind_speed <= scale.value[0]:
                return scale.value[1]
        return cls.HURRICANE.value[1]

    @property
    def scale(self) -> str:
        return self.value[0]

    @property
    def description(self) -> str:
        return self.value[1]


class WindDirection(Enum):
    NORTH = "North"
    NORTH_NORTHEAST = "North-Northeast"
    NORTHEAST = "Northeast"
    EAST_NORTHEAST = "East-Northeast"
    EAST = "East"
    EAST_SOUTHEAST = "East-Southeast"
    SOUTHEAST = "Southeast"
    SOUTH_SOUTHEAST = "South-Southeast"
    SOUTH = "South"
    SOUTH_SOUTHWEST = "South-Southwest"
    SOUTHWEST = "Southwest"
    WEST_SOUTHWEST = "West-Southwest"
    WEST = "West"
    WEST_NORTHWEST = "West-Northwest"
    NORTHWEST = "Northwest"
    NORTH_NORTHWEST = "North-Northwest"


class TemperatureUnit(Enum):
    CELSIUS = "metric"
    FAHRENHEIT = "imperial"
    KELVIN = "standard"
