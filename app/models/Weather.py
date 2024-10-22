from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    FloatField,
    DateTimeField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    IntField,
)
import pytz


class Coord(EmbeddedDocument):
    lon = FloatField()
    lat = FloatField()


class WeatherData(EmbeddedDocument):
    id = IntField()
    main = StringField()
    description = StringField()
    icon = StringField()


class Main(EmbeddedDocument):
    temp = FloatField()
    feels_like = FloatField()
    temp_min = FloatField()
    temp_max = FloatField()
    pressure = IntField()
    humidity = IntField()
    sea_level = IntField()
    grnd_level = IntField()


class Wind(EmbeddedDocument):
    speed = FloatField()
    deg = IntField()


class Clouds(EmbeddedDocument):
    all = IntField()


class Sys(EmbeddedDocument):
    type = IntField()
    id = IntField()
    country = StringField()
    sunrise = IntField()
    sunset = IntField()


class Weather(Document):
    created_at = DateTimeField(default=datetime.now(tz=pytz.UTC))
    updated_at = DateTimeField(default=datetime.now(tz=pytz.UTC))
    id = IntField(primary_key=True)
    coord = EmbeddedDocumentField(Coord)
    weather = ListField(EmbeddedDocumentField(WeatherData))
    base = StringField()
    main = EmbeddedDocumentField(Main)
    visibility = IntField()
    wind = EmbeddedDocumentField(Wind)
    clouds = EmbeddedDocumentField(Clouds)
    dt = IntField()
    sys = EmbeddedDocumentField(Sys)
    timezone = IntField()
    name = StringField()
    cod = IntField()
    forecast = ListField()
