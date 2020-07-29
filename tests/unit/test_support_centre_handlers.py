from aiohttp.test_utils import unittest_run_loop

from . import RHTestCase


class TestSupportCentre(RHTestCase):

    @unittest_run_loop
    async def test_get_support_centre_enter_postcode_empty_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'GET', self.get_support_centre_enter_postcode_en)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received GET on endpoint 'en/find-a-support-centre'")
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/find-a-support-centre/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_en, contents)

            response = await self.client.request(
                'POST',
                self.post_support_centre_enter_postcode_en,
                data=self.support_centre_enter_postcode_input_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/find-a-support-centre'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/find-a-support-centre'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/find-a-support-centre/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_error_en, contents)

    @unittest_run_loop
    async def test_get_support_centre_enter_postcode_empty_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'GET', self.get_support_centre_enter_postcode_cy)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/find-a-support-centre'")
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/find-a-support-centre/" lang="en" >English</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_cy, contents)

            response = await self.client.request(
                'POST',
                self.post_support_centre_enter_postcode_cy,
                data=self.support_centre_enter_postcode_input_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/find-a-support-centre'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/find-a-support-centre'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/find-a-support-centre/" lang="en" >English</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_error_cy, contents)

    @unittest_run_loop
    async def test_get_support_centre_enter_postcode_invalid_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'GET', self.get_support_centre_enter_postcode_en)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received GET on endpoint 'en/find-a-support-centre'")
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/find-a-support-centre/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_en, contents)

            response = await self.client.request(
                'POST',
                self.post_support_centre_enter_postcode_en,
                data=self.support_centre_enter_postcode_input_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/find-a-support-centre'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/find-a-support-centre'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/find-a-support-centre/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_error_en, contents)

    @unittest_run_loop
    async def test_get_support_centre_enter_postcode_invalid_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'GET', self.get_support_centre_enter_postcode_cy)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/find-a-support-centre'")
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/find-a-support-centre/" lang="en" >English</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_cy, contents)

            response = await self.client.request(
                'POST',
                self.post_support_centre_enter_postcode_cy,
                data=self.support_centre_enter_postcode_input_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/find-a-support-centre'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/find-a-support-centre'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/find-a-support-centre/" lang="en" >English</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_error_cy, contents)
