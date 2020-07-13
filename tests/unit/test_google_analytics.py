from aiohttp.test_utils import make_mocked_request, unittest_run_loop

from app.google_analytics import ga_ua_id_processor
from . import RHTestCase


class TestGoogleAnalytics(RHTestCase):
    @unittest_run_loop
    async def test_google_analytics_context(self):
        self.app['GTM_AUTH'] = '12345'
        self.app['GTM_PREVIEW'] = 'env-5'
        self.app['GTM_COOKIES_WIN'] = 'x'
        request = make_mocked_request('GET', '/', app=self.app)
        context = await ga_ua_id_processor(request)
        self.assertEqual(context['gtm_auth'], '12345')
        self.assertEqual(context['gtm_preview'], 'env-5')
        self.assertEqual(context['gtm_cookies_win'], 'x')

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_en(self):
        self.app['GTM_AUTH'] = '12345'
        self.app['GTM_PREVIEW'] = 'env-5'
        self.app['GTM_COOKIES_WIN'] = 'x'
        response = await self.client.request('GET', self.get_start_en)
        self.assertEqual(response.status, 200)
        self.assertIn(f"gtm_auth=12345&gtm_preview=env-5&gtm_cookies_win=x".encode(), await
                      response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_cy(self):
        self.app['GTM_AUTH'] = '12345'
        self.app['GTM_PREVIEW'] = 'env-5'
        self.app['GTM_COOKIES_WIN'] = 'x'
        response = await self.client.request('GET', self.get_start_cy)
        self.assertEqual(response.status, 200)
        self.assertIn(f"gtm_auth=12345&gtm_preview=env-5&gtm_cookies_win=x".encode(), await
                      response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_ni(self):
        self.app['GTM_AUTH'] = '12345'
        self.app['GTM_PREVIEW'] = 'env-5'
        self.app['GTM_COOKIES_WIN'] = 'x'
        response = await self.client.request('GET', self.get_start_ni)
        self.assertEqual(response.status, 200)
        self.assertIn(f"gtm_auth=12345&gtm_preview=env-5&gtm_cookies_win=x".encode(), await
                      response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_en(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_start_en)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"ga('gtm_auth', '', 'auto');".encode(), await
                         response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_cy(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_start_cy)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"ga('gtm_auth', '', 'auto');".encode(), await
                         response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_ni(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_start_ni)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"ga('gtm_auth', '', 'auto');".encode(), await
                         response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_webchat_en(self):
        self.app['GTM_AUTH'] = '12345'
        self.app['GTM_PREVIEW'] = 'env-5'
        self.app['GTM_COOKIES_WIN'] = 'x'
        response = await self.client.request('GET', self.get_webchat_en)
        self.assertEqual(response.status, 200)
        self.assertIn(f"gtm_auth=12345&gtm_preview=env-5&gtm_cookies_win=x".encode(), await
                      response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_webchat_cy(self):
        self.app['GTM_AUTH'] = '12345'
        self.app['GTM_PREVIEW'] = 'env-5'
        self.app['GTM_COOKIES_WIN'] = 'x'
        response = await self.client.request('GET', self.get_webchat_cy)
        self.assertEqual(response.status, 200)
        self.assertIn(f"gtm_auth=12345&gtm_preview=env-5&gtm_cookies_win=x".encode(), await
                      response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_webchat_ni(self):
        self.app['GTM_AUTH'] = '12345'
        self.app['GTM_PREVIEW'] = 'env-5'
        self.app['GTM_COOKIES_WIN'] = 'x'
        response = await self.client.request('GET', self.get_webchat_ni)
        self.assertEqual(response.status, 200)
        self.assertIn(f"gtm_auth=12345&gtm_preview=env-5&gtm_cookies_win=x".encode(), await
                      response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_webchat_en(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_webchat_en)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"ga('gtm_auth', '', 'auto');".encode(), await
                         response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_webchat_cy(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_webchat_cy)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"ga('gtm_auth', '', 'auto');".encode(), await
                         response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_webchat_ni(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_webchat_ni)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"ga('gtm_auth', '', 'auto');".encode(), await
                         response.content.read())
