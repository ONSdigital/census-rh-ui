from unittest import mock
from aiohttp.test_utils import unittest_run_loop
from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses

from . import RHTestCase

import urllib.parse


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
            self.assertIn(self.content_support_centre_enter_postcode_page_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_en, contents)

            response = await self.client.request(
                'POST',
                self.post_support_centre_enter_postcode_en,
                data=self.support_centre_enter_postcode_input_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/find-a-support-centre'")
            self.assertLogEvent(cm, 'invalid postcode')
            self.assertLogEvent(cm, "received GET on endpoint 'en/find-a-support-centre'")

            self.assertEqual(response.status, 200)
            resp_content = str(await response.content.read())
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/find-a-support-centre/" lang="cy" >Cymraeg</a>', resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_page_title_error_en, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_title_en, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_en, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_error_empty_en, resp_content)

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
            self.assertIn(self.content_support_centre_enter_postcode_page_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_cy, contents)

            response = await self.client.request(
                'POST',
                self.post_support_centre_enter_postcode_cy,
                data=self.support_centre_enter_postcode_input_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/find-a-support-centre'")
            self.assertLogEvent(cm, 'invalid postcode')
            self.assertLogEvent(cm, "received GET on endpoint 'cy/find-a-support-centre'")

            self.assertEqual(response.status, 200)
            resp_content = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/find-a-support-centre/" lang="en" >English</a>', resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_page_title_error_cy, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_title_cy, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_cy, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_error_empty_cy, resp_content)

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
            self.assertIn(self.content_support_centre_enter_postcode_page_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_en, contents)

            response = await self.client.request(
                'POST',
                self.post_support_centre_enter_postcode_en,
                data=self.support_centre_enter_postcode_input_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/find-a-support-centre'")
            self.assertLogEvent(cm, 'invalid postcode')
            self.assertLogEvent(cm, "received GET on endpoint 'en/find-a-support-centre'")

            self.assertEqual(response.status, 200)
            resp_content = str(await response.content.read())
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/find-a-support-centre/" lang="cy" >Cymraeg</a>', resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_page_title_error_en, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_title_en, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_en, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_error_invalid_en, resp_content)

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
            self.assertIn(self.content_support_centre_enter_postcode_page_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_cy, contents)

            response = await self.client.request('POST',
                                                 self.post_support_centre_enter_postcode_cy,
                                                 data=self.support_centre_enter_postcode_input_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/find-a-support-centre'")
            self.assertLogEvent(cm, 'invalid postcode')
            self.assertLogEvent(cm, "received GET on endpoint 'cy/find-a-support-centre'")

            self.assertEqual(response.status, 200)
            resp_content = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/find-a-support-centre/" lang="en" >English</a>', resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_page_title_error_cy, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_title_cy, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_cy, resp_content)
            self.assertIn(self.content_support_centre_enter_postcode_error_invalid_cy, resp_content)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_invalid_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'GET', self.get_support_centre_list_of_centres_postcode_invalid_en)
            self.assertEqual(response.status, 404)
            self.assertLogEvent(cm, 'invalid postcode')
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/find-a-support-centre/' + urllib.parse.quote(self.postcode_invalid) +
                          '/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_common_404_error_title_en, contents)
            self.assertIn(self.content_common_404_error_secondary_en, contents)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_invalid_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'GET', self.get_support_centre_list_of_centres_postcode_invalid_cy)
            self.assertEqual(response.status, 404)
            self.assertLogEvent(cm, 'invalid postcode')
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/find-a-support-centre/' + urllib.parse.quote(self.postcode_invalid) +
                          '/" lang="en" >English</a>', contents)
            self.assertIn(self.content_common_404_error_title_cy, contents)
            self.assertIn(self.content_common_404_error_secondary_cy, contents)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_single_result_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.ADLookUp.get_ad_lookup_by_postcode') as mocked_get_ad_lookup_by_postcode:
            mocked_get_ad_lookup_by_postcode.return_value = self.ad_single_return

            response = await self.client.request(
                'GET', self.get_support_centre_enter_postcode_en)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received GET on endpoint 'en/find-a-support-centre'")
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/find-a-support-centre/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_page_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_en, contents)

            response = await self.client.request(
                'POST',
                self.post_support_centre_enter_postcode_en,
                data=self.support_centre_enter_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/find-a-support-centre'")
            self.assertLogEvent(cm, 'valid postcode')
            self.assertLogEvent(cm, "received GET on endpoint 'en/find-a-support-centre/" + self.postcode_valid + "'")

            self.assertEqual(response.status, 200)
            resp_content = str(await response.content.read())
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/find-a-support-centre/' + urllib.parse.quote(self.postcode_valid) +
                          '/" lang="cy" >Cymraeg</a>', resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_title_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_location_name_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_distance_away_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_address_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_google_url, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_telephone_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_email_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_monday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_tuesday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_wednesday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_thursday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_friday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_saturday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_sunday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_census_saturday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_census_day_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_good_friday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_easter_monday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_may_bank_holiday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_public_parking_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_level_access_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_wheelchair_access_en, resp_content)
            self.assertNotIn(self.content_support_centre_list_of_centres_result_one_disability_aware_en, resp_content)
            self.assertNotIn(self.content_support_centre_list_of_centres_result_one_hearing_loop_en, resp_content)
            self.assertNotIn(self.content_support_centre_list_of_centres_result_two_location_name_en, resp_content)
            self.assertNotIn(self.content_support_centre_list_of_centres_result_two_public_parking_en, resp_content)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_single_result_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.ADLookUp.get_ad_lookup_by_postcode') as mocked_get_ad_lookup_by_postcode:
            mocked_get_ad_lookup_by_postcode.return_value = self.ad_single_return

            response = await self.client.request(
                'GET', self.get_support_centre_enter_postcode_cy)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/find-a-support-centre'")
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/find-a-support-centre/" lang="en" >English</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_page_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_cy, contents)

            response = await self.client.request(
                'POST',
                self.post_support_centre_enter_postcode_cy,
                data=self.support_centre_enter_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/find-a-support-centre'")
            self.assertLogEvent(cm, 'valid postcode')
            self.assertLogEvent(cm, "received GET on endpoint 'cy/find-a-support-centre/" + self.postcode_valid + "'")

            self.assertEqual(response.status, 200)
            resp_content = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/find-a-support-centre/' + urllib.parse.quote(self.postcode_valid) +
                          '/" lang="en" >English</a>', resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_title_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_location_name_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_distance_away_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_address_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_google_url, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_telephone_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_email_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_monday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_tuesday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_wednesday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_thursday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_friday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_saturday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_sunday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_census_saturday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_census_day_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_good_friday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_easter_monday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_open_may_bank_holiday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_public_parking_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_level_access_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_wheelchair_access_cy, resp_content)
            self.assertNotIn(self.content_support_centre_list_of_centres_result_one_disability_aware_cy, resp_content)
            self.assertNotIn(self.content_support_centre_list_of_centres_result_one_hearing_loop_cy, resp_content)
            self.assertNotIn(self.content_support_centre_list_of_centres_result_two_location_name_cy, resp_content)
            self.assertNotIn(self.content_support_centre_list_of_centres_result_two_public_parking_cy, resp_content)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_multiple_results_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.ADLookUp.get_ad_lookup_by_postcode') as mocked_get_ad_lookup_by_postcode:
            mocked_get_ad_lookup_by_postcode.return_value = self.ad_multiple_return

            response = await self.client.request(
                'GET', self.get_support_centre_enter_postcode_en)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received GET on endpoint 'en/find-a-support-centre'")
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/find-a-support-centre/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_page_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_en, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_en, contents)

            response = await self.client.request(
                'POST',
                self.post_support_centre_enter_postcode_en,
                data=self.support_centre_enter_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/find-a-support-centre'")
            self.assertLogEvent(cm, 'valid postcode')
            self.assertLogEvent(cm, "received GET on endpoint 'en/find-a-support-centre/" + self.postcode_valid + "'")

            self.assertEqual(response.status, 200)
            resp_content = str(await response.content.read())
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/find-a-support-centre/' + urllib.parse.quote(self.postcode_valid) +
                          '/" lang="cy" >Cymraeg</a>', resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_title_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_location_name_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_two_location_name_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_monday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_tuesday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_wednesday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_thursday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_friday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_saturday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_sunday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_census_saturday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_census_day_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_good_friday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_easter_monday_en, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_may_bank_holiday_en, resp_content)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_multiple_results_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.ADLookUp.get_ad_lookup_by_postcode') as mocked_get_ad_lookup_by_postcode:
            mocked_get_ad_lookup_by_postcode.return_value = self.ad_multiple_return

            response = await self.client.request(
                'GET', self.get_support_centre_enter_postcode_cy)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/find-a-support-centre'")
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/find-a-support-centre/" lang="en" >English</a>', contents)
            self.assertIn(self.content_support_centre_enter_postcode_page_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_title_cy, contents)
            self.assertIn(self.content_support_centre_enter_postcode_secondary_cy, contents)

            response = await self.client.request(
                'POST',
                self.post_support_centre_enter_postcode_cy,
                data=self.support_centre_enter_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/find-a-support-centre'")
            self.assertLogEvent(cm, 'valid postcode')
            self.assertLogEvent(cm, "received GET on endpoint 'cy/find-a-support-centre/" + self.postcode_valid + "'")

            self.assertEqual(response.status, 200)
            resp_content = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/find-a-support-centre/' + urllib.parse.quote(self.postcode_valid) +
                          '/" lang="en" >English</a>', resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_title_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_one_location_name_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_two_location_name_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_monday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_tuesday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_wednesday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_thursday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_friday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_saturday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_sunday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_census_saturday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_census_day_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_good_friday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_easter_monday_cy, resp_content)
            self.assertIn(self.content_support_centre_list_of_centres_result_closed_may_bank_holiday_cy, resp_content)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_connection_error_en(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.ad_lookup_url, exception=ClientConnectionError('Failed'))

            response = await self.client.request('GET', self.get_support_centre_list_of_centres_postcode_valid_en)

            self.assertLogEvent(cm, 'client failed to connect', url=self.ad_lookup_url)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_connection_error_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.ad_lookup_url, exception=ClientConnectionError('Failed'))

            response = await self.client.request('GET', self.get_support_centre_list_of_centres_postcode_valid_cy)

            self.assertLogEvent(cm, 'client failed to connect', url=self.ad_lookup_url)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_api_returns_404_en(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.ad_lookup_url, status=404)

            response = await self.client.request('GET', self.get_support_centre_list_of_centres_postcode_valid_en)

            self.assertLogEvent(cm, 'AD Lookup API returned as postcode not existing')

            self.assertEqual(response.status, 404)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_404_error_title_en, contents)
            self.assertIn(self.content_common_404_error_secondary_en, contents)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_api_returns_404_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.ad_lookup_url, status=404)

            response = await self.client.request('GET', self.get_support_centre_list_of_centres_postcode_valid_cy)

            self.assertLogEvent(cm, 'AD Lookup API returned as postcode not existing')

            self.assertEqual(response.status, 404)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_404_error_title_cy, contents)
            self.assertIn(self.content_common_404_error_secondary_cy, contents)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_api_returns_500_en(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.ad_lookup_url, status=500)

            response = await self.client.request('GET', self.get_support_centre_list_of_centres_postcode_valid_en)

            self.assertLogEvent(cm, 'AD Lookup API not responding')

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_support_centre_list_of_centres_api_returns_500_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.ad_lookup_url, status=500)

            response = await self.client.request('GET', self.get_support_centre_list_of_centres_postcode_valid_cy)

            self.assertLogEvent(cm, 'AD Lookup API not responding')

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)
