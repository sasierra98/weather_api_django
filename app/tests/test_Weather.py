from django.test import TestCase
from mongoengine import connect, disconnect
import mongomock
from app.models.Weather import Weather, Coord, WeatherData, Main, Wind, Clouds, Sys


class TestWeatherModel(TestCase):
    @classmethod
    def setUpClass(cls):
        # Connect to a test database
        disconnect()
        connect(
            "mongoenginetest",
            host="mongodb://localhost",
            mongo_client_class=mongomock.MongoClient,
        )
        print("Connected to test database")

    @classmethod
    def tearDownClass(cls):
        # Disconnect from the test database
        disconnect()
        print("Disconnected from test database")

    def setUp(self):
        # Clear the database before each test
        Weather.objects.delete()
        print("Database cleared before test")

    def test_create_weather(self):
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
        sys = Sys(
            type=3, id=2019346, country="JP", sunrise=1560343627, sunset=1560396563
        )

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

        # Retrieve the weather object from the database
        retrieved_weather = Weather.objects(id=1851632).first()

        # Assertions to check if the object was saved correctly
        self.assertIsNotNone(retrieved_weather)
        self.assertEqual(retrieved_weather.coord.lon, 139)
        self.assertEqual(retrieved_weather.coord.lat, 35)
        self.assertEqual(retrieved_weather.weather[0].main, "Clear")
        self.assertEqual(retrieved_weather.main.temp, 289.92)
        self.assertEqual(retrieved_weather.wind.speed, 0.47)
        self.assertEqual(retrieved_weather.clouds.all, 2)
        self.assertEqual(retrieved_weather.sys.country, "JP")
        self.assertEqual(retrieved_weather.name, "Shuzenji")
        print("--> test_create_weather completed successfully")

    def test_update_weather(self):
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
        sys = Sys(
            type=3, id=2019346, country="JP", sunrise=1560343627, sunset=1560396563
        )

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

        # Update the weather object
        weather.update(set__name="UpdatedName")
        updated_weather = Weather.objects(id=1851632).first()

        # Assertions to check if the object was updated correctly
        self.assertEqual(updated_weather.name, "UpdatedName")
        print("--> test_update_weather completed successfully")

    def test_delete_weather(self):
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
        sys = Sys(
            type=3, id=2019346, country="JP", sunrise=1560343627, sunset=1560396563
        )

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

        # Delete the weather object
        weather.delete()
        deleted_weather = Weather.objects(id=1851632).first()

        # Assertions to check if the object was deleted correctly
        self.assertIsNone(deleted_weather)
        print("--> test_delete_weather completed successfully")
