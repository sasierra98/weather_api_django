def parse_kelvin_to_celsius(kelvin: float) -> str:
    """
    Convert a temperature from Kelvin to Celsius.
    Args:
        kelvin (float): Temperature in Kelvin.
    Returns:
        str: Temperature in Celsius, formatted as a string with the degree symbol and "C".
    """

    return str(round(kelvin - 273.15)) + "°C"


def format_celsius_temperature(temperature: float) -> str:
    """
    Formats a given temperature in Celsius to a string with a degree symbol.
    Args:
        temperature (float): The temperature in Celsius to be formatted.
    Returns:
        str: The formatted temperature string with a degree symbol, rounded to the nearest integer.
    """

    return str(round(temperature)) + "°C"
