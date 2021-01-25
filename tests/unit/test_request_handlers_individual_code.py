from aiohttp.test_utils import unittest_run_loop
from .helpers import TestHelpers


# noinspection PyTypeChecker
class TestRequestHandlersIndividualCode(TestHelpers):

    user_journey = 'request'
    sub_user_journey = 'access-code'
    individual = True

    async def check_post_request_individual_code(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url)
            self.assertLogEvent(cm, self.build_url_log_entry('individual', display_region, 'POST', True))
            self.assertLogEvent(cm, 'no session - directing to enter address')
            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-address', display_region), contents)
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=False)

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_individual_code_confirm_send_by_text_en, 'en', 'HH', 'E', 'true')

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_individual_code_confirm_send_by_text_en, 'en', 'HH', 'W', 'true')

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_individual_code_confirm_send_by_text_cy, 'cy', 'HH', 'W', 'true')

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_individual_code_confirm_send_by_text_ni, 'ni', 'HH', 'N', 'true')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_no_results_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_individual_code_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_no_results_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_individual_code_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_no_results_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_individual_code_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_error(self):
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_en,
                                                          self.post_request_individual_code_enter_address_en, 'en', 500)
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_cy,
                                                          self.post_request_individual_code_enter_address_cy, 'cy', 500)
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_ni,
                                                          self.post_request_individual_code_enter_address_ni, 'ni', 500)
        await self.check_post_enter_address_error_503_from_ai(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_enter_address_error_503_from_ai(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_enter_address_error_503_from_ai(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_en,
                                                          self.post_request_individual_code_enter_address_en, 'en', 403)
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_cy,
                                                          self.post_request_individual_code_enter_address_cy, 'cy', 403)
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_ni,
                                                          self.post_request_individual_code_enter_address_ni, 'ni', 403)
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_en,
                                                          self.post_request_individual_code_enter_address_en, 'en', 401)
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_cy,
                                                          self.post_request_individual_code_enter_address_cy, 'cy', 401)
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_ni,
                                                          self.post_request_individual_code_enter_address_ni, 'ni', 401)
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_en,
                                                          self.post_request_individual_code_enter_address_en, 'en', 400)
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_cy,
                                                          self.post_request_individual_code_enter_address_cy, 'cy', 400)
        await self.check_post_enter_address_error_from_ai(self.get_request_individual_code_enter_address_ni,
                                                          self.post_request_individual_code_enter_address_ni, 'ni', 400)
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_individual_code_enter_address_en, 'en', epoch='test')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_individual_code_enter_address_cy, 'cy', epoch='test')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_individual_code_enter_address_ni, 'ni', epoch='test')

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_scotland_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(
            self.post_request_individual_code_select_address_en, 'en', 'HH', self.ai_uprn_result_scotland)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_individual_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_scotland_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(
            self.post_request_individual_code_select_address_cy, 'cy', 'HH', self.ai_uprn_result_scotland)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_individual_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_scotland_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_individual_code_select_address_ni, 'ni', 'HH', self.ai_uprn_result_scotland)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_individual_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_individual_code_address_not_found_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address_address_not_found(
            self.post_request_individual_code_select_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_individual_code_address_not_found_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address_address_not_found(
            self.post_request_individual_code_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_individual_code_address_not_found_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address_address_not_found(
            self.post_request_individual_code_select_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_individual_code_census_address_type_na_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en,
                                             'en', 'HH', self.ai_uprn_result_censusaddresstype_na)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_individual_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_individual_code_census_address_type_na_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy,
                                             'cy', 'HH', self.ai_uprn_result_censusaddresstype_na)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_individual_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_individual_code_census_address_type_na_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni,
                                             'ni', 'HH', self.ai_uprn_result_censusaddresstype_na_ni)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_individual_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_invalid_postcode_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address_input_invalid(self.post_request_individual_code_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_invalid_postcode_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address_input_invalid(self.post_request_individual_code_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_invalid_postcode_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address_input_invalid(self.post_request_individual_code_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_get_cases_error_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_individual_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_get_cases_error_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_individual_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_get_cases_error_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_individual_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_new_case_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e, 
            'individual', 'HH')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_new_case_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_new_case_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_new_case_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n, 
            'individual', 'HH')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_new_case_error_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_individual_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_new_case_error_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_individual_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_new_case_error_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_individual_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_no_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_no(self.post_request_individual_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_individual_confirm_address_data_no_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_no(self.post_request_individual_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_no_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_no(self.post_request_individual_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_en, 'en', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address_no_selection_made(
            self.post_request_individual_code_select_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address_no_selection_made(
            self.post_request_individual_code_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address_no_selection_made(
            self.post_request_individual_code_select_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_individual_code_select_how_to_receive_no_selection_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_individual_code_select_how_to_receive_en, 'en', self.common_form_data_empty, 
            'individual', 'HH')

    @unittest_run_loop
    async def test_post_request_individual_code_select_how_to_receive_no_selection_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_individual_code_select_how_to_receive_en, 'en', self.common_form_data_empty, 
            'individual', 'HH')

    @unittest_run_loop
    async def test_post_request_individual_code_select_how_to_receive_no_selection_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy', self.common_form_data_empty, 
            'individual', 'HH')

    @unittest_run_loop
    async def test_post_request_individual_code_select_how_to_receive_no_selection_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni', self.common_form_data_empty, 
            'individual', 'HH')

    @unittest_run_loop
    async def test_post_request_individual_code_select_how_to_receive_input_invalid_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_individual_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'HH')

    @unittest_run_loop
    async def test_post_request_individual_code_select_how_to_receive_input_invalid_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_individual_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'HH')

    @unittest_run_loop
    async def test_post_request_individual_code_select_how_to_receive_input_invalid_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'HH')

    @unittest_run_loop
    async def test_post_request_individual_code_select_how_to_receive_input_invalid_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'HH')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_mobile_invalid_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_invalid(self.post_request_individual_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_mobile_invalid_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_invalid(self.post_request_individual_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_mobile_invalid_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile_input_invalid(self.post_request_individual_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_individual_code_enter_mobile_invalid_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile_input_invalid(self.post_request_individual_code_enter_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_no_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_no(
            self.post_request_individual_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_no_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_no(
            self.post_request_individual_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_no_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_input_no(
            self.post_request_individual_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_no_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_input_no(
            self.post_request_individual_code_confirm_send_by_text_ni, 'ni')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_empty_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_empty_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_empty_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_empty_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_text_ni, 'ni',
            self.request_code_mobile_confirmation_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_invalid_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_invalid_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_invalid_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w, 
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_invalid_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_text_ni, 'ni',
            self.request_code_mobile_confirmation_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_get_fulfilment_error_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_en, 'en', 'HH', 'E', 'true')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_get_fulfilment_error_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_en, 'en', 'HH', 'W', 'true')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_get_fulfilment_error_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_cy, 'cy', 'HH', 'W', 'true')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_get_fulfilment_error_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_ni, 'ni', 'HH', 'N', 'true')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_request_fulfilment_error_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_request_fulfilment_error_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_request_fulfilment_error_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_request_fulfilment_error_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_ni, 'ni')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_request_fulfilment_error_429_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_request_fulfilment_error_429_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_request_fulfilment_error_429_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_text_request_fulfilment_error_429_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_text_ni, 'ni')

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_empty_hh_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_empty_hh_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_empty_hh_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_empty_hh_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_ni, 'ni',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_no_first_hh_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_no_first_hh_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_no_first_hh_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_no_first_hh_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_no_last_hh_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_no_last_hh_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_no_last_hh_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_no_last_hh_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_overlong_first_hh_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_overlong_first_hh_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_overlong_first_hh_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_overlong_first_hh_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_overlong_last_hh_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_overlong_last_hh_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_overlong_last_hh_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_individual_code_post_enter_name_overlong_last_hh_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_individual_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_empty_hh_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', self.common_form_data_empty,
            'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_empty_hh_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', self.common_form_data_empty,
            'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_empty_hh_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_cy, 'cy', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_post_cy, 'cy', self.common_form_data_empty,
            'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_empty_hh_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_ni, 'ni', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_post_ni, 'ni', self.common_form_data_empty,
            'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_invalid_hh_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_invalid_hh_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_invalid_hh_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_cy, 'cy', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_post_cy, 'cy',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_invalid_hh_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_ni, 'ni', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_individual_code_confirm_send_by_post_ni, 'ni',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_option_no_hh_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', 'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_option_no_hh_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', 'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_option_no_hh_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_cy, 'cy', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_individual_code_confirm_send_by_post_cy, 'cy', 'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_confirm_send_by_post_option_no_hh_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_ni, 'ni', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_individual_code_confirm_send_by_post_ni, 'ni', 'individual', 'HH')

    @unittest_run_loop
    async def test_request_individual_code_post_code_sent_post_hh_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', 'HH', 'UAC', 'E', 'true')

    @unittest_run_loop
    async def test_request_individual_code_post_code_sent_post_hh_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', 'HH', 'UAC', 'W', 'true')

    @unittest_run_loop
    async def test_request_individual_code_post_code_sent_post_hh_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_cy, 'cy', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_code_confirm_send_by_post_cy, 'cy', 'HH', 'UAC', 'W', 'true')

    @unittest_run_loop
    async def test_request_individual_code_post_code_sent_post_hh_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_ni, 'ni', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_code_confirm_send_by_post_ni, 'ni', 'HH', 'UAC', 'N', 'true')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_get_fulfilment_error_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', 'HH', 'E', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_get_fulfilment_error_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', 'HH', 'W', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_get_fulfilment_error_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_cy, 'cy', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_individual_code_confirm_send_by_post_cy, 'cy', 'HH', 'W', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_get_fulfilment_error_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_ni, 'ni', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_individual_code_confirm_send_by_post_ni, 'ni', 'HH', 'N', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_request_fulfilment_error_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_request_fulfilment_error_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_request_fulfilment_error_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_cy, 'cy', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_request_fulfilment_error_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_ni, 'ni', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_individual_code_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_request_fulfilment_error_429_ew_e(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_individual_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_request_fulfilment_error_429_ew_w(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_individual_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_individual_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_request_fulfilment_error_429_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_individual_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_cy, 'cy', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_individual_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_individual_code_confirm_send_by_post_request_fulfilment_error_429_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_individual_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_ni, 'ni', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_individual_code_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_northern_ireland_ew(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code(self.post_request_individual_code_en, 'en')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_en, 'en')
        await self.check_post_select_address(
            self.post_request_individual_code_select_address_en, 'en', 'HH', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_address_in_northern_ireland(
            self.post_request_individual_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_northern_ireland_cy(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code(self.post_request_individual_code_cy, 'cy')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_cy, 'cy')
        await self.check_post_select_address(
            self.post_request_individual_code_select_address_cy, 'cy', 'HH', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_address_in_northern_ireland(
            self.post_request_individual_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_northern_ireland_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_individual_code_select_address_ni, 'ni', 'HH', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_individual_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n,
            'individual', 'HH')

    @unittest_run_loop
    async def test_get_request_individual_code_address_not_in_northern_ireland_region_e_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_individual_code_select_address_ni, 'ni', 'HH', self.ai_uprn_result_england)
        await self.check_post_confirm_address_address_in_england(
            self.post_request_individual_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_individual_code_address_not_in_northern_ireland_region_w_ni(self):
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code(self.post_request_individual_code_ni, 'ni')
        await self.check_post_enter_address(self.post_request_individual_code_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_individual_code_select_address_ni, 'ni', 'HH', self.ai_uprn_result_wales)
        await self.check_post_confirm_address_address_in_wales(
            self.post_request_individual_code_confirm_address_ni, 'ni')
