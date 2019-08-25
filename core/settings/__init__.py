import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    env: str
    debug: bool = os.getenv('DEBUG', True)
    app_host: str = os.getenv('APP_HOST', '0.0.0.0')
    app_port: int = os.getenv('APP_PORT', 8000)
    db_url: str = os.getenv(
        'DB_URL',
        'mysql+pymysql://sanic:sanic@localhost:3306/sanic',
    )


@dataclass(frozen=True)
class DevelopmentConfig(Config):
    env: str = 'development'
    debug: bool = True


@dataclass(frozen=True)
class TestingConfig(Config):
    env: str = 'testing'
    debug: bool = True


@dataclass(frozen=True)
class ProductionConfig(Config):
    env: str = 'production'
    debug: bool = False


def get_config():
    env = os.getenv('env', 'development')
    config_type = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    return config_type[env]
