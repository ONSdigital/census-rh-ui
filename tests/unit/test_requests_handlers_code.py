from unittest import mock

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from . import RHTestCase

attempts_retry_limit = 5


# noinspection PyTypeChecker
class TestRequestsHandlersAccessCode(RHTestCase):

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ew_e(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            post_enter_address_response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await post_enter_address_response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>', str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=E, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent/" lang="cy" >Cymraeg</a>', str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ew_w(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>', str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=W, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent/" lang="cy" >Cymraeg</a>', str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_cy(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/access-code/enter-address/" lang="en" >English</a>', contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/select-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>', str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=W, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/code-sent/" lang="en" >English</a>', str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ni(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=N, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_ew_e(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=SPG, region=E, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_ew_w(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=SPG, region=W, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_cy(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/access-code/enter-address/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/select-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=SPG, region=W, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/code-sent/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_ni(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=SPG, region=N, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_manager_ce_m_ew_e(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_title_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=E, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_manager_ce_m_ew_w(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_title_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=W, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_manager_ce_m_cy(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_title_cy, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_resident_cy, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_resident_cy, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_manager_cy, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_manager_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=W, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_manager_ce_m_ni(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_title_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=N, individual=false")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_ew_e(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_title_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=E, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_ew_w(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_title_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_resident_or_manager_en,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=W, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_cy(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/access-code/enter-address/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/select-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_title_cy, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_resident_cy, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_resident_cy, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_manager_cy, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_manager_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_resident_or_manager_cy,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=W, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/code-sent/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_ni(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_title_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, str(resp_content))
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_resident_or_manager_ni,
                    data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=N, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_ew_e(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=E, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_ew_w(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=W, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/code-sent/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_cy(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/access-code/enter-address/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/select-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=W, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/code-sent/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_ni(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=CE, region=N, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_ew(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/select-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/access-code/select-address/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_common_select_address_no_results_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_ew(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_with_epoch_ew(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_with_epoch_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_with_epoch_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_in_scotland_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/address-in-scotland/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_in_scotland_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/address-in-scotland/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_common_address_in_scotland_cy, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_in_scotland_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/call-contact-centre/address-not-found/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_not_listed_cy)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/call-contact-centre/address-not-found/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_census_address_type_na_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
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
    async def test_get_request_access_code_census_address_type_na_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
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
    async def test_get_request_access_code_census_address_type_na_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_change_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/call-contact-centre/address-not-found/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_change_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/call-contact-centre/address-not-found/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_change_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_ew(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('<a href="/cy/requests/access-code/enter-address/" lang="cy" >Cymraeg</a>',
                      contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_cy(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('<a href="/en/requests/access-code/enter-address/" lang="en" >English</a>',
                      contents)
        self.assertIn(self.content_request_enter_address_title_cy, contents)
        self.assertIn(self.content_common_enter_address_error_cy, contents)
        self.assertIn(self.content_request_enter_address_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_ni(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_ew(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_access_code_timeout_en)
        self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('<a href="/cy/requests/access-code/timeout/" lang="cy" >Cymraeg</a>',
                      contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_cy(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_access_code_timeout_cy)
        self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('<a href="/en/requests/access-code/timeout/" lang="en" >English</a>',
                      contents)
        self.assertIn(self.content_common_timeout_cy, contents)
        self.assertIn(self.content_request_timeout_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_ni(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_access_code_timeout_ni)
        self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_ni(self):
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

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_access_address_not_required_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'en/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/call-contact-centre/unable-to-match-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_access_address_not_required_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'cy/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/call-contact-centre/unable-to-match-address/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_contact_centre_cy, contents)

    @unittest_run_loop
    async def test_get_request_access_address_not_required_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'ni/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'en/requests/access-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'cy/requests/access-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/enter-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'ni/requests/access-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/select-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    def mock503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_invalid_ce_m_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_resident_or_manager_en,
                                                 data=self.common_resident_or_manager_input_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_resident_or_manager_title_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_invalid_ce_m_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_resident_or_manager_en,
                                                 data=self.common_resident_or_manager_input_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_resident_or_manager_title_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_invalid_ce_m_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_resident_or_manager_cy,
                                                 data=self.common_resident_or_manager_input_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_title_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_invalid_ce_m_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_resident_or_manager_ni,
                                                 data=self.common_resident_or_manager_input_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_resident_or_manager_title_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_resident_or_manager_en,
                                                 data=self.common_form_data_empty)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_resident_or_manager_title_en, contents)
            self.assertIn(self.content_common_resident_or_manager_error_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_resident_or_manager_en,
                                                 data=self.common_form_data_empty)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_resident_or_manager_title_en, contents)
            self.assertIn(self.content_common_resident_or_manager_error_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_resident_or_manager_cy,
                                                 data=self.common_form_data_empty)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_title_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_error_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_resident_or_manager_ni,
                                                 data=self.common_form_data_empty)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/resident-or-manager'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/resident-or-manager'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_resident_or_manager_title_en, contents)
            self.assertIn(self.content_common_resident_or_manager_error_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_cy,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_cy, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_ni,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_spg_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_spg_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_spg_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_cy,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_cy, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_spg_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_ni,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_m_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_m_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_m_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_cy,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_cy, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_m_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_ni,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_cy,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_enter_mobile_title_cy, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_access_code_enter_mobile_ni,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_hh_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_hh_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_spg_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_spg_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_r_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_r_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/enter-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_hh_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_hh_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_cy,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_ni,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_spg_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_spg_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_cy,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_ni,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_cy,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_ni,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_r_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_r_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_cy,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_ni,
                data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_hh_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_hh_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_cy,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_ni,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_spg_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_spg_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_cy,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_ni,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_m_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_m_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_cy,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_ni,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_r_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_r_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w

            await self.client.request('GET', self.get_request_access_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/access-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_cy,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/access-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_access_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_access_code_enter_mobile_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_access_code_confirm_mobile_ni,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_hh_ew_e(
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
                                    '?caseType=HH&region=E&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_hh_ew_w(
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
                                    '?caseType=HH&region=W&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_hh_cy(
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
                                    '?caseType=HH&region=W&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_hh_ni(
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
                                    '?caseType=HH&region=N&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_spg_ew_e(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=SPG&region=E&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_spg_ew_w(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=SPG&region=W&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_spg_cy(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=SPG&region=W&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_spg_ni(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=SPG&region=N&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_m_ew_e(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=CE&region=E&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_m_ew_w(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=CE&region=W&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_m_cy(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=CE&region=W&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_m_ni(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=CE&region=N&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_r_ew_e(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=CE&region=E&deliveryChannel=SMS&productGroup=UAC&individual=true',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_r_ew_w(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=CE&region=W&deliveryChannel=SMS&productGroup=UAC&individual=true',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_r_cy(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=CE&region=W&deliveryChannel=SMS&productGroup=UAC&individual=true',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_r_ni(
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
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=CE&region=N&deliveryChannel=SMS&productGroup=UAC&individual=true',
                                    status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_hh_ew_e(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_hh_ew_w(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_hh_cy(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_hh_ni(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_spg_ew_e(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_spg_ew_w(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_spg_cy(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_spg_ni(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_m_ew_e(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_m_ew_w(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_m_cy(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_m_ni(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_r_ew_e(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_r_ew_w(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_r_cy(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_r_ni(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)


# noinspection PyTypeChecker
class TestRequestsHandlersHouseholdCode(RHTestCase):

    @unittest_run_loop
    async def test_request_household_code_sms_happy_path_hh_ew_e(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_household_code_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_household_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_request_household_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_sms_happy_path_hh_ew_w(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_household_code_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_household_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_request_household_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_sms_happy_path_hh_cy(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_household_code_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_household_title_cy, contents)
            self.assertIn(self.content_request_secondary_cy, contents)

            response = await self.client.request('GET',
                                                 self.get_request_household_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_sms_happy_path_hh_ni(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_household_code_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_household_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_request_household_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_not_found_ew(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_en,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_not_found_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_cy,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_select_address_no_results_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_not_found_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_ni,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_ew(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_with_epoch_ew(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_with_epoch_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_with_epoch_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_in_scotland_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_in_scotland_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_address_in_scotland_cy, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_in_scotland_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_not_found_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_not_found_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_not_listed_cy)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_not_found_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_census_address_type_na_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'en/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_census_address_type_na_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'cy/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_census_address_type_na_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_change_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_change_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_change_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_bad_postcode_ew(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_en,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_bad_postcode_cy(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_household_code_cy)

            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_cy,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_request_enter_address_title_cy, contents)
        self.assertIn(self.content_common_enter_address_error_cy, contents)
        self.assertIn(self.content_request_enter_address_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_bad_postcode_ni(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_household_code_ni)

            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_ni,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_timeout_ew(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_household_code_timeout_en)
        self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_timeout_cy(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_household_code_timeout_cy)
        self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_timeout_cy, contents)
        self.assertIn(self.content_request_timeout_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_household_code_timeout_ni(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_household_code_timeout_ni)
        self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_get_cases_error_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_get_cases_error_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_get_cases_error_ni(self):
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

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_household_address_not_required_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'en/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_household_address_not_required_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'cy/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_contact_centre_cy, contents)

    @unittest_run_loop
    async def test_get_request_household_address_not_required_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'ni/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_no_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'en/requests/household-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_no_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'cy/requests/household-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_no_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'ni/requests/household-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_invalid_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_invalid_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_invalid_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_no_selection_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_select_address_no_selection_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'en/requests/household-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_select_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'cy/requests/household-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_select_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'ni/requests/household-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_500_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_500_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    def mock503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_503_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_503_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_403_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_403_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_403_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_401_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_401_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_400_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_400_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_400_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_mobile_invalid_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_household_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_mobile_invalid_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_household_code_enter_mobile_en,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_mobile_invalid_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_household_code_enter_mobile_cy,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_enter_mobile_title_cy, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_mobile_invalid_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            response = await self.client.request('POST', self.post_request_household_code_enter_mobile_ni,
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_no_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_no_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_no_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_household_code_cy)

            await self.client.request('GET', self.get_request_household_code_enter_address_cy)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_no_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_household_code_ni)

            await self.client.request('GET', self.get_request_household_code_enter_address_ni)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_empty_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_empty_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_empty_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_household_code_cy)

            await self.client.request('GET', self.get_request_household_code_enter_address_cy)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_empty_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_household_code_ni)

            await self.client.request('GET', self.get_request_household_code_enter_address_ni)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_invalid_ew_e(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_household_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_household_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_household_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_household_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_invalid_ew_w(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)

            await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_en,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_household_code_select_address_en,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_household_code_confirm_address_en,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_household_code_enter_mobile_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_household_code_confirm_mobile_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_invalid_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w

            await self.client.request('GET', self.get_request_household_code_cy)

            await self.client.request('GET', self.get_request_household_code_enter_address_cy)

            await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_household_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_household_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_household_code_enter_mobile_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_household_code_confirm_mobile_cy,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_invalid_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n

            await self.client.request('GET', self.get_request_household_code_ni)

            await self.client.request('GET', self.get_request_household_code_enter_address_ni)

            await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_household_code_select_address_ni,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_household_code_confirm_address_ni,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_household_code_enter_mobile_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_request_household_code_confirm_mobile_ni,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_get_fulfilment_error_ew_e(
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
                                    '?caseType=HH&region=E&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_get_fulfilment_error_ew_w(
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
                                    '?caseType=HH&region=W&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_get_fulfilment_error_cy(
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
                                    '?caseType=HH&region=W&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_get_fulfilment_error_ni(
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
                                    '?caseType=HH&region=N&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_request_fulfilment_error_ew_e(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_request_fulfilment_error_ew_w(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_request_fulfilment_error_cy(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_request_fulfilment_error_ni(
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)


# noinspection PyTypeChecker
class TestRequestsHandlersIndividualCode(RHTestCase):

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_ew_e(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/individual-code/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_individual_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/individual-code/enter-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=E, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/code-sent/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_ew_w(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/individual-code/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_individual_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/individual-code/enter-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/enter-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/confirm-mobile/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=W, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/code-sent/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_cy(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/individual-code/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_individual_title_cy, contents)
            self.assertIn(self.content_request_secondary_cy, contents)

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/individual-code/enter-address/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/select-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/confirm-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/enter-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/confirm-mobile/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=W, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/code-sent/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_ni(
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
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_individual_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "fulfilment query: case_type=HH, region=N, individual=true")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_not_found_ew(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_en,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/requests/individual-code/select-address/" lang="cy" >Cymraeg</a>',
                          contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_not_found_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_cy,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/requests/individual-code/select-address/" lang="en" >English</a>',
                          contents)
            self.assertIn(self.content_common_select_address_no_results_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_not_found_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_ni,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_ew(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_with_epoch_ew(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_with_epoch_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_with_epoch_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

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
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
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
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
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
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
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
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
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
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
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
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
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
    async def test_get_request_individual_code_confirm_address_data_change_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/call-contact-centre/address-not-found/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_change_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/call-contact-centre/address-not-found/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_change_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_bad_postcode_ew(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_en,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('<a href="/cy/requests/individual-code/enter-address/" lang="cy" >Cymraeg</a>',
                      contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_bad_postcode_cy(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_individual_code_cy)

            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_cy,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('<a href="/en/requests/individual-code/enter-address/" lang="en" >English</a>',
                      contents)
        self.assertIn(self.content_request_enter_address_title_cy, contents)
        self.assertIn(self.content_common_enter_address_error_cy, contents)
        self.assertIn(self.content_request_enter_address_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_bad_postcode_ni(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_individual_code_ni)

            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_ni,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

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
    async def test_get_request_individual_code_confirm_address_data_no_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'en/requests/individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/enter-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_confirm_address_data_no_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'cy/requests/individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/enter-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_request_enter_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_no_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'ni/requests/individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/confirm-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/confirm-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/confirm-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_ew(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'en/requests/individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('<a href="/cy/requests/individual-code/select-address/" lang="cy" >Cymraeg</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'cy/requests/individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('<a href="/en/requests/individual-code/select-address/" lang="en" >English</a>',
                          str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'ni/requests/individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_500_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_500_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    def mock503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_503_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_503_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_403_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_403_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_403_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_401_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_401_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_400_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_400_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_400_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

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
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

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
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

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
            self.assertIn(self.content_request_enter_mobile_title_cy, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_cy, contents)

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
            self.assertIn(self.content_request_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

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
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

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
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

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
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_cy,
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
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

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
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

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
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

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
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

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
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_cy,
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
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

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
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

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
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

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
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

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
                self.post_request_household_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_request_household_code_select_address_cy,
                data=self.common_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_request_household_code_confirm_address_cy,
                data=self.common_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_request_household_code_enter_mobile_cy,
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
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

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
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
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
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
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
