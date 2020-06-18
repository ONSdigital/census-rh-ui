from unittest import mock

from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from . import RHTestCase

attempts_retry_limit = 5


# noinspection PyTypeChecker
class TestRequestsHandlers(RHTestCase):

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_en(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_request_household_code_enter_mobile_en,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn(self.content_request_enter_mobile_title_en, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_cy(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_request_household_code_enter_mobile_cy,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn(self.content_request_enter_mobile_title_cy, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ni(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_request_household_code_enter_mobile_ni,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn(self.content_request_enter_mobile_title_en, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hi_en(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_request_individual_code_enter_mobile_en,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn(self.content_request_enter_mobile_title_en, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hi_cy(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_request_individual_code_enter_mobile_cy,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn(self.content_request_enter_mobile_title_cy, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hi_ni(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_request_individual_code_enter_mobile_ni,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn(self.content_request_enter_mobile_title_en, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_request_household_code_confirm_mobile_no_en(
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
    async def test_request_individual_code_confirm_mobile_no_en(
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
    async def test_request_household_code_confirm_mobile_empty_en(
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
    async def test_request_individual_code_confirm_mobile_empty_en(
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
    async def test_request_household_code_confirm_mobile_invalid_en(
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
    async def test_request_individual_code_confirm_mobile_invalid_en(
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
    async def test_request_household_code_confirm_mobile_get_fulfilment_error_en(
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
    async def test_request_individual_code_confirm_mobile_get_fulfilment_error_en(
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
    async def test_request_household_code_confirm_mobile_request_fulfilment_error_en(
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

    @unittest_run_loop
    async def test_request_individual_code_confirm_mobile_request_fulfilment_error_en(
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
