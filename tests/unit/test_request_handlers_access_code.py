from aiohttp.test_utils import unittest_run_loop
from .helpers import TestHelpers


# noinspection PyTypeChecker
class TestRequestHandlersAccessCode(TestHelpers):

    user_journey = 'request'
    sub_user_journey = 'access-code'

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'HH', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni', 'HH', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'SPG', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'SPG', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'SPG', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'manager')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'CE', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni', 'CE', 'N', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni', 'CE', 'N', 'true')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_no_results_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_access_code_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_no_results_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_access_code_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_no_results_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_access_code_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_error(self):
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_en,
                                                          self.post_request_access_code_enter_address_en, 'en', 500)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_cy,
                                                          self.post_request_access_code_enter_address_cy, 'cy', 500)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_ni,
                                                          self.post_request_access_code_enter_address_ni, 'ni', 500)
        await self.check_post_enter_address_error_503_from_ai(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address_error_503_from_ai(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address_error_503_from_ai(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_en,
                                                          self.post_request_access_code_enter_address_en, 'en', 403)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_cy,
                                                          self.post_request_access_code_enter_address_cy, 'cy', 403)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_ni,
                                                          self.post_request_access_code_enter_address_ni, 'ni', 403)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_en,
                                                          self.post_request_access_code_enter_address_en, 'en', 401)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_cy,
                                                          self.post_request_access_code_enter_address_cy, 'cy', 401)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_ni,
                                                          self.post_request_access_code_enter_address_ni, 'ni', 401)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_en,
                                                          self.post_request_access_code_enter_address_en, 'en', 400)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_cy,
                                                          self.post_request_access_code_enter_address_cy, 'cy', 400)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_ni,
                                                          self.post_request_access_code_enter_address_ni, 'ni', 400)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_en,
                                                          self.post_request_access_code_enter_address_en, 'en', 429)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_cy,
                                                          self.post_request_access_code_enter_address_cy, 'cy', 429)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_ni,
                                                          self.post_request_access_code_enter_address_ni, 'ni', 429)
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_access_code_enter_address_en, 'en', epoch='test')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_access_code_enter_address_cy, 'cy', epoch='test')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_access_code_enter_address_ni, 'ni', epoch='test')

    @unittest_run_loop
    async def test_get_request_access_code_address_in_scotland_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case(
            self.post_request_access_code_select_address_en, 'en', 'HH', scotland=True)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_access_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_access_code_address_in_scotland_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_no_case(
            self.post_request_access_code_select_address_cy, 'cy', 'HH', scotland=True)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_access_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_address_in_scotland_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address_no_case(
            self.post_request_access_code_select_address_ni, 'ni', 'HH', scotland=True)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_access_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_address_not_found(
            self.post_request_access_code_select_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_address_not_found(
            self.post_request_access_code_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address_address_not_found(
            self.post_request_access_code_select_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_access_code_sms_census_address_type_na_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case_aims_addresstype_na(
            self.post_request_access_code_select_address_en, 'en', 'E')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'HH', 'E', 'false')

    @unittest_run_loop
    async def test_get_request_access_code_sms_census_address_type_na_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case_aims_addresstype_na(
            self.post_request_access_code_select_address_en, 'en', 'W')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_get_request_access_code_sms_census_address_type_na_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_no_case_aims_addresstype_na(
            self.post_request_access_code_select_address_cy, 'cy', 'W')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_get_request_access_code_sms_census_address_type_na_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address_no_case_aims_addresstype_na(
            self.post_request_access_code_select_address_ni, 'ni', 'N')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni', 'HH', 'N', 'false')

    @unittest_run_loop
    async def test_get_request_access_code_form_census_address_type_na_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case_aims_addresstype_na(
            self.post_request_access_code_select_address_en, 'en', 'E')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'HH', 'UAC', 'E', 'false',
            check_address_was_na=True)

    @unittest_run_loop
    async def test_get_request_access_code_form_census_address_type_na_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case_aims_addresstype_na(
            self.post_request_access_code_select_address_en, 'en', 'W')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'HH', 'UAC', 'W', 'false',
            check_address_was_na=True)

    @unittest_run_loop
    async def test_get_request_access_code_form_census_address_type_na_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_no_case_aims_addresstype_na(
            self.post_request_access_code_select_address_cy, 'cy', 'W')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'HH', 'UAC', 'W', 'false',
            check_address_was_na=True)

    @unittest_run_loop
    async def test_get_request_access_code_form_census_address_type_na_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address_no_case_aims_addresstype_na(
            self.post_request_access_code_select_address_ni, 'ni', 'N')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'HH', 'UAC', 'N', 'false',
            check_address_was_na=True)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_invalid_postcode_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address_input_invalid(self.post_request_access_code_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_invalid_postcode_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address_input_invalid(self.post_request_access_code_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_invalid_postcode_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address_input_invalid(self.post_request_access_code_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_error_from_get_cases(self.post_request_access_code_select_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_error_from_get_cases(self.post_request_access_code_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address_error_from_get_cases(self.post_request_access_code_select_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_code_new_case_individual(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual', 'CE')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_code_new_case_individual(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual', 'CE')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_code_new_case_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual', 'CE')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_code_new_case_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual', 'CE')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_error_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_access_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_error_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_access_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_new_case_error_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_access_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_no(self.post_request_access_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_individual_confirm_address_data_no_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_no(self.post_request_access_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_no(self.post_request_access_code_confirm_address_ni, 'ni')

    # CR-1818 ensure attributes cleared when trying new address.
    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_where_user_changes_address(self):
        # asks for address which is in RHSvc, but then rejects it to go round again
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_no(self.post_request_access_code_confirm_address_en, 'en')

        # back round again, but this time confirms address
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_case(self.post_request_access_code_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_code_new_case(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_en, 'en', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_cy, 'cy', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_ni, 'ni', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_ni, 'ni', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_selection_made(
            self.post_request_access_code_select_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_no_selection_made(
            self.post_request_access_code_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address_no_selection_made(
            self.post_request_access_code_select_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_invalid_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_en, 'en', self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_invalid_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_en, 'en', self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_invalid_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_cy, 'cy', self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_invalid_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_ni, 'ni', self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_ni, 'ni', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty,
            'household', 'HH')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty,
            'household', 'HH')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy', self.common_form_data_empty,
            'household', 'HH')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_ni, 'ni', self.common_form_data_empty,
            'household', 'HH')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty,
            'household', 'SPG')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty,
            'household', 'SPG')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy', self.common_form_data_empty,
            'household', 'SPG')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty, 'manager', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty, 'manager', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy', self.common_form_data_empty, 'manager', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_ni, 'ni', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_ni, 'ni', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy',
            self.request_code_select_how_to_receive_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_ni, 'ni',
            self.request_code_select_how_to_receive_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'household', 'SPG')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'household', 'SPG')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy',
            self.request_code_select_how_to_receive_data_invalid, 'household', 'SPG')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'manager', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'manager', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy',
            self.request_code_select_how_to_receive_data_invalid, 'manager', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_ni, 'ni',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_ni, 'ni',
            self.request_code_select_how_to_receive_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'household')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'manager')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni',
            self.request_code_mobile_confirmation_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'manager')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'manager')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'manager')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_empty, 'manager')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni',
            self.request_code_mobile_confirmation_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni',
            self.request_code_mobile_confirmation_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'manager')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'manager')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'manager')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_invalid, 'manager')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni',
            self.request_code_mobile_confirmation_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'HH', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'household')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni', 'HH', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'SPG', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'SPG', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'SPG', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'manager')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'CE', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni', 'CE', 'N', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni', 'CE', 'N', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'household')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'manager')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_texte_request_fulfilment_error_429_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'household')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'manager')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'manager')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_select_resident_ce_m_ew_e(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_select_resident_ce_m_ew_w(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni', 'individual')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty, 'household', 'HH')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty, 'household', 'HH')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', self.common_form_data_empty, 'household', 'HH')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', self.common_form_data_empty, 'household', 'HH')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty,
            'household', 'SPG')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty,
            'household', 'SPG')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', self.common_form_data_empty,
            'household', 'SPG')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty, 'manager', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty, 'manager', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', self.common_form_data_empty, 'manager', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', self.common_form_data_empty,
            'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'SPG')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'SPG')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'SPG')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'manager', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'manager', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy',
            self.request_common_confirm_send_by_post_data_invalid, 'manager', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'HH', 'UAC', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'HH', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'HH', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'HH', 'UAC', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'SPG', 'UAC', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'SPG', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'SPG', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'UAC', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'CE', 'UAC', 'N', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'UAC', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'CE', 'UAC', 'N', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'HH', 'E', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'HH', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'HH', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'HH', 'N', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'SPG', 'E', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'SPG', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'SPG', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'E', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'E', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'W', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'W', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'CE', 'N', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'E', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'W', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'W', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'CE', 'N', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_select_manager_ce_m_ew_e(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_select_manager_ce_m_ew_w(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_select_resident_ce_m_ew_e(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_select_resident_ce_m_ew_w(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_ni, 'ni', 'household', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_en, 'en', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_household_information_code(
            self.post_request_access_code_household_cy, 'cy', 'household', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_select_manager_ce_m_ew_e(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_select_manager_ce_m_ew_w(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_select_manager_ce_m_cy(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_select_resident_ce_m_ew_e(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_select_resident_ce_m_ew_w(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_select_resident_ce_m_cy(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_select_resident_ce_m_ni(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_to_individual_code_sms_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_en, 'en', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual',
                                           override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_text(
            self.post_request_individual_code_confirm_send_by_text_en, 'en', 'HH', 'E', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_sms_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_en, 'en', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual',
                                           override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_text(
            self.post_request_individual_code_confirm_send_by_text_en, 'en', 'HH', 'W', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_sms_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_cy, 'cy', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy', override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_cy, 'cy', 'individual',
                                           override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_text(
            self.post_request_individual_code_confirm_send_by_text_cy, 'cy', 'HH', 'W', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_sms_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_ni, 'ni', 'HH')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni', override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_ni, 'ni', 'individual',
                                           override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_text(
            self.post_request_individual_code_confirm_send_by_text_ni, 'ni', 'HH', 'N', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_sms_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_en, 'en', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual',
                                           override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_text(
            self.post_request_individual_code_confirm_send_by_text_en, 'en', 'SPG', 'E', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_sms_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_en, 'en', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_en, 'en', 'individual',
                                           override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_text(
            self.post_request_individual_code_confirm_send_by_text_en, 'en', 'SPG', 'W', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_sms_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_cy, 'cy', 'SPG')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy', override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(self.post_request_individual_code_enter_mobile_cy, 'cy', 'individual',
                                           override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_text(
            self.post_request_individual_code_confirm_send_by_text_cy, 'cy', 'SPG', 'W', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_post_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_en, 'en', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH',
                                         override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', 'HH', 'UAC', 'E', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_post_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_en, 'en', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'HH',
                                         override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', 'HH', 'UAC', 'W', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_post_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_cy, 'cy', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy', override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_cy, 'cy', 'individual', 'HH',
                                         override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_code_confirm_send_by_post_cy, 'cy', 'HH', 'UAC', 'W', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_post_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_get_request_individual_code(self.get_request_individual_code_ni, 'ni')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_ni, 'ni', 'HH')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_ni, 'ni', override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_ni, 'ni', 'individual', 'HH',
                                         override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_code_confirm_send_by_post_ni, 'ni', 'HH', 'UAC', 'N', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_post_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_en, 'en', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'SPG',
                                         override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', 'SPG', 'UAC', 'E', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_post_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_get_request_individual_code(self.get_request_individual_code_en, 'en')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_en, 'en', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_en, 'en', 'individual', 'SPG',
                                         override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_code_confirm_send_by_post_en, 'en', 'SPG', 'UAC', 'W', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_to_individual_code_post_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'SPG', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_get_request_individual_code(self.get_request_individual_code_cy, 'cy')
        await self.check_post_request_individual_code_journey_switch(self.post_request_individual_code_cy, 'cy', 'SPG')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_individual_code_select_how_to_receive_cy, 'cy', override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_individual_code_enter_name_cy, 'cy', 'individual', 'SPG',
                                         override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_code_confirm_send_by_post_cy, 'cy', 'SPG', 'UAC', 'W', 'true',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_add_room_early_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'manager', 'ConfirmAddress', 'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'E', 'false',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_add_room_early_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'manager', 'ConfirmAddress', 'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'W', 'false',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_add_room_early_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.add_room_number(self.get_request_access_code_enter_room_number_cy,
                                   self.post_request_access_code_enter_room_number_cy,
                                   'cy', 'manager', 'ConfirmAddress', 'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'UAC', 'W', 'false',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_add_room_early_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'E', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_add_room_early_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_add_room_early_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.add_room_number(self.get_request_access_code_enter_room_number_cy,
                                   self.post_request_access_code_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress', 'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'UAC', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_add_room_early_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.add_room_number(self.get_request_access_code_enter_room_number_ni,
                                   self.post_request_access_code_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress', 'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'CE', 'UAC', 'N', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'E', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_cy,
                                   self.post_request_access_code_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress', 'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'UAC', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_ni,
                                   self.post_request_access_code_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress', 'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'CE', 'UAC', 'N', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_add_room_late_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'manager', 'ConfirmNameAddress', 'E', ce_type='manager')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'E', 'false',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_add_room_late_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager', 'CE')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'manager', 'ConfirmNameAddress', 'W', ce_type='manager')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'W', 'false',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_add_room_late_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager', 'CE')
        await self.add_room_number(self.get_request_access_code_enter_room_number_cy,
                                   self.post_request_access_code_enter_room_number_cy,
                                   'cy', 'manager', 'ConfirmNameAddress', 'W', ce_type='manager')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'UAC', 'W', 'false',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_add_room_late_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress', 'E', ce_type='manager')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'E', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_add_room_late_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress', 'W', ce_type='manager')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_add_room_late_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.add_room_number(self.get_request_access_code_enter_room_number_cy,
                                   self.post_request_access_code_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmNameAddress', 'W', ce_type='manager')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'UAC', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_add_room_late_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.add_room_number(self.get_request_access_code_enter_room_number_ni,
                                   self.post_request_access_code_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmNameAddress', 'N', ce_type='manager')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'CE', 'UAC', 'N', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_late_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress', 'E', ce_type='resident')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'E', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_late_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress', 'W', ce_type='resident')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_late_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE')
        await self.add_room_number(self.get_request_access_code_enter_room_number_cy,
                                   self.post_request_access_code_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmNameAddress', 'W', ce_type='resident')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'UAC', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_late_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE')
        await self.add_room_number(self.get_request_access_code_enter_room_number_ni,
                                   self.post_request_access_code_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmNameAddress', 'N', ce_type='resident')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'CE', 'UAC', 'N', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_over_length_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'E', ce_type='resident', data_over_length=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_over_length_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'W', ce_type='resident', data_over_length=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_over_length_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_cy,
                                   self.post_request_access_code_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress', 'W', ce_type='resident', data_over_length=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_over_length_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_ni,
                                   self.post_request_access_code_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress', 'N', ce_type='resident', data_over_length=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_check_for_value_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'E', ce_type='resident', check_for_value=False)
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'E', ce_type='resident', check_for_value=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_check_for_value_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'W', ce_type='resident', check_for_value=False)
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'W', ce_type='resident', check_for_value=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_check_for_value_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_cy,
                                   self.post_request_access_code_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress', 'W', ce_type='resident', check_for_value=False)
        await self.add_room_number(self.get_request_access_code_enter_room_number_cy,
                                   self.post_request_access_code_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress', 'W', ce_type='resident', check_for_value=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_check_for_value_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_ni,
                                   self.post_request_access_code_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress', 'N', ce_type='resident', check_for_value=False)
        await self.add_room_number(self.get_request_access_code_enter_room_number_ni,
                                   self.post_request_access_code_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress', 'N', ce_type='resident', check_for_value=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_only_space_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'E', ce_type='resident',
                                   check_for_value=False, data_only_space=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_only_space_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', 'W', ce_type='resident',
                                   check_for_value=False, data_only_space=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_only_space_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_cy,
                                   self.post_request_access_code_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress', 'W', ce_type='resident',
                                   check_for_value=False, data_only_space=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_early_only_space_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.add_room_number(self.get_request_access_code_enter_room_number_ni,
                                   self.post_request_access_code_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress', 'N', ce_type='resident',
                                   check_for_value=False, data_only_space=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_late_long_surname_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'E', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE',
                                         long_surname=True)
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress', 'E', ce_type='resident')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'E', 'true',
            check_room_number=True, long_surname=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_late_long_surname_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_en, 'en', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual', 'CE',
                                         long_surname=True)
        await self.add_room_number(self.get_request_access_code_enter_room_number_en,
                                   self.post_request_access_code_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress', 'W', ce_type='resident')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'W', 'true',
            check_room_number=True, long_surname=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_late_long_surname_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'CE',
                                             'W', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_cy, 'cy', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual', 'CE',
                                         long_surname=True)
        await self.add_room_number(self.get_request_access_code_enter_room_number_cy,
                                   self.post_request_access_code_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmNameAddress', 'W', ce_type='resident')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'UAC', 'W', 'true',
            check_room_number=True, long_surname=True)

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_add_room_late_long_surname_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual', 'CE',
                                         long_surname=True)
        await self.add_room_number(self.get_request_access_code_enter_room_number_ni,
                                   self.post_request_access_code_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmNameAddress', 'N', ce_type='resident')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_ni, 'ni', 'CE', 'UAC', 'N', 'true',
            check_room_number=True, long_surname=True)

    @unittest_run_loop
    async def test_get_request_access_code_address_in_northern_ireland_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'N')
        await self.check_post_confirm_address_address_in_northern_ireland(
            self.post_request_access_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_access_code_address_in_northern_ireland_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'N')
        await self.check_post_confirm_address_address_in_northern_ireland(
            self.post_request_access_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_address_in_northern_ireland_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'N')
        await self.check_post_confirm_address_input_yes_code(self.post_request_access_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_access_code_address_in_northern_ireland_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_access_code_address_in_northern_ireland_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='resident')
        await self.check_post_confirm_address_input_yes_code_individual(
            self.post_request_access_code_confirm_address_ni, 'ni', 'individual', 'CE')

    @unittest_run_loop
    async def test_get_request_access_code_address_not_in_northern_ireland_region_e_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'HH', 'E')
        await self.check_post_confirm_address_address_in_england(self.post_request_access_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_access_code_address_not_in_northern_ireland_region_w_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_access_code_select_address_ni, 'ni', 'HH', 'W')
        await self.check_post_confirm_address_address_in_wales(
            self.post_request_access_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_happy_path_nisra_manager(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni', 'CE',
                                             'N', ce_type='manager')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni')
        await self.check_post_resident_or_manager_code_manager_ni(
            self.post_request_access_code_resident_or_manager_ni, self.common_resident_or_manager_input_manager)
