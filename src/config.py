import aumbry
import os
from aumbry import Attr, YamlConfig


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DatabaseConfig(YamlConfig):
    __mapping__ = {
        'connection': Attr('connection', str),
    }

    connection = os.getenv('DB')


class ServiceConfig(YamlConfig):
    __mapping__ = {
        'host': Attr('host', str),
        'port': Attr('port', int),
        'log_level': Attr('log_level', str),
        'debug': Attr('debug', bool),
    }

    host = os.getenv('SERVICE_HOST', '0.0.0.0')
    port = os.getenv('SERVICE_PORT', 5000)
    log_level = os.getenv('SERVICE_LOG_LEVEL', 'debug')
    debug = os.getenv('SERVICE_DEBUG', True)


class ApiConfig(YamlConfig):
    __mapping__ = {
        'version': Attr('version', str),
    }

    version = os.getenv('API_VERSION', 'v1.0.0')


class AppConfig(YamlConfig):
    __mapping__ = {
        'api': Attr('api', ApiConfig),
        'service': Attr('service', ServiceConfig),
        'db': Attr('db', DatabaseConfig),
    }

    def __init__(self) -> None:
        self.api = ApiConfig()
        self.service = ServiceConfig()
        self.db = DatabaseConfig()


cfg = aumbry.load(
    aumbry.FILE,
    AppConfig,
    {
        'CONFIG_FILE_PATH': os.path.join(BASE_DIR, 'settings.yml')
    }
)