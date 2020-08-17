from unittest import mock

from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from .helpers import TestHelpers

attempts_retry_limit = 5


# noinspection PyTypeChecker
class TestRequestsHandlersIndividualCode(TestHelpers):

    user_journey = 'requests'
    sub_user_journey = 'individual-code'

    async def get_request_individual_code(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey)
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/" '
                              'lang="en" >English</a>', contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_individual_title_cy, contents)
                self.assertIn(self.content_request_secondary_cy, contents)
            else:
                self.assertIn(self.content_request_individual_title_en, contents)
                self.assertIn(self.content_request_secondary_en, contents)

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_ew_e(self):
        await self.get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_en, 'en')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.post_common_select_address(self.post_request_individual_code_select_address_en, 'en')
        await self.post_common_confirm_address_yes(self.post_request_individual_code_confirm_address_en,
                                                   'en', self.rhsvc_case_by_uprn_hh_e)
        await self.post_common_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en')

        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_sms
            mocked_request_fulfilment_sms.return_value = self.rhsvc_request_fulfilment_sms

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=E, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/code-sent-sms'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/code-sent-sms/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_title_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_secondary_individual_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_ew_w(self):
        await self.get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_en, 'en')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.post_common_select_address(self.post_request_individual_code_select_address_en, 'en')
        await self.post_common_confirm_address_yes(self.post_request_individual_code_confirm_address_en,
                                                   'en', self.rhsvc_case_by_uprn_hh_w)
        await self.post_common_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en')

        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_sms
            mocked_request_fulfilment_sms.return_value = self.rhsvc_request_fulfilment_sms

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=W, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/code-sent-sms'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/code-sent-sms/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_title_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_secondary_individual_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_cy(self):
        await self.get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_select_address(self.post_request_individual_code_select_address_cy, 'cy')
        await self.post_common_confirm_address_yes(self.post_request_individual_code_confirm_address_cy,
                                                   'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.post_common_enter_mobile(self.post_request_individual_code_enter_mobile_cy, 'cy')

        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_sms
            mocked_request_fulfilment_sms.return_value = self.rhsvc_request_fulfilment_sms

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=W, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/code-sent-sms'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/code-sent-sms/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_title_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_secondary_individual_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_ni(self):
        await self.get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_select_address(self.post_request_individual_code_select_address_ni, 'ni')
        await self.post_common_confirm_address_yes(self.post_request_individual_code_confirm_address_ni,
                                                   'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.post_common_enter_mobile(self.post_request_individual_code_enter_mobile_ni, 'ni')

        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_sms
            mocked_request_fulfilment_sms.return_value = self.rhsvc_request_fulfilment_sms

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=N, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/code-sent-sms'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_title_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_sms_secondary_individual_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_no_results_ew(self):
        await self.get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_en, 'en')
        await self.post_common_enter_address_no_results(self.post_request_individual_code_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_no_results_cy(self):
        await self.get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_enter_address_no_results(self.post_request_individual_code_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_no_results_ni(self):
        await self.get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_enter_address_no_results(self.post_request_individual_code_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_error(self):
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_en, 'en', 500)
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_cy, 'cy', 500)
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_ni, 'ni', 500)
        await self.post_common_enter_address_ai_error_503(self.post_request_individual_code_enter_address_en, 'en')
        await self.post_common_enter_address_ai_error_503(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_enter_address_ai_error_503(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_en, 'en', 403)
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_cy, 'cy', 403)
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_ni, 'ni', 403)
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_en, 'en', 401)
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_cy, 'cy', 401)
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_ni, 'ni', 401)
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_en, 'en', 400)
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_cy, 'cy', 400)
        await self.post_common_enter_address_ai_error(self.post_request_individual_code_enter_address_ni, 'ni', 400)
        await self.post_common_enter_address_ai_connection_error(
            self.post_request_individual_code_enter_address_en, 'en')
        await self.post_common_enter_address_ai_connection_error(
            self.post_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_enter_address_ai_connection_error(
            self.post_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_enter_address_ai_connection_error(
            self.post_request_individual_code_enter_address_en, 'en', epoch='test')
        await self.post_common_enter_address_ai_connection_error(
            self.post_request_individual_code_enter_address_cy, 'cy', epoch='test')
        await self.post_common_enter_address_ai_connection_error(
            self.post_request_individual_code_enter_address_ni, 'ni', epoch='test')

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_scotland_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/address-in-scotland/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_scotland_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/address-in-scotland/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_common_address_in_scotland_cy, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_scotland_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_address_not_found_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/call-contact-centre/address-not-found/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_address_not_found_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_not_listed_cy)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/call-contact-centre/address-not-found/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_address_not_found_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_census_address_type_na_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
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
    async def test_get_request_individual_code_census_address_type_na_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
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
    async def test_get_request_individual_code_census_address_type_na_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_invalid_postcode_ew(self):
        await self.get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_en, 'en')
        await self.post_common_enter_address_invalid(self.post_request_individual_code_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_invalid_postcode_cy(self):
        await self.get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_enter_address_invalid(self.post_request_individual_code_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_invalid_postcode_ni(self):
        await self.get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_enter_address_invalid(self.post_request_individual_code_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_individual_code_timeout_ew(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_timeout_en)
        self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('<a href="/cy/requests/individual-code/timeout/" lang="cy" >Cymraeg</a>',
                      contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_timeout_cy(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_timeout_cy)
        self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('<a href="/en/requests/individual-code/timeout/" lang="en" >English</a>',
                      contents)
        self.assertIn(self.content_common_timeout_cy, contents)
        self.assertIn(self.content_request_timeout_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_timeout_ni(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_timeout_ni)
        self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_get_cases_error_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_get_cases_error_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_get_cases_error_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_address_not_required_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'en/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/call-contact-centre/unable-to-match-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_address_not_required_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'cy/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/call-contact-centre/unable-to-match-address/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_contact_centre_cy, contents)

    @unittest_run_loop
    async def test_get_request_individual_address_not_required_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'ni/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_no_ew(self):
        await self.get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_en, 'en')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.post_common_select_address(self.post_request_individual_code_select_address_en, 'en')
        await self.post_common_confirm_address_no(self.post_request_individual_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_individual_confirm_address_data_no_cy(self):
        await self.get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_select_address(self.post_request_individual_code_select_address_cy, 'cy')
        await self.post_common_confirm_address_no(self.post_request_individual_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_no_ni(self):
        await self.get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_select_address(self.post_request_individual_code_select_address_ni, 'ni')
        await self.post_common_confirm_address_no(self.post_request_individual_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_ew(self):
        await self.get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_en, 'en')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.post_common_select_address(self.post_request_individual_code_select_address_en, 'en')
        await self.post_common_confirm_address_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_en, 'en', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_cy(self):
        await self.get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_select_address(self.post_request_individual_code_select_address_cy, 'cy')
        await self.post_common_confirm_address_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_ni(self):
        await self.get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_select_address(self.post_request_individual_code_select_address_ni, 'ni')
        await self.post_common_confirm_address_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_ew(self):
        await self.get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_en, 'en')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.post_common_select_address(self.post_request_individual_code_select_address_en, 'en')
        await self.post_common_confirm_address_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_cy(self):
        await self.get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_select_address(self.post_request_individual_code_select_address_cy, 'cy')
        await self.post_common_confirm_address_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_ni(self):
        await self.get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_select_address(self.post_request_individual_code_select_address_ni, 'ni')
        await self.post_common_confirm_address_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_ew(self):
        await self.get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_en, 'en')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.post_common_select_address_empty(self.post_request_individual_code_select_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_cy(self):
        await self.get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.post_common_select_address_empty(self.post_request_individual_code_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_ni(self):
        await self.get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.get_common_enter_address(self.get_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.post_common_select_address_empty(self.post_request_individual_code_select_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_mobile_invalid_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_individual_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/individual-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_code_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_code_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_enter_mobile_invalid_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_individual_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/individual-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_code_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_code_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_enter_mobile_invalid_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_individual_code_enter_mobile_cy,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/individual-code/enter-mobile/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_code_enter_mobile_title_cy, contents)
            self.assertIn(self.content_request_code_enter_mobile_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_enter_mobile_invalid_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_individual_code_enter_mobile_ni,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_code_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_code_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_no_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_code_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_no_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_code_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_no_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_individual_code_cy)

            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/enter-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_code_enter_mobile_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_no_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_individual_code_ni)

            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_code_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_empty_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_empty_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_empty_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_individual_code_cy)

            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_empty_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_individual_code_ni)

            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_invalid_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_individual_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_individual_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_individual_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_invalid_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_individual_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_individual_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_individual_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_invalid_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_individual_code_cy)

            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_individual_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_individual_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_individual_code_enter_mobile_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_confirm_mobile_cy,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_invalid_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_individual_code_ni)

            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_individual_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_individual_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_individual_code_enter_mobile_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_confirm_mobile_ni,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_code_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_get_fulfilment_error_ew_e(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=E&deliveryChannel=SMS&productGroup=UAC&individual=true',
                                    status=400)

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_get_fulfilment_error_ew_w(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=W&deliveryChannel=SMS&productGroup=UAC&individual=true',
                                    status=400)

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_get_fulfilment_error_cy(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=W&deliveryChannel=SMS&productGroup=UAC&individual=true',
                                    status=400)

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_get_fulfilment_error_ni(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=N&deliveryChannel=SMS&productGroup=UAC&individual=true',
                                    status=400)

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_request_fulfilment_error_ew_e(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_sms
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_request_fulfilment_error_ew_w(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_sms
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_request_fulfilment_error_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_sms
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_request_fulfilment_error_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
                'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_sms
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)
