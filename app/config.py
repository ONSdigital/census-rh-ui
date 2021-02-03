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

    def get_service_urls_mapped_with_path(self,
                                          path='/',
                                          suffix='URL',
                                          excludes=None) -> dict:
        return {
            service_name: f'{self[service_name]}{path}'
            for service_name in self
            if service_name.endswith(suffix) and service_name not in (
                excludes if excludes else [])
        }

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f'"{name}" not found')

    def __setattr__(self, name, value):
        self[name] = value


class BaseConfig:
    env = Env()
    env = partial(env, default=None)

    HOST = env('HOST')
    PORT = env('PORT')
    LOG_LEVEL = env('LOG_LEVEL')
    EXT_LOG_LEVEL = env('EXT_LOG_LEVEL')

    DOMAIN_URL_PROTOCOL = env('DOMAIN_URL_PROTOCOL', default='https://')
    DOMAIN_URL_EN = env('DOMAIN_URL_EN')
    DOMAIN_URL_CY = env('DOMAIN_URL_CY')

    ACCOUNT_SERVICE_URL = env('ACCOUNT_SERVICE_URL')
    EQ_URL = env('EQ_URL')
    JSON_SECRET_KEYS = env('JSON_SECRET_KEYS')

    RHSVC_URL = env('RHSVC_URL')
    RHSVC_AUTH = (env('RHSVC_USERNAME'), env('RHSVC_PASSWORD'))

    URL_PATH_PREFIX = env('URL_PATH_PREFIX', default='')

    GTM_CONTAINER_ID = env('GTM_CONTAINER_ID', default='')
    GTM_AUTH = env('GTM_AUTH', default='')

    REDIS_SERVER = env('REDIS_SERVER', default='localhost')

    REDIS_PORT = env('REDIS_PORT', default='7379')
    REDIS_POOL_MIN = env('REDIS_POOL_MIN', default='50')
    REDIS_POOL_MAX = env('REDIS_POOL_MAX', default='500')

    SESSION_AGE = env('SESSION_AGE', default='2700')  # 45 minutes

    WEBCHAT_SVC_URL = env('WEBCHAT_SVC_URL')

    ADDRESS_INDEX_SVC_URL = env('ADDRESS_INDEX_SVC_URL')
    ADDRESS_INDEX_SVC_AUTH = (env('ADDRESS_INDEX_SVC_USERNAME'), env('ADDRESS_INDEX_SVC_PASSWORD'))
    ADDRESS_INDEX_EPOCH = env('ADDRESS_INDEX_EPOCH', default='')

    AD_LOOK_UP_SVC_URL = env('AD_LOOK_UP_SVC_URL')
    AD_LOOK_UP_SVC_AUTH = (env('AD_LOOK_UP_SVC_USERNAME'), env('AD_LOOK_UP_SVC_PASSWORD'))
    AD_LOOK_UP_SVC_APIKEY = env('AD_LOOK_UP_SVC_APIKEY')
    AD_LOOK_UP_SVC_APPID = env('AD_LOOK_UP_SVC_APPID')
    EQ_SALT = env('EQ_SALT', default='s3cr3tS4lt')


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig:
    env = Env()
    HOST = env.str('HOST', default='0.0.0.0')
    PORT = env.int('PORT', default='9092')
    LOG_LEVEL = env('LOG_LEVEL', default='INFO')
    EXT_LOG_LEVEL = env('EXT_LOG_LEVEL', default='WARN')

    DOMAIN_URL_PROTOCOL = 'http://'
    DOMAIN_URL_EN = env.str('DOMAIN_URL_EN', default='localhost:9092')
    DOMAIN_URL_CY = env.str('DOMAIN_URL_CY', default='localhost:9092')

    ACCOUNT_SERVICE_URL = env.str('ACCOUNT_SERVICE_URL',
                                  default='http://localhost:9092')
    EQ_URL = env.str('EQ_URL', default='http://localhost:5000')
    JSON_SECRET_KEYS = env.str(
        'JSON_SECRET_KEYS',
        default=None) or open('./tests/test_data/test_keys.json').read()

    RHSVC_URL = env.str('RHSVC_URL', default='http://localhost:8071')
    RHSVC_AUTH = (env.str('RHSVC_USERNAME', default='admin'),
                  env.str('RHSVC_PASSWORD', default='secret'))

    URL_PATH_PREFIX = env('URL_PATH_PREFIX', default='')

    GTM_CONTAINER_ID = env.str('GTM_CONTAINER_ID', default='GTM-MRQGCXS')
    GTM_AUTH = env.str('GTM_AUTH', default='SMijm6Rii1nctiBFRb1Rdw')

    REDIS_SERVER = env('REDIS_SERVER', default='localhost')

    REDIS_PORT = env('REDIS_PORT', default='7379')
    REDIS_POOL_MIN = env('REDIS_POOL_MIN', default='50')
    REDIS_POOL_MAX = env('REDIS_POOL_MAX', default='500')

    SESSION_AGE = env('SESSION_AGE', default='2700')  # 45 minutes

    WEBCHAT_SVC_URL = env.str(
        'WEBCHAT_SVC_URL',
        default='https://www.timeforstorm.com/IM/endpoint/client/5441/ONSWebchat/ce033298af0c07067a77b7940c011ec8ef670d66b7fe15c5776a16e205478221'
    )  # yapf: disable

    ADDRESS_INDEX_SVC_URL = env.str('ADDRESS_INDEX_SVC_URL', default='http://localhost:9000')
    ADDRESS_INDEX_SVC_AUTH = (env.str('ADDRESS_INDEX_SVC_USERNAME', default='admin'),
                              env.str('ADDRESS_INDEX_SVC_PASSWORD', default='secret'))
    ADDRESS_INDEX_EPOCH = env.str('ADDRESS_INDEX_EPOCH', default='')

    AD_LOOK_UP_SVC_URL = env.str('AD_LOOK_UP_SVC_URL', default='http://localhost:8071/v1')
    AD_LOOK_UP_SVC_AUTH = (env.str('AD_LOOK_UP_SVC_USERNAME', default='admin'),
                           env.str('AD_LOOK_UP_SVC_PASSWORD', default='secret'))
    AD_LOOK_UP_SVC_APIKEY = env.str('AD_LOOK_UP_SVC_APIKEY', default='apikey')
    AD_LOOK_UP_SVC_APPID = env.str('AD_LOOK_UP_SVC_APPID', default='appid')
    EQ_SALT = env('EQ_SALT', default='s3cr3tS4lt')


