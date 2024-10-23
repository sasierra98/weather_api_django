from app.models.enums import TemperatureUnit


def parse_temperature(kelvin: float, unit: str) -> str:
    """
    Convert a temperature from Kelvin to Celsius.
    Args:
        kelvin (float): Temperature in Kelvin.
    Returns:
        str: Temperature in Celsius, formatted as a string with the degree symbol and "C".
    """
    if unit == TemperatureUnit.CELSIUS.value:
        return str(round(kelvin - 273.15)) + "°C"
    elif unit == TemperatureUnit.FAHRENHEIT.value:
        return str(round((kelvin - 273.15) * 9 / 5 + 32)) + "°F"
    else:
        return str(kelvin) + "°K"


def format_celsius_temperature(temperature: float) -> str:
    """
    Formats a given temperature in Celsius to a string with a degree symbol.
    Args:
        temperature (float): The temperature in Celsius to be formatted.
    Returns:
        str: The formatted temperature string with a degree symbol, rounded to the nearest integer.
    """

    return str(round(temperature)) + "°C"
