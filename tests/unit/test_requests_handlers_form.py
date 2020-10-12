from aiohttp.test_utils import unittest_run_loop
from .helpers import TestHelpers


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
    async def test_post_request_paper_form_select_address_no_selection_ni(self):
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
    async def test_get_request_paper_form_confirm_address_data_invalid_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_address_en, 'en', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_data_invalid_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_data_invalid_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_scotland_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(
            self.post_request_paper_form_select_address_en, 'en', self.ai_uprn_result_scotland)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_paper_form_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_scotland_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(
            self.post_request_paper_form_select_address_cy, 'cy', self.ai_uprn_result_scotland)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_paper_form_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_scotland_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_form_select_address_ni, 'ni', self.ai_uprn_result_scotland)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_paper_form_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_form_address_not_found_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address_address_not_found(
            self.post_request_paper_form_select_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_form_address_not_found_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address_address_not_found(
            self.post_request_paper_form_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_form_address_not_found_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address_address_not_found(
            self.post_request_paper_form_select_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_form_census_address_type_na_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en,
                                             'en', self.ai_uprn_result_censusaddresstype_na)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_paper_form_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_form_census_address_type_na_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy,
                                             'cy', self.ai_uprn_result_censusaddresstype_na)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_paper_form_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_form_census_address_type_na_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni,
                                             'ni', self.ai_uprn_result_censusaddresstype_na_ni)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_paper_form_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_error_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_paper_form_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_error_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_paper_form_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_form_confirm_address_new_case_error_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_paper_form_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_empty_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_form_resident_or_manager_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_empty_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_form_resident_or_manager_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_empty_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_form_resident_or_manager_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_empty_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_form_resident_or_manager_ni, 'ni', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_invalid_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_form_resident_or_manager_en, 'en', self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_invalid_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_form_resident_or_manager_en, 'en', self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_invalid_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_form_resident_or_manager_cy, 'cy', self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_paper_form_resident_or_manager_invalid_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_form_resident_or_manager_ni, 'ni', self.common_resident_or_manager_input_invalid)

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
    async def test_request_paper_form_enter_name_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_first_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_enter_name_no_last_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_form_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', self.common_form_data_empty, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_cy, 'cy',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_ni, 'ni',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_cy, 'cy',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_ni, 'ni',
            self.request_common_confirm_name_address_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_cy, 'cy',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_ni, 'ni',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_en, 'en',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_cy, 'cy',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_invalid_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_invalid_or_no_selection(
            self.post_request_paper_form_confirm_name_address_ni, 'ni',
            self.request_common_confirm_name_address_data_invalid, 'individual')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_option_no_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_no_form(
            self.post_request_paper_form_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'HH', 'E', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'HH', 'W', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy, 'cy',
                                                             self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'HH', 'W', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni, 'ni',
                                                             self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'HH', 'N', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'SPG', 'E', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'SPG', 'W', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy, 'cy',
                                                             self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'SPG', 'W', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni, 'ni',
                                                             self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'SPG', 'N', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'E', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'W', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'CE', 'W', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'CE', 'N', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'E', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'W', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy, 'cy',
                                                             self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'CE', 'W', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_get_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni, 'ni',
                                                             self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_error_from_get_fulfilment(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'CE', 'N', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy, 'cy',
                                                             self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni, 'ni',
                                                             self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy, 'cy',
                                                             self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni, 'ni',
                                                             self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_en, 'en',
                                                             self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_cy, 'cy',
                                                             self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_form_confirm_name_address_request_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni, 'ni',
                                                             self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_error_from_request_fulfilment(
            self.post_request_paper_form_confirm_name_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'HH', 'QUESTIONNAIRE', 'E', 'false')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'HH', 'QUESTIONNAIRE', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'HH', 'QUESTIONNAIRE', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'HH', 'QUESTIONNAIRE', 'N', 'false')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'SPG', 'QUESTIONNAIRE', 'E', 'false')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'SPG', 'QUESTIONNAIRE', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'SPG', 'QUESTIONNAIRE', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'SPG', 'QUESTIONNAIRE', 'N', 'false')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'QUESTIONNAIRE', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'CE', 'QUESTIONNAIRE', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'QUESTIONNAIRE', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_sent_post_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'CE', 'QUESTIONNAIRE', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'HH', 'LARGE_PRINT', 'E', 'false')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'HH', 'LARGE_PRINT', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'HH', 'LARGE_PRINT', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'HH', 'LARGE_PRINT', 'N', 'false')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'SPG', 'LARGE_PRINT', 'E', 'false')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'SPG', 'LARGE_PRINT', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'SPG', 'LARGE_PRINT', 'W', 'false')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'household')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'SPG', 'LARGE_PRINT', 'N', 'false')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'LARGE_PRINT', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'CE', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'CE', 'LARGE_PRINT', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'LARGE_PRINT', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_en, 'en', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_en, 'en', 'CE', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_cy, 'cy', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_cy, 'cy', 'CE', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_form_large_print_sent_post_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_form_enter_name_ni, 'ni', 'individual')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_paper_form_confirm_name_address_ni, 'ni', 'CE', 'LARGE_PRINT', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_en, 'en')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_sms_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_get_select_method_form_manager(self.get_request_access_code_select_method_en, 'en')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en',
                                                      override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en',
                                           override_sub_user_journey='access-code')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'E', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_sms_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_get_select_method_form_manager(self.get_request_access_code_select_method_en, 'en')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_en, 'en',
                                                      override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en',
                                           override_sub_user_journey='access-code')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_en, 'en', 'CE', 'W', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_sms_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_get_select_method_form_manager(self.get_request_access_code_select_method_cy, 'cy')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_cy, 'cy',
                                                      override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy',
                                           override_sub_user_journey='access-code')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_cy, 'cy', 'CE', 'W', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_sms_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_get_select_method_form_manager(self.get_request_access_code_select_method_ni, 'ni')
        await self.check_post_select_method_input_sms(self.post_request_access_code_select_method_ni, 'ni',
                                                      override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_ni, 'ni',
                                           override_sub_user_journey='access-code')
        await self.check_post_confirm_mobile(
            self.post_request_access_code_confirm_mobile_ni, 'ni', 'CE', 'N', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_post_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_get_select_method_form_manager(self.get_request_access_code_select_method_en, 'en')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en',
                                                       override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en',
                                         'manager', override_sub_user_journey='access-code')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'UAC', 'E', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_post_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_form_select_address_en, 'en')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_en, 'en')
        await self.check_get_select_method_form_manager(self.get_request_access_code_select_method_en, 'en')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_en, 'en',
                                                       override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en',
                                         'manager', override_sub_user_journey='access-code')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_en, 'en', 'CE', 'UAC', 'W', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_post_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_form_select_address_cy, 'cy')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_cy, 'cy')
        await self.check_get_select_method_form_manager(self.get_request_access_code_select_method_cy, 'cy')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_cy, 'cy',
                                                       override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy',
                                         'manager', override_sub_user_journey='access-code')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_cy, 'cy', 'CE', 'UAC', 'W', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_form_select_manager_uac_post_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_form_select_address_ni, 'ni')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_form_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_form_resident_or_manager_ni, 'ni')
        await self.check_get_select_method_form_manager(self.get_request_access_code_select_method_ni, 'ni')
        await self.check_post_select_method_input_post(self.post_request_access_code_select_method_ni, 'ni',
                                                       override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_ni, 'ni',
                                         'manager', override_sub_user_journey='access-code')
        await self.check_post_confirm_name_address_input_yes(
            self.post_request_access_code_confirm_name_address_ni, 'ni', 'CE', 'UAC', 'N', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_northern_ireland_ew(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_en, 'en')
        await self.check_post_select_address(
            self.post_request_paper_form_select_address_en, 'en', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_address_in_northern_ireland(
            self.post_request_paper_form_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_northern_ireland_cy(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_cy, 'cy')
        await self.check_post_select_address(
            self.post_request_paper_form_select_address_cy, 'cy', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_address_in_northern_ireland(
            self.post_request_paper_form_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_northern_ireland_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_form_select_address_ni, 'ni', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni, 'ni',
                                                             self.rhsvc_case_by_uprn_hh_n)

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_northern_ireland_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_form_select_address_ni, 'ni', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni, 'ni',
                                                             self.rhsvc_case_by_uprn_spg_n)

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_northern_ireland_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_form_select_address_ni, 'ni', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_form_confirm_address_ni, 'ni',
                                                           self.rhsvc_case_by_uprn_ce_m_n)

    @unittest_run_loop
    async def test_get_request_paper_form_address_in_northern_ireland_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_form_select_address_ni, 'ni', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_form_confirm_address_ni, 'ni',
                                                             self.rhsvc_case_by_uprn_ce_r_n)

    @unittest_run_loop
    async def test_get_request_paper_form_address_not_in_northern_ireland_region_e_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_form_select_address_ni, 'ni', self.ai_uprn_result_england)
        await self.check_post_confirm_address_address_in_england(
            self.post_request_paper_form_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_form_address_not_in_northern_ireland_region_w_ni(self):
        await self.check_get_enter_address(self.get_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_form_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_form_select_address_ni, 'ni', self.ai_uprn_result_wales)
        await self.check_post_confirm_address_address_in_wales(
            self.post_request_paper_form_confirm_address_ni, 'ni')