class TestingConfig:
    HOST = '0.0.0.0'
    PORT = '9092'
    LOG_LEVEL = 'DEBUG'
    EXT_LOG_LEVEL = 'DEBUG'

    DOMAIN_URL_PROTOCOL = 'http://'
    DOMAIN_URL_EN = 'localhost:9092'
    DOMAIN_URL_CY = 'localhost:9092'

    ACCOUNT_SERVICE_URL = 'http://localhost:9092'
    EQ_URL = 'http://localhost:5000'
    JSON_SECRET_KEYS = open('./tests/test_data/test_keys.json').read()

    RHSVC_URL = 'http://localhost:8071'
    RHSVC_AUTH = ('admin', 'secret')

    URL_PATH_PREFIX = ''

    GTM_CONTAINER_ID = 'GTM-MRQGCXS'
    GTM_AUTH = 'SMijm6Rii1nctiBFRb1Rdw'

    REDIS_SERVER = ''

    REDIS_PORT = ''
    REDIS_POOL_MIN = '50'
    REDIS_POOL_MAX = '500'

    SESSION_AGE = ''

    WEBCHAT_SVC_URL = 'https://www.timeforstorm.com/IM/endpoint/client/5441/ONSWebchat/ce033298af0c07067a77b7940c011ec8ef670d66b7fe15c5776a16e205478221'

    ADDRESS_INDEX_SVC_URL = 'http://localhost:9000'
    ADDRESS_INDEX_SVC_AUTH = ('admin', 'secret')
    ADDRESS_INDEX_EPOCH = ''

    AD_LOOK_UP_SVC_URL = 'http://localhost:8071/v1'
    AD_LOOK_UP_SVC_AUTH = ('admin', 'secret')
    AD_LOOK_UP_SVC_APIKEY = 'apikey'
    AD_LOOK_UP_SVC_APPID = 'appid'
    EQ_SALT = 's3cr3tS4lt'
