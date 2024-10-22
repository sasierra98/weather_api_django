import pytest
from mongoengine import connect, disconnect
import mongomock
from app.models import Weather, Coord, WeatherData, Main, Wind, Clouds, Sys


@pytest.fixture(scope="module", autouse=True)
def mongoengine_connection():
    disconnect()
    connect(
        "mongoenginetest",
        host="mongodb://localhost",
        mongo_client_class=mongomock.MongoClient,
        uuidRepresentation="standard",
    )


@pytest.fixture(autouse=True)
def clear_db():
    Weather.objects.delete()
    print("Database cleared before test")


def test_create_weather():
    print("Running test_create_weather")
    coord = Coord(lon=139, lat=35)
    weather_data = WeatherData(
        id=800, main="Clear", description="clear sky", icon="01n"
    )
    main = Main(
        temp=289.92,
        feels_like=287.15,
        temp_min=288.71,
        temp_max=290.93,
        pressure=1013,
        humidity=100,
        sea_level=1013,
        grnd_level=1013,
    )
    wind = Wind(speed=0.47, deg=107)
    clouds = Clouds(all=2)
    sys = Sys(type=3, id=2019346, country="JP", sunrise=1560343627, sunset=1560396563)

    weather = Weather(
        id=1851632,
        coord=coord,
        weather=[weather_data],
        base="stations",
        main=main,
        visibility=10000,
        wind=wind,
        clouds=clouds,
        dt=1560350192,
        sys=sys,
        timezone=32400,
        name="Shuzenji",
        cod=200,
    )
    weather.save()

    retrieved_weather = Weather.objects(id=1851632).first()

    assert retrieved_weather is not None
    assert retrieved_weather.coord.lon == 139
    assert retrieved_weather.coord.lat == 35
    assert retrieved_weather.weather[0].main == "Clear"
    assert retrieved_weather.main.temp == 289.92
    assert retrieved_weather.wind.speed == 0.47
    assert retrieved_weather.clouds.all == 2
    assert retrieved_weather.sys.country == "JP"
    assert retrieved_weather.name == "Shuzenji"
    print("--> test_create_weather completed successfully")


def test_update_weather():
    print("Running test_update_weather")
    coord = Coord(lon=139, lat=35)
    weather_data = WeatherData(
        id=800, main="Clear", description="clear sky", icon="01n"
    )
    main = Main(
        temp=289.92,
        feels_like=287.15,
        temp_min=288.71,
        temp_max=290.93,
        pressure=1013,
        humidity=100,
        sea_level=1013,
        grnd_level=1013,
    )
    wind = Wind(speed=0.47, deg=107)
    clouds = Clouds(all=2)
    sys = Sys(type=3, id=2019346, country="JP", sunrise=1560343627, sunset=1560396563)

    weather = Weather(
        id=1851632,
        coord=coord,
        weather=[weather_data],
        base="stations",
        main=main,
        visibility=10000,
        wind=wind,
        clouds=clouds,
        dt=1560350192,
        sys=sys,
        timezone=32400,
        name="Shuzenji",
        cod=200,
    )
    weather.save()

    weather.update(set__name="UpdatedName")
    updated_weather = Weather.objects(id=1851632).first()

    assert updated_weather.name == "UpdatedName"
    print("--> test_update_weather completed successfully")


def test_delete_weather():
    print("Running test_delete_weather")
    coord = Coord(lon=139, lat=35)
    weather_data = WeatherData(
        id=800, main="Clear", description="clear sky", icon="01n"
    )
    main = Main(
        temp=289.92,
        feels_like=287.15,
        temp_min=288.71,
        temp_max=290.93,
        pressure=1013,
        humidity=100,
        sea_level=1013,
        grnd_level=1013,
    )
    wind = Wind(speed=0.47, deg=107)
    clouds = Clouds(all=2)
    sys = Sys(type=3, id=2019346, country="JP", sunrise=1560343627, sunset=1560396563)

    weather = Weather(
        id=1851632,
        coord=coord,
        weather=[weather_data],
        base="stations",
        main=main,
        visibility=10000,
        wind=wind,
        clouds=clouds,
        dt=1560350192,
        sys=sys,
        timezone=32400,
        name="Shuzenji",
        cod=200,
    )
    weather.save()

    weather.delete()
    deleted_weather = Weather.objects(id=1851632).first()

    assert deleted_weather is None
    print("--> test_delete_weather completed successfully")
