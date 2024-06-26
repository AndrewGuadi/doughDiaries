import os
from datetime import timedelta


class Config:
    """Base configuration with settings common to all environments."""
    SECRET_KEY = 'SECRETS_NEED_CHANGED'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class ProductionConfig(Config):
    """Production-specific configuration."""
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///production.db')
    # SESSION_COOKIE_SECURE = True
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
    # DEBUG = False

class DevelopmentConfig(Config):
    """Development environment specific configuration."""
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'omyguasch@gmail.com'
    MAIL_PASSWORD = 'cfmc vzvr wjkk nxyr'
    MAIL_DEFAULT_SENDER = 'omyguasch@gmail.com'  # Default sender
    SECRET_KEY = 'SECRETS_NEED_CHANGED'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    DEBUG = True

class TestingConfig(Config):
    """Testing environment specific configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    TESTING = True
