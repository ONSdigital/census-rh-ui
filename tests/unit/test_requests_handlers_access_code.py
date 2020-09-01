from unittest import mock

from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from .helpers import TestHelpers

attempts_retry_limit = 5


# noinspection PyTypeChecker
class TestRequestsHandlersAccessCode(TestHelpers):

    user_journey = 'requests'
    sub_user_journey = 'access-code'

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'HH', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_cy, 'cy', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_ni, 'ni', 'HH', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'SPG', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'SPG', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_cy, 'cy', 'SPG', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_ni, 'ni', 'SPG', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_cy, 'cy', 'CE', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_ni, 'ni', 'CE', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_cy, 'cy', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_ni, 'ni', 'CE', 'N', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_cy, 'cy', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_ni, 'ni', 'CE', 'N', 'true')

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
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_en, 'en', 500)
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_cy, 'cy', 500)
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_ni, 'ni', 500)
        await self.check_post_enter_address_error_503_from_ai(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address_error_503_from_ai(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address_error_503_from_ai(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_en, 'en', 403)
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_cy, 'cy', 403)
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_ni, 'ni', 403)
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_en, 'en', 401)
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_cy, 'cy', 401)
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_ni, 'ni', 401)
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_en, 'en', 400)
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_cy, 'cy', 400)
        await self.check_post_enter_address_error_from_ai(self.post_request_access_code_enter_address_ni, 'ni', 400)
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
        await self.check_post_select_address(
            self.post_request_access_code_select_address_en, 'en', self.ai_uprn_result_scotland)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_access_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_access_code_address_in_scotland_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(
            self.post_request_access_code_select_address_cy, 'cy', self.ai_uprn_result_scotland)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_access_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_address_in_scotland_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_access_code_select_address_ni, 'ni', self.ai_uprn_result_scotland)
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
    async def test_get_request_access_code_census_address_type_na_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en,
                                             'en', self.ai_uprn_result_censusaddresstype_na)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_access_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_access_code_census_address_type_na_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy,
                                             'cy', self.ai_uprn_result_censusaddresstype_na)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_access_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_census_address_type_na_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni,
                                             'ni', self.ai_uprn_result_censusaddresstype_na)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_access_code_confirm_address_ni, 'ni')

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
    async def test_get_request_access_code_timeout_ew(self):
        await self.check_get_timeout(self.get_request_access_code_timeout_en, 'en')

    @unittest_run_loop
    async def test_get_request_access_code_timeout_cy(self):
        await self.check_get_timeout(self.get_request_access_code_timeout_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_timeout_ni(self):
        await self.check_get_timeout(self.get_request_access_code_timeout_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_access_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_access_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_access_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_access_code_address_not_required_ew(self):
        # TODO - to be removed, test will become redundant soon
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
    async def test_get_request_access_code_address_not_required_cy(self):
        # TODO - to be removed, test will become redundant soon
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
    async def test_get_request_access_code_address_not_required_ni(self):
        # TODO - to be removed, test will become redundant soon
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
    async def test_get_request_access_code_confirm_address_data_no_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_no(self.post_request_access_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_individual_confirm_address_data_no_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_no(self.post_request_access_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_no(self.post_request_access_code_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_en, 'en', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_cy, 'cy', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_ni, 'ni', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
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
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_en, 'en', self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_invalid_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_en, 'en', self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_invalid_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_cy, 'cy', self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_invalid_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_ni, 'ni', self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_resident_or_manager_empty_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_access_code_resident_or_manager_ni, 'ni', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_cy, 'cy', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_ni, 'ni', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_cy, 'cy', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_ni, 'ni', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en', self.common_form_data_empty, 'manager')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en', self.common_form_data_empty, 'manager')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_cy, 'cy', self.common_form_data_empty, 'manager')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_ni, 'ni', self.common_form_data_empty, 'manager')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_cy, 'cy', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_ni, 'ni', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_cy, 'cy', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_no_selection_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_ni, 'ni', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en',
            self.request_code_select_method_data_invalid, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en',
            self.request_code_select_method_data_invalid, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_cy, 'cy',
            self.request_code_select_method_data_invalid, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_ni, 'ni',
            self.request_code_select_method_data_invalid, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en',
            self.request_code_select_method_data_invalid, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en',
            self.request_code_select_method_data_invalid, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_cy, 'cy',
            self.request_code_select_method_data_invalid, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_ni, 'ni',
            self.request_code_select_method_data_invalid, 'household')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en',
            self.request_code_select_method_data_invalid, 'manager')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en',
            self.request_code_select_method_data_invalid, 'manager')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_cy, 'cy',
            self.request_code_select_method_data_invalid, 'manager')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_ni, 'ni',
            self.request_code_select_method_data_invalid, 'manager')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en',
            self.request_code_select_method_data_invalid, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en',
            self.request_code_select_method_data_invalid, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_cy, 'cy',
            self.request_code_select_method_data_invalid, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_ni, 'ni',
            self.request_code_select_method_data_invalid, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en',
            self.request_code_select_method_data_invalid, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_en, 'en',
            self.request_code_select_method_data_invalid, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_cy, 'cy',
            self.request_code_select_method_data_invalid, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_select_method_input_invalid_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_invalid_or_no_selection(
            self.post_request_access_code_select_method_ni, 'ni',
            self.request_code_select_method_data_invalid, 'individual')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_no_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_no(self.post_request_access_code_confirm_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_cy, 'cy', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_ni, 'ni', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_cy, 'cy', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_ni, 'ni', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_cy, 'cy', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_ni, 'ni', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_cy, 'cy', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_ni, 'ni', self.request_code_mobile_confirmation_data_empty)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_cy, 'cy', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_ni, 'ni', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_cy, 'cy', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_ni, 'ni', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_cy, 'cy', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_ni, 'ni', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_en, 'en', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_cy, 'cy', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_invalid_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_mobile_ni, 'ni', self.request_code_mobile_confirmation_data_invalid)

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en', 'HH', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_cy, 'cy', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_ni, 'ni', 'HH', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en', 'SPG', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en', 'SPG', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_cy, 'cy', 'SPG', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_ni, 'ni', 'SPG', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_cy, 'cy', 'CE', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_ni, 'ni', 'CE', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_cy, 'cy', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_ni, 'ni', 'CE', 'N', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_cy, 'cy', 'CE', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_get_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_error_from_get_fulfilment(
            self.post_request_access_code_confirm_mobile_ni, 'ni', 'CE', 'N', 'true')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_mobile_request_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(
            self.post_request_access_code_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni')
        await self.check_post_confirm_mobile_error_from_request_fulfilment(
            self.post_request_access_code_confirm_mobile_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_cy, 'cy', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_ni, 'ni', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_cy, 'cy', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_ni, 'ni', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en', self.common_form_data_empty, 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en', self.common_form_data_empty, 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_cy, 'cy', self.common_form_data_empty, 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'manager')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_ni, 'ni', self.common_form_data_empty, 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_cy, 'cy', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_ni, 'ni', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_cy, 'cy', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_ni, 'ni', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_cy, 'cy',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_ni, 'ni',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_cy, 'cy',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_ni, 'ni',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_cy, 'cy',
            self.request_common_confirm_name_address_data_invalid, 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'manager')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_ni, 'ni',
            self.request_common_confirm_name_address_data_invalid, 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_cy, 'cy',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_ni, 'ni',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_cy, 'cy',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_input_invalid_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_name_address_ni, 'ni',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_en, 'en', 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_en, 'en', 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_en, 'en', 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_en, 'en', 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_en, 'en', 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_en, 'en', 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'manager')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'manager')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_en, 'en', 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_en, 'en', 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_en, 'en', 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_en, 'en', 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_option_no_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_no(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'individual')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'HH', 'UAC', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'HH', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'HH', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'HH', 'UAC', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'SPG', 'UAC', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'SPG', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'SPG', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'SPG', 'UAC', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'UAC', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'CE', 'UAC', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'manager')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'CE', 'UAC', 'N', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'UAC', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'UAC', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'CE', 'UAC', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'CE', 'UAC', 'N', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'UAC', 'E', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'UAC', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'CE', 'UAC', 'W', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'CE', 'UAC', 'N', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en', 'HH', 'E', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en', 'HH', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'HH', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'HH', 'N', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en', 'SPG', 'E', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en', 'SPG', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'SPG', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'SPG', 'N', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'E', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'CE', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'manager')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'CE', 'N', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'E', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'W', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'CE', 'W', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'CE', 'N', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'E', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'W', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'CE', 'W', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_get_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'CE', 'N', 'UAC', 'true')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_hh_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_hh_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_e, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_spg_w, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_spg_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_spg_n, 'household')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_select_manager_ce_m_ew_e(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_select_manager_ce_m_ew_w(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'manager')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'manager')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_manager, 'manager')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'manager')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_select_resident_ce_m_ew_e(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_select_resident_ce_m_ew_w(
            self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_access_code_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager(
            self.post_request_access_code_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_resident, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_e, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_en,
                                                        'en', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_cy,
                                                        'cy', self.rhsvc_case_by_uprn_ce_r_w, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_name_address_request_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_access_code_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes(self.post_request_access_code_confirm_address_ni,
                                                        'ni', self.rhsvc_case_by_uprn_ce_r_n, 'individual')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_access_code_confirm_name_address_ni, 'ni')
