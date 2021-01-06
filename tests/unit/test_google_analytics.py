from aiohttp.test_utils import make_mocked_request, unittest_run_loop

from app.google_analytics import ga_ua_id_processor
from . import RHTestCase


class TestGoogleAnalytics(RHTestCase):
    @unittest_run_loop
    async def test_google_analytics_context(self):
        self.app['GTM_CONTAINER_ID'] = 'GTM-XXXXXXX'
        self.app['GTM_AUTH'] = '12345'
        request = make_mocked_request('GET', '/', app=self.app)
        context = await ga_ua_id_processor(request)
        self.assertEqual(context['gtm_cont_id'], 'GTM-XXXXXXX')
        self.assertEqual(context['gtm_auth'], '12345')

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_en(self):
        self.app['GTM_CONTAINER_ID'] = 'GTM-XXXXXXX'
        self.app['GTM_AUTH'] = '12345'
        response = await self.client.request('GET', self.get_start_en)
        self.assertEqual(response.status, 200)
        response = await response.content.read()
        self.assertIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(), response)
        self.assertIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), response)

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_cy(self):
        self.app['GTM_CONTAINER_ID'] = 'GTM-XXXXXXX'
        self.app['GTM_AUTH'] = '12345'
        response = await self.client.request('GET', self.get_start_cy)
        self.assertEqual(response.status, 200)
        response = await response.content.read()
        self.assertIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(), response)
        self.assertIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), response)

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_ni(self):
        self.app['GTM_CONTAINER_ID'] = 'GTM-XXXXXXX'
        self.app['GTM_AUTH'] = '12345'
        response = await self.client.request('GET', self.get_start_ni)
        self.assertEqual(response.status, 200)
        response = await response.content.read()
        self.assertIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(), response)
        self.assertIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), response)

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_missing_container_id_base_en(self):
        self.app['GTM_CONTAINER_ID'] = ''

        response = await self.client.request('GET', self.get_start_en)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(),
                         await response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_missing_container_id_base_cy(self):
        self.app['GTM_CONTAINER_ID'] = ''

        response = await self.client.request('GET', self.get_start_cy)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(),
                         await response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_missing_container_id_base_ni(self):
        self.app['GTM_CONTAINER_ID'] = ''

        response = await self.client.request('GET', self.get_start_ni)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(),
                         await response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_en(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_start_en)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), await response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_cy(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_start_cy)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), await response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_ni(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_start_ni)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), await response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_webchat_en(self):
        self.app['GTM_CONTAINER_ID'] = 'GTM-XXXXXXX'
        self.app['GTM_AUTH'] = '12345'
        response = await self.client.request('GET', self.get_webchat_en)
        self.assertEqual(response.status, 200)
        response = await response.content.read()
        self.assertIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(), response)
        self.assertIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), response)

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_webchat_cy(self):
        self.app['GTM_CONTAINER_ID'] = 'GTM-XXXXXXX'
        self.app['GTM_AUTH'] = '12345'
        response = await self.client.request('GET', self.get_webchat_cy)
        self.assertEqual(response.status, 200)
        response = await response.content.read()
        self.assertIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(), response)
        self.assertIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), response)

    @unittest_run_loop
    async def test_google_analytics_script_rendered_base_webchat_ni(self):
        self.app['GTM_CONTAINER_ID'] = 'GTM-XXXXXXX'
        self.app['GTM_AUTH'] = '12345'
        response = await self.client.request('GET', self.get_webchat_ni)
        self.assertEqual(response.status, 200)
        response = await response.content.read()
        self.assertIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(), response)
        self.assertIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), response)

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_missing_container_id_base_webchat_en(self):
        self.app['GTM_CONTAINER_ID'] = ''

        response = await self.client.request('GET', self.get_webchat_en)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(),
                         await response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_missing_container_id_base_webchat_cy(self):
        self.app['GTM_CONTAINER_ID'] = ''

        response = await self.client.request('GET', self.get_webchat_cy)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(),
                         await response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_missing_container_id_base_webchat_ni(self):
        self.app['GTM_CONTAINER_ID'] = ''

        response = await self.client.request('GET', self.get_webchat_ni)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(),
                         await response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_webchat_en(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_webchat_en)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), await response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_webchat_cy(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_webchat_cy)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), await response.content.read())

    @unittest_run_loop
    async def test_google_analytics_script_not_rendered_base_webchat_ni(self):
        self.app['GTM_AUTH'] = ''

        response = await self.client.request('GET', self.get_webchat_ni)
        self.assertEqual(response.status, 200)
        self.assertNotIn(f"gtm_auth=12345&gtm_cookies_win=x".encode(), await response.content.read())
