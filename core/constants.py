import os
from dotenv import load_dotenv


load_dotenv()


# Django
APP_SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")
APP_STAGE = os.environ.get("APP_STAGE", "development")

# Postgres
POSTGRES_DB = os.environ.get("POSTGRES_DB", "your_db_name")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "your_db_user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "your_db_password")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)

# MongoDB
MONGO_DB = os.environ.get("MONGO_DB", "your_db_name")
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_USERNAME = os.environ.get("MONGO_USERNAME", "your_db_name")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "your_db_name")

# Redis
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_DB = os.environ.get("REDIS_DB", "0")
