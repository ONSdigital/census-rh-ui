from aiohttp.test_utils import unittest_run_loop

from . import RHTestCase


class TestHandlers(RHTestCase):

    @unittest_run_loop
    async def test_get_accessibility_statement_en(self):
        response = await self.client.request(
            'GET', self.get_accessibility_statement_en)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Census questionnaire accessibility statement', contents)

    @unittest_run_loop
    async def test_get_accessibility_statement_cy(self):
        response = await self.client.request(
            'GET', self.get_accessibility_statement_cy)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Datganiad hygyrchedd holiadur y cyfrifiad', contents)

    @unittest_run_loop
    async def test_get_accessibility_statement_ni(self):
        response = await self.client.request(
            'GET', self.get_accessibility_statement_ni)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Census questionnaire accessibility statement', contents)
