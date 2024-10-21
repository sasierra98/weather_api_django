import os
from dotenv import load_dotenv


load_dotenv()


OPEN_WEATHER_MAP_API = os.environ.get(
    "OPEN_WEATHER_MAP_API", "your_open_weather_api_key"
)
OPEN_WEATHER_MAP_API_KEY = os.environ.get(
    "OPEN_WEATHER_MAP_API_KEY", "your_open_weather_api_key"
)
