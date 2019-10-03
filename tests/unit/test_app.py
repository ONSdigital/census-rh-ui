from importlib import reload

from unittest import TestCase, mock

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp.web_app import Application
from aiohttp_session import session_middleware
from aiohttp_session import SimpleCookieStorage
from aioresponses import aioresponses

from envparse import ConfigurationError, env

from app.app import create_app

from app import session


class TestCreateApp(AioHTTPTestCase):
    config = 'TestingConfig'

    def session_storage(self, app_config):
        self.assertIn('REDIS_SERVER', app_config)
        self.assertIn('REDIS_PORT', app_config)
        self.assertIn('SESSION_AGE', app_config)
        return session_middleware(
            SimpleCookieStorage(cookie_name='RH_SESSION'))

    async def get_application(self):
        from app import settings
        settings.DEBUG = False  # force security headers to be applied to response
        # Monkey patch the session setup function to remove Redis dependency for unit tests
        session.setup = self.session_storage
        return create_app(self.config)

    @unittest_run_loop
    async def test_create_app(self):
        self.assertIsInstance(self.app, Application)

    @unittest_run_loop
    async def test_security_headers(self):
        with mock.patch('app.security.get_random_string') as mocked_rando:
            response = await self.client.request('GET', '/')
        self.assertEqual(response.headers['Strict-Transport-Security'],
                         'max-age=31536000 includeSubDomains')
        self.assertIn("default-src 'self' https://cdn.ons.gov.uk",
                      response.headers['Content-Security-Policy'])
        self.assertIn("font-src 'self' data: https://cdn.ons.gov.uk",
                      response.headers['Content-Security-Policy'])
        self.assertIn(
            "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://tagmanager.google.com https://www.google-analytics.com https://cdn.ons.gov.uk https://connect.facebook.net",
            response.headers['Content-Security-Policy'])
        self.assertIn(
            "connect-src 'self' https://www.googletagmanager.com https://tagmanager.google.com https://cdn.ons.gov.uk",
            response.headers['Content-Security-Policy'])
        self.assertIn(
            "img-src 'self' data: https://www.googletagmanager.com https://cdn.ons.gov.uk https://www.google-analytics.com https://www.facebook.com",
            response.headers['Content-Security-Policy'])
        self.assertEqual(response.headers['X-XSS-Protection'], '1; mode=block')
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(response.headers['Referrer-Policy'], 'strict-origin-when-cross-origin')


class TestCreateAppURLPathPrefix(TestCase):
    config = 'TestingConfig'

    def test_create_app_with_url_path_prefix_en(self):
        from app import config

        url_prefix = '/url-path-prefix'
        config.TestingConfig.URL_PATH_PREFIX = url_prefix

        app = create_app(self.config)
        self.assertEqual(app['URL_PATH_PREFIX'], url_prefix)

        self.assertEqual(app.router['IndexEN:get'].canonical,
                         '/url-path-prefix/start/')
        self.assertEqual(app.router['IndexEN:post'].canonical,
                         '/url-path-prefix/start/')
        self.assertEqual(app.router['Info:get'].canonical, '/info')

    def test_create_app_with_url_path_prefix_ni(self):
        from app import config

        url_prefix = '/url-path-prefix'
        config.TestingConfig.URL_PATH_PREFIX = url_prefix

        app = create_app(self.config)
        self.assertEqual(app['URL_PATH_PREFIX'], url_prefix)

        self.assertEqual(app.router['IndexNI:get'].canonical,
                         '/url-path-prefix/ni/start/')
        self.assertEqual(app.router['IndexNI:post'].canonical,
                         '/url-path-prefix/ni/start/')
        self.assertEqual(app.router['Info:get'].canonical, '/info')

    def test_create_app_without_url_path_prefix_en(self):
        from app import config

        config.TestingConfig.URL_PATH_PREFIX = ''

        app = create_app(self.config)
        self.assertEqual(app['URL_PATH_PREFIX'], '')

        self.assertEqual(app.router['IndexEN:get'].canonical, '/start/')
        self.assertEqual(app.router['IndexEN:post'].canonical, '/start/')
        self.assertEqual(app.router['Info:get'].canonical, '/info')

    def test_create_app_without_url_path_prefix_ni(self):
        from app import config

        config.TestingConfig.URL_PATH_PREFIX = ''

        app = create_app(self.config)
        self.assertEqual(app['URL_PATH_PREFIX'], '')

        self.assertEqual(app.router['IndexNI:get'].canonical, '/ni/start/')
        self.assertEqual(app.router['IndexNI:post'].canonical, '/ni/start/')
        self.assertEqual(app.router['Info:get'].canonical, '/info')


class TestCreateAppMissingConfig(TestCase):
    config = 'ProductionConfig'
    env_file = 'tests/test_data/local.env'

    def test_create_prod_app(self):
        from app import config

        config.ProductionConfig.ACCOUNT_SERVICE_URL = None

        with self.assertRaises(ConfigurationError) as ex:
            create_app(self.config)
        self.assertIn('not set', ex.exception.args[0])

        env.read_envfile(self.env_file)
        reload(config)
        self.assertIsInstance(create_app(self.config), Application)


class TestCheckServices(AioHTTPTestCase):
    config = 'TestingConfig'
    # required_services = ('case', 'collection_exercise', 'collection_instrument', 'iac', 'sample', 'survey')
    required_services = ['rhsvc']

    def session_storage(self, app_config):
        self.assertIn('REDIS_SERVER', app_config)
        self.assertIn('REDIS_PORT', app_config)
        return session_middleware(
            SimpleCookieStorage(cookie_name='RH_SESSION'))

    async def get_application(self):
        # Monkey patch the session setup function to remove Redis dependency for unit tests
        session.setup = self.session_storage
        return create_app(self.config)

    @unittest_run_loop
    async def test_service_status_urls(self):
        from app.config import TestingConfig

        self.assertEqual(len(self.required_services),
                         len(self.app.service_status_urls))

        for service in self.required_services:
            config_name = f'{service}_url'.upper()
            self.assertIn(config_name, self.app.service_status_urls)
            self.assertEqual(
                getattr(TestingConfig, config_name) + '/info',
                self.app.service_status_urls[config_name])

    @unittest_run_loop
    async def test_check_services(self):
        with aioresponses() as mocked:
            for service_url in self.app.service_status_urls.values():
                mocked.get(service_url)
            self.assertTrue(await self.app.check_services())

    @unittest_run_loop
    async def test_check_services_failed(self):
        with aioresponses():
            self.assertFalse(await self.app.check_services())
