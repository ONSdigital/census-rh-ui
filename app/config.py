from functools import partial

from envparse import Env, ConfigurationError


class Config(dict):

    def from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                config = getattr(obj, key)
                if config is None:
                    raise ConfigurationError(f'{key} not set')
                self[key] = config

    def get_service_urls_mapped_with_path(self, path='/', suffix='URL', excludes=None) -> dict:
        return {service_name: f"{self[service_name]}{path}"
                for service_name in self
                if service_name.endswith(suffix)
                and service_name not in (excludes if excludes else [])}

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError('"{}" not found'.format(name))

    def __setattr__(self, name, value):
        self[name] = value


class BaseConfig:
    env = Env()
    env = partial(env, default=None)

    HOST = env("HOST")
    PORT = env("PORT")
    LOG_LEVEL = env("LOG_LEVEL")

    ACCOUNT_SERVICE_URL = env("ACCOUNT_SERVICE_URL")
    EQ_URL = env("EQ_URL")
    JSON_SECRET_KEYS = env("JSON_SECRET_KEYS")

    RHSVC_URL = env("RHSVC_URL")
    RHSVC_AUTH = (env("RHSVC_USERNAME"), env("RHSVC_PASSWORD"))

    URL_PATH_PREFIX = env("URL_PATH_PREFIX", default="")

    ANALYTICS_UA_ID = env("ANALYTICS_UA_ID", default="")

    REDIS_SERVER = env("REDIS_SERVER", default="localhost")

    REDIS_PORT = env("REDIS_PORT", default="7379")

    SESSION_AGE = env("SESSION_AGE", default="600")

    WEBCHAT_SVC_URL = env("WEBCHAT_SVC_URL")

    AI_POSTCODE_SVC_URL = env("AI_POSTCODE_SVC_URL")


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig:
    env = Env()
    HOST = env.str("HOST", default="0.0.0.0")
    PORT = env.int("PORT", default="9092")
    LOG_LEVEL = env("LOG_LEVEL", default="INFO")

    ACCOUNT_SERVICE_URL = env.str("ACCOUNT_SERVICE_URL", default="http://localhost:9092")
    EQ_URL = env.str("EQ_URL", default="http://localhost:5000")
    JSON_SECRET_KEYS = env.str("JSON_SECRET_KEYS", default=None) or open("./tests/test_data/test_keys.json").read()

    RHSVC_URL = env.str("RHSVC_URL", default="http://localhost:8071")
    RHSVC_AUTH = (env.str("RHSVC_USERNAME", default="admin"), env.str("RHSVC_PASSWORD", default="secret"))

    URL_PATH_PREFIX = env("URL_PATH_PREFIX", default="")

    ANALYTICS_UA_ID = env("ANALYTICS_UA_ID", default="")

    REDIS_SERVER = env("REDIS_SERVER", default="localhost")

    REDIS_PORT = env("REDIS_PORT", default="7379")

    SESSION_AGE = env("SESSION_AGE", default="600")

    WEBCHAT_SVC_URL = env.str("WEBCHAT_SVC_URL", default="https://www.timeforstorm.com/IM/endpoint/client/5441/ONSWebchat/ce033298af0c07067a77b7940c011ec8ef670d66b7fe15c5776a16e205478221")  # NOQA

    AI_POSTCODE_SVC_URL = env.str("AI_POSTCODE_SVC_URL", default="http://addressindex-api-beta.apps.devtest.onsclofo.uk/addresses/postcode/")  # NOQA


class TestingConfig:
    HOST = "0.0.0.0"
    PORT = "9092"
    LOG_LEVEL = "INFO"

    ACCOUNT_SERVICE_URL = "http://localhost:9092"
    EQ_URL = "http://localhost:5000"
    JSON_SECRET_KEYS = open("./tests/test_data/test_keys.json").read()

    RHSVC_URL = "http://localhost:8071"
    RHSVC_AUTH = ("admin", "secret")

    URL_PATH_PREFIX = ""

    ANALYTICS_UA_ID = ""

    REDIS_SERVER = ""

    REDIS_PORT = ""

    SESSION_AGE = ""

    WEBCHAT_SVC_URL = "https://www.timeforstorm.com/IM/endpoint/client/5441/ONSWebchat/ce033298af0c07067a77b7940c011ec8ef670d66b7fe15c5776a16e205478221"  # NOQA

    AI_POSTCODE_SVC_URL = "http://addressindex-api-beta.apps.devtest.onsclofo.uk/addresses/postcode/"  # NOQA
