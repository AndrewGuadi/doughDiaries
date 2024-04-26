import os

class Config:
    """Base configuration with settings common to all environments."""
    SECRET_KEY = 'SECRETS_NEED_CHANGED'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class ProductionConfig(Config):
    """Production-specific configuration."""
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///production.db')
    # DEBUG = False

class DevelopmentConfig(Config):
    """Development environment specific configuration."""
    SECRET_KEY = 'SECRETS_NEED_CHANGED'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    DEBUG = True

class TestingConfig(Config):
    """Testing environment specific configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    TESTING = True
