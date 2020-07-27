from aiohttp.test_utils import unittest_run_loop

from . import RHTestCase


class TestStatic(RHTestCase):

    @unittest_run_loop
    async def test_get_accessibility_statement_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'GET', self.get_accessibility_statement_en)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/accessibility'")
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/start/accessibility/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn('Census questionnaire accessibility statement', contents)

    @unittest_run_loop
    async def test_get_accessibility_statement_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'GET', self.get_accessibility_statement_cy)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/accessibility'")
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/start/accessibility/" lang="en" >English</a>', contents)
            self.assertIn('Datganiad hygyrchedd holiadur y cyfrifiad', contents)

    @unittest_run_loop
    async def test_get_accessibility_statement_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'GET', self.get_accessibility_statement_ni)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/accessibility'")
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Census questionnaire accessibility statement', contents)
