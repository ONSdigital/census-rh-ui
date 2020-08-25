from unittest import mock

from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from .helpers import TestHelpers

attempts_retry_limit = 5


# noinspection PyTypeChecker
class TestRequestsHandlersPaperForm(TestHelpers):

    user_journey = 'requests'
    sub_user_journey = 'paper-form'

    @unittest_run_loop
    async def test_post_request_paper_form_enter_address_empty_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address_input_empty(self.post_request_paper_form_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_paper_form_enter_address_empty_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address_input_empty(self.post_request_paper_form_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_paper_form_enter_address_empty_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address_input_empty(self.post_request_paper_form_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_paper_form_enter_address_invalid_postcode_en(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address_input_invalid(self.post_request_paper_form_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_paper_form_enter_address_invalid_postcode_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address_input_invalid(self.post_request_paper_form_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_paper_form_enter_address_invalid_postcode_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address_input_invalid(self.post_request_paper_form_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_paper_form_select_address_no_selection_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address_no_selection_made(self.post_request_paper_form_select_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_paper_form_select_address_no_selection_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address_no_selection_made(self.post_request_paper_form_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_paper_form_select_address_no_selection_ni(
            self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address_no_selection_made(self.post_request_paper_form_select_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_paper_form_enter_address_no_results_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_paper_form_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_paper_form_enter_address_no_results_cy(
            self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_paper_form_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_paper_form_enter_address_no_results_ni(
            self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_paper_form_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_no_selection_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_address_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_no_selection_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_no_selection_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_get_cases_error_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_paper_form_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_get_cases_error_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_paper_form_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_get_cases_error_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_paper_form_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_data_no_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_no(self.post_request_paper_form_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_data_no_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_no(self.post_request_paper_form_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_data_no_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_no(self.post_request_paper_form_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_data_invalid_ew(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request('POST',
                                                 self.post_request_paper_form_confirm_address_en,
                                                 data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "address confirmation error")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_data_invalid_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request('POST',
                                                 self.post_request_paper_form_confirm_address_cy,
                                                 data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "address confirmation error")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_data_invalid_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request('POST',
                                                 self.post_request_paper_form_confirm_address_ni,
                                                 data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "address confirmation error")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_scotland_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('POST',
                                      self.post_request_paper_form_enter_address_en,
                                      data=self.common_postcode_input_valid)

            await self.client.request('POST',
                                      self.post_request_paper_form_select_address_en,
                                      data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/address-in-scotland/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_scotland_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('POST',
                                      self.post_request_paper_form_enter_address_cy,
                                      data=self.common_postcode_input_valid)

            await self.client.request('POST',
                                      self.post_request_paper_form_select_address_cy,
                                      data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/address-in-scotland/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_common_address_in_scotland_cy, contents)

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_scotland_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_paper_form_address_not_found_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/call-contact-centre/address-not-found/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_paper_form_address_not_found_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_not_listed_cy)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/call-contact-centre/address-not-found/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, contents)

    @unittest_run_loop
    async def test_get_request_paper_form_address_not_found_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_paper_form_census_address_type_na_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'en/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/call-contact-centre/unable-to-match-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_paper_form_census_address_type_na_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'cy/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/call-contact-centre/unable-to-match-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_paper_form_census_address_type_na_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_paper_form_timeout_ew(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_paper_form_timeout_en)
        self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('<a href="/cy/requests/paper-form/timeout/" lang="cy" >Cymraeg</a>',
                      contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_paper_form_timeout_cy(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_paper_form_timeout_cy)
        self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('<a href="/en/requests/paper-form/timeout/" lang="en" >English</a>',
                      contents)
        self.assertIn(self.content_common_timeout_cy, contents)
        self.assertIn(self.content_request_timeout_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_paper_form_timeout_ni(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_paper_form_timeout_ni)
        self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_paper_form_address_not_required_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'en/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/call-contact-centre/unable-to-match-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_paper_form_address_not_required_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'cy/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/call-contact-centre/unable-to-match-address/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_contact_centre_cy, contents)

    @unittest_run_loop
    async def test_get_request_paper_form_address_not_required_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'ni/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_empty_ce_m_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e

            await self.client.request(
                'POST',
                self.post_request_paper_form_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_select_address_en,
                data=self.common_select_address_input_valid)

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/paper-form/resident-or-manager/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_common_resident_or_manager_title_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, contents)

            response = await self.client.request('POST', self.post_request_paper_form_resident_or_manager_en,
                                                 data=self.common_form_data_empty)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_resident_or_manager_error_en, contents)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_empty_ce_m_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request(
                'POST',
                self.post_request_paper_form_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_select_address_en,
                data=self.common_select_address_input_valid)

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/paper-form/resident-or-manager/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_common_resident_or_manager_title_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, contents)

            response = await self.client.request('POST', self.post_request_paper_form_resident_or_manager_en,
                                                 data=self.common_form_data_empty)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_resident_or_manager_error_en, contents)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_empty_ce_m_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request(
                'POST',
                self.post_request_paper_form_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_select_address_cy,
                data=self.common_select_address_input_valid)

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/paper-form/resident-or-manager/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_common_resident_or_manager_title_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_cy, contents)

            response = await self.client.request('POST', self.post_request_paper_form_resident_or_manager_cy,
                                                 data=self.common_form_data_empty)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_resident_or_manager_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_empty_ce_m_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n

            await self.client.request(
                'POST',
                self.post_request_paper_form_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_select_address_ni,
                data=self.common_select_address_input_valid)

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_resident_or_manager_title_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, contents)

            response = await self.client.request('POST', self.post_request_paper_form_resident_or_manager_ni,
                                                 data=self.common_form_data_empty)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_resident_or_manager_error_en, contents)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_invalid_ce_m_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e

            await self.client.request(
                'POST',
                self.post_request_paper_form_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_paper_form_resident_or_manager_en,
                                                 data=self.common_resident_or_manager_input_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_resident_or_manager_error_en, contents)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_invalid_ce_m_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request(
                'POST',
                self.post_request_paper_form_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_paper_form_resident_or_manager_en,
                                                 data=self.common_resident_or_manager_input_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_resident_or_manager_error_en, contents)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_invalid_ce_m_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request(
                'POST',
                self.post_request_paper_form_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_paper_form_resident_or_manager_cy,
                                                 data=self.common_resident_or_manager_input_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_resident_or_manager_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_invalid_ce_m_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n

            await self.client.request(
                'POST',
                self.post_request_paper_form_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_paper_form_resident_or_manager_ni,
                                                 data=self.common_resident_or_manager_input_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_resident_or_manager_error_en, contents)

    @unittest_run_loop
    async def test_post_request_paper_form_get_ai_postcode_error(self):
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_en, 'en', 500)
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_cy, 'cy', 500)
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_ni, 'ni', 500)
        await self.check_post_enter_address_error_503_from_ai(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address_error_503_from_ai(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address_error_503_from_ai(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_en, 'en', 403)
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_cy, 'cy', 403)
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_ni, 'ni', 403)
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_en, 'en', 401)
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_cy, 'cy', 401)
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_ni, 'ni', 401)
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_en, 'en', 400)
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_cy, 'cy', 400)
        await self.check_post_enter_address_error_from_ai(self.post_request_paper_form_enter_address_ni, 'ni', 400)
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_form_enter_address_en, 'en', epoch='test')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_form_enter_address_cy, 'cy', epoch='test')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_form_enter_address_ni, 'ni', epoch='test')

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_hh_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_hh_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_spg_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_spg_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_select_resident_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_select_resident_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_select_resident_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_select_resident_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_ce_r_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_ce_r_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_hh_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_hh_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_spg_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_spg_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_select_resident_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_select_resident_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_select_resident_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_select_resident_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_ce_r_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_ce_r_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_no_first)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertNotIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_hh_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_hh_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_spg_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_spg_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_select_resident_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_select_resident_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_select_resident_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_select_resident_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_ce_r_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_ce_r_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/enter-name/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/enter-name/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_cy, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_no_last)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertNotIn(self.content_request_common_enter_name_error_first_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_error_last_name_en, str(resp_content))
            self.assertIn(self.content_request_common_enter_name_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_hh_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_hh_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_spg_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_spg_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_select_resident_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_select_resident_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_select_resident_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_select_resident_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_ce_r_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_ce_r_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_hh_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_hh_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_spg_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_spg_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_select_resident_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_select_resident_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_select_resident_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_select_resident_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_ce_r_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_ce_r_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.request_common_confirm_name_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_common_confirm_name_address_error_en, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_hh_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/request-cancelled/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_hh_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/request-cancelled/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/request-cancelled/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_spg_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/request-cancelled/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_spg_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/request-cancelled/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/request-cancelled/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_select_resident_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/request-cancelled/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_select_resident_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/request-cancelled/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_select_resident_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/request-cancelled/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_select_resident_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_ce_r_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/request-cancelled/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_ce_r_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_en,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/confirm-name-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_en,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/paper-form/request-cancelled/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_cy,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/confirm-name-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_cy, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_cy,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/paper-form/request-cancelled/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-name'")

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_enter_name_ni,
                data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-name-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_confirm_name_address_title_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_request_paper_form_confirm_name_address_ni,
                data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/request-cancelled'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_form_request_cancelled_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_hh_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=HH&region=E&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=false',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_hh_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=HH&region=W&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=false',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=HH&region=W&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=false',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_cy,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=HH&region=N&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=false',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_ni,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_spg_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=SPG&region=E&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=false',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_spg_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=SPG&region=W&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=false',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=SPG&region=W&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=false',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_cy,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=SPG&region=N&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=false',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_ni,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_select_resident_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=CE&region=E&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=true',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_select_resident_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=CE&region=W&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=true',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_select_resident_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=CE&region=W&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=true',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_resident)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_cy,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_select_resident_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=CE&region=N&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=true',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_resident)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_ni,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_ce_r_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=CE&region=E&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=true',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_ce_r_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=CE&region=W&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=true',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=CE&region=W&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=true',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_cy,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n
            mocked_aioresponses.get(
                self.rhsvc_url_fulfilments +
                '?caseType=CE&region=N&deliveryChannel=POST&productGroup=QUESTIONNAIRE&individual=true',
                status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_ni,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_hh_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_hh_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_cy,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_ni,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_spg_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_spg_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_cy,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_ni,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_select_resident_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_resident)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_select_resident_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_resident)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_select_resident_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_resident)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_cy,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_select_resident_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_resident)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_ni,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_ce_r_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_ce_r_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_cy,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_cy,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_name_ni,
                    data=self.request_common_enter_name_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_name_address_ni,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-name-address'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'HH', 'QUESTIONNAIRE', 'E', 'false')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'HH', 'QUESTIONNAIRE', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'HH', 'QUESTIONNAIRE', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'HH', 'QUESTIONNAIRE', 'N', 'false')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'SPG', 'QUESTIONNAIRE', 'E', 'false')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'SPG', 'QUESTIONNAIRE', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'SPG', 'QUESTIONNAIRE', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'SPG', 'QUESTIONNAIRE', 'N', 'false')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form(self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'QUESTIONNAIRE', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form(self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form(self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form(self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'CE', 'QUESTIONNAIRE', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'QUESTIONNAIRE', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_code_sent_post_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'CE', 'QUESTIONNAIRE', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/form-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn('<a href="/cy/requests/paper-form/form-manager/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_manager_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_select_manager_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/form-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn('<a href="/cy/requests/paper-form/form-manager/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_manager_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_select_manager_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/form-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn('<a href="/en/requests/paper-form/form-manager/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_form_manager_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_select_manager_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            response = await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/form-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.content_request_form_manager_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_sms_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_sms
            mocked_request_fulfilment_sms.return_value = self.rhsvc_request_fulfilment_sms

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/form-manager'")

            await self.client.request('GET', self.get_request_access_code_select_method_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-method'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_method_en,
                    data=self.request_code_select_method_data_sms)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-method'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=E, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent-sms'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent-sms/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_title_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_secondary_manager_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_sms_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_sms
            mocked_request_fulfilment_sms.return_value = self.rhsvc_request_fulfilment_sms

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/form-manager'")

            await self.client.request('GET', self.get_request_access_code_select_method_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-method'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_method_en,
                    data=self.request_code_select_method_data_sms)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-method'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=W, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent-sms'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent-sms/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_title_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_secondary_manager_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_sms_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_sms
            mocked_request_fulfilment_sms.return_value = self.rhsvc_request_fulfilment_sms

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/form-manager'")

            await self.client.request('GET', self.get_request_access_code_select_method_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-method'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_method_cy,
                    data=self.request_code_select_method_data_sms)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-method'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-mobile'")

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=W, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/code-sent-sms'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/code-sent-sms/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_title_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_secondary_manager_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_sms_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_sms
            mocked_request_fulfilment_sms.return_value = self.rhsvc_request_fulfilment_sms

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/form-manager'")

            await self.client.request('GET', self.get_request_access_code_select_method_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-method'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_method_ni,
                    data=self.request_code_select_method_data_sms)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-method'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-mobile'")

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=N, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/code-sent-sms'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_title_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_secondary_manager_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_post_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/form-manager'")

            await self.client.request('GET', self.get_request_access_code_select_method_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-method'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-method'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_method_en,
                    data=self.request_code_select_method_data_post)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-method'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-name'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-name-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-name-address'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, fulfilment_type=UAC, region=E, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent-post'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent-post/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_post_title_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_post_secondary_manager_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_post_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/paper-form/form-manager'")

            await self.client.request('GET', self.get_request_access_code_select_method_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-method'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_method_en,
                    data=self.request_code_select_method_data_post)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-method'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-name'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_name_en,
                    data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-name-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_name_address_en,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-name-address'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, fulfilment_type=UAC, region=W, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent-post'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent-post/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_post_title_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_post_secondary_manager_en, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_post_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/paper-form/form-manager'")

            await self.client.request('GET', self.get_request_access_code_select_method_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-method'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_method_cy,
                    data=self.request_code_select_method_data_post)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-method'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-name'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_name_cy,
                    data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-name-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_name_address_cy,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-name-address'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, fulfilment_type=UAC, region=W, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/code-sent-post'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/code-sent-post/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_post_title_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_post_secondary_manager_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_post_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_post'
        ) as mocked_request_fulfilment_post:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            await self.client.request('GET', self.get_request_paper_form_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/enter-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/select-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/confirm-address'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/resident-or-manager'")

            await self.client.request(
                    'POST',
                    self.post_request_paper_form_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/paper-form/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/paper-form/form-manager'")

            await self.client.request('GET', self.get_request_access_code_select_method_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-method'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_method_ni,
                    data=self.request_code_select_method_data_post)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-method'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-name'")

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_name_ni,
                    data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-name'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-name-address'")

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_name_address_ni,
                    data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-name-address'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, fulfilment_type=UAC, region=N, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/code-sent-post'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_post_title_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_post_secondary_manager_en, str(resp_content))
