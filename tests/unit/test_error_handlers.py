from aiohttp.test_utils import unittest_run_loop

from . import RHTestCase


class TestErrorHandlers(RHTestCase):

    @unittest_run_loop
    async def test_partial_path_redirects_to_index_en(self):
        with self.assertLogs('respondent-home', 'DEBUG') as cm:
            response = await self.client.request('GET', str(self.get_start_en).rstrip('/'))
        self.assertLogEvent(cm, 'redirecting to index')
        self.assertEqual(response.status, 200)
        contents = await response.content.read()
        self.assertIn(self.content_start_uac_title_en, str(contents))
        self.assertEqual(contents.count(b'input--text'), 1)
        self.assertIn(b'type="submit"', contents)

    @unittest_run_loop
    async def test_partial_path_redirects_to_index_cy(self):
        with self.assertLogs('respondent-home', 'DEBUG') as cm:
            response = await self.client.request('GET', str(self.get_start_cy).rstrip('/'))
        self.assertLogEvent(cm, 'redirecting to index')
        self.assertEqual(response.status, 200)
        contents = await response.content.read()
        self.assertIn(self.content_start_uac_title_cy, str(contents))
        self.assertEqual(contents.count(b'input--text'), 1)
        self.assertIn(b'type="submit"', contents)

    @unittest_run_loop
    async def test_partial_path_redirects_to_index_ni(self):
        with self.assertLogs('respondent-home', 'DEBUG') as cm:
            response = await self.client.request('GET', str(self.get_start_ni).rstrip('/'))
        self.assertLogEvent(cm, 'redirecting to index')
        self.assertEqual(response.status, 200)
        contents = await response.content.read()
        self.assertIn(self.content_start_uac_title_en, str(contents))
        self.assertEqual(contents.count(b'input--text'), 1)
        self.assertIn(b'type="submit"', contents)

    @unittest_run_loop
    async def test_404_renders_template(self):
        response = await self.client.request('GET', '/unknown-path')
        self.assertEqual(response.status, 404)
        contents = str(await response.content.read())
        self.assertIn('Page not found', contents)
