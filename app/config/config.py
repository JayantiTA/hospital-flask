import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration."""

    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False


def get_config_by_name(config_name):
    """Get config by name"""
    if config_name == "development":
        return DevelopmentConfig()
    elif config_name == "production":
        return ProductionConfig()
    elif config_name == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()
