from aiohttp.test_utils import unittest_run_loop
from .helpers import TestHelpers


# noinspection PyTypeChecker
class TestRequestsHandlersPaperForm(TestHelpers):

    user_journey = 'requests'
    sub_user_journey = 'paper-questionnaire'

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_enter_address_empty_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address_input_empty(self.post_request_paper_questionnaire_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_enter_address_empty_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address_input_empty(self.post_request_paper_questionnaire_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_enter_address_empty_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address_input_empty(self.post_request_paper_questionnaire_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_enter_address_invalid_postcode_en(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address_input_invalid(self.post_request_paper_questionnaire_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_enter_address_invalid_postcode_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address_input_invalid(self.post_request_paper_questionnaire_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_enter_address_invalid_postcode_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address_input_invalid(self.post_request_paper_questionnaire_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_select_address_no_selection_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address_no_selection_made(
            self.post_request_paper_questionnaire_select_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_select_address_no_selection_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address_no_selection_made(
            self.post_request_paper_questionnaire_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_select_address_no_selection_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address_no_selection_made(
            self.post_request_paper_questionnaire_select_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_enter_address_no_results_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_paper_questionnaire_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_enter_address_no_results_cy(
            self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_paper_questionnaire_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_enter_address_no_results_ni(
            self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_paper_questionnaire_enter_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_no_selection_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_no_selection_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_no_selection_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_get_cases_error_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_paper_questionnaire_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_get_cases_error_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_get_cases_error_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_error_from_get_cases(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_data_no_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_no(self.post_request_paper_questionnaire_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_data_no_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_no(self.post_request_paper_questionnaire_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_data_no_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_no(self.post_request_paper_questionnaire_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_data_invalid_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_data_invalid_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_data_invalid_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_in_scotland_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(
            self.post_request_paper_questionnaire_select_address_en, 'en', 'HH', self.ai_uprn_result_scotland)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_paper_questionnaire_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_in_scotland_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(
            self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH', self.ai_uprn_result_scotland)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_in_scotland_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH', self.ai_uprn_result_scotland)
        await self.check_post_confirm_address_address_in_scotland(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_not_found_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address_address_not_found(
            self.post_request_paper_questionnaire_select_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_not_found_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address_address_not_found(
            self.post_request_paper_questionnaire_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_not_found_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address_address_not_found(
            self.post_request_paper_questionnaire_select_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_census_address_type_na_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en,
                                             'en', 'HH', self.ai_uprn_result_censusaddresstype_na)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_paper_questionnaire_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_census_address_type_na_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy,
                                             'cy', 'HH', self.ai_uprn_result_censusaddresstype_na)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_census_address_type_na_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni,
                                             'ni', 'HH', self.ai_uprn_result_censusaddresstype_na_ni)
        await self.check_post_confirm_address_returns_addresstype_na(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form_new_case(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce_new_case(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_new_case_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_new_case_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_new_case_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_new_case_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_error_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_paper_questionnaire_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_error_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_confirm_address_new_case_error_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_error_from_create_case(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_resident_or_manager_empty_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_resident_or_manager_empty_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_resident_or_manager_empty_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_resident_or_manager_empty_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_resident_or_manager_invalid_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_resident_or_manager_invalid_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en',
            self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_resident_or_manager_invalid_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy',
            self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_resident_or_manager_invalid_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni',
            self.common_resident_or_manager_input_invalid)

    @unittest_run_loop
    async def test_post_request_paper_questionnaire_get_ai_postcode_error(self):
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_en,
                                                          self.post_request_paper_questionnaire_enter_address_en,
                                                          'en', 500)
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_cy,
                                                          self.post_request_paper_questionnaire_enter_address_cy,
                                                          'cy', 500)
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_ni,
                                                          self.post_request_paper_questionnaire_enter_address_ni,
                                                          'ni', 500)
        await self.check_post_enter_address_error_503_from_ai(self.post_request_paper_questionnaire_enter_address_en,
                                                              'en')
        await self.check_post_enter_address_error_503_from_ai(self.post_request_paper_questionnaire_enter_address_cy,
                                                              'cy')
        await self.check_post_enter_address_error_503_from_ai(self.post_request_paper_questionnaire_enter_address_ni,
                                                              'ni')
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_en,
                                                          self.post_request_paper_questionnaire_enter_address_en,
                                                          'en', 403)
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_cy,
                                                          self.post_request_paper_questionnaire_enter_address_cy,
                                                          'cy', 403)
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_ni,
                                                          self.post_request_paper_questionnaire_enter_address_ni,
                                                          'ni', 403)
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_en,
                                                          self.post_request_paper_questionnaire_enter_address_en,
                                                          'en', 401)
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_cy,
                                                          self.post_request_paper_questionnaire_enter_address_cy,
                                                          'cy', 401)
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_ni,
                                                          self.post_request_paper_questionnaire_enter_address_ni,
                                                          'ni', 401)
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_en,
                                                          self.post_request_paper_questionnaire_enter_address_en,
                                                          'en', 400)
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_cy,
                                                          self.post_request_paper_questionnaire_enter_address_cy,
                                                          'cy', 400)
        await self.check_post_enter_address_error_from_ai(self.get_request_paper_questionnaire_enter_address_ni,
                                                          self.post_request_paper_questionnaire_enter_address_ni,
                                                          'ni', 400)
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_questionnaire_enter_address_en, 'en', epoch='test')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_questionnaire_enter_address_cy, 'cy', epoch='test')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_paper_questionnaire_enter_address_ni, 'ni', epoch='test')

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.common_form_data_empty, False, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_first_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_first, False, True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_en,
                                                             'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_ni,
                                                             'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_enter_name_no_last_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name_inputs_error(self.post_request_paper_questionnaire_enter_name_ni, 'ni',
                                                      self.request_common_enter_name_form_data_no_last, True, False)

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.common_form_data_empty, 'household', 'HH')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.common_form_data_empty, 'household', 'HH')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy',
            self.common_form_data_empty, 'household', 'HH')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni',
            self.common_form_data_empty, 'household', 'HH')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.common_form_data_empty, 'household', 'SPG')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.common_form_data_empty, 'household', 'SPG')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy',
            self.common_form_data_empty, 'household', 'SPG')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni',
            self.common_form_data_empty, 'household', 'SPG')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.common_form_data_empty, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.common_form_data_empty, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy',
            self.common_form_data_empty, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni',
            self.common_form_data_empty, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.common_form_data_empty, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.common_form_data_empty, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy',
            self.common_form_data_empty, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni',
            self.common_form_data_empty, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'HH')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'SPG')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'SPG')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(self.post_request_paper_questionnaire_confirm_address_cy,
                                                             'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'SPG')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni',
            self.request_common_confirm_send_by_post_data_invalid, 'household', 'SPG')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_invalid_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni',
            self.request_common_confirm_send_by_post_data_invalid, 'individual', 'CE')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_option_no_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_no_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'E', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'W', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'HH', 'W', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'HH', 'N', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'E', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'W', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'SPG', 'W', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'SPG', 'N', 'QUESTIONNAIRE', 'false')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'E', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'W', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'CE', 'W', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'CE', 'N', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'E', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'W', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'CE', 'W', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_get_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'CE', 'N', 'QUESTIONNAIRE', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_en,
                                                           'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_cy,
                                                           'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(self.post_request_paper_questionnaire_confirm_address_ni,
                                                           'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_questionnaire_confirm_send_by_post_request_fulfilment_error_429_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_form(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'E', 'false',
            number_in_household=4)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=4)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'HH', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=4)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'HH', 'QUESTIONNAIRE', 'N', 'false',
            number_in_household=4)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'E', 'false',
            number_in_household=4)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=4)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'SPG', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=4)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '4')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'SPG', 'QUESTIONNAIRE', 'N', 'false',
            number_in_household=4)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'CE', 'QUESTIONNAIRE', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'CE', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'CE', 'QUESTIONNAIRE', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '2')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'LARGE_PRINT', 'E', 'false',
            number_in_household=2)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '2')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'LARGE_PRINT', 'W', 'false',
            number_in_household=2)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '2')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'HH', 'LARGE_PRINT', 'W', 'false',
            number_in_household=2)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '2')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'HH', 'LARGE_PRINT', 'N', 'false',
            number_in_household=2)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '2')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'LARGE_PRINT', 'E', 'false',
            number_in_household=2)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '2')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'LARGE_PRINT', 'W', 'false',
            number_in_household=2)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '2')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'SPG', 'LARGE_PRINT', 'W', 'false',
            number_in_household=2)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '2')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'SPG', 'LARGE_PRINT', 'N', 'false',
            number_in_household=2)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_select_resident_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'LARGE_PRINT', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_select_resident_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_select_resident_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'CE', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_select_resident_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'CE', 'LARGE_PRINT', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'LARGE_PRINT', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'CE', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'CE', 'LARGE_PRINT', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_select_manager_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_select_manager_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')

    @unittest_run_loop
    async def test_request_paper_questionnaire_select_manager_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')

    @unittest_run_loop
    async def test_request_paper_questionnaire_select_manager_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_manager_ni(
            self.post_request_paper_questionnaire_resident_or_manager_ni, self.common_resident_or_manager_input_manager)

    @unittest_run_loop
    async def test_request_paper_questionnaire_select_manager_uac_sms_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_get_select_how_to_receive_form_manager(
            self.get_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(
            self.post_request_access_code_enter_mobile_en, 'en', 'manager', override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'E', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_questionnaire_select_manager_uac_sms_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_get_select_how_to_receive_form_manager(
            self.get_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(
            self.post_request_access_code_enter_mobile_en, 'en', 'manager', override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'CE', 'W', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_questionnaire_select_manager_uac_sms_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_get_select_how_to_receive_form_manager(
            self.get_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy', override_sub_user_journey='access-code')
        await self.check_post_enter_mobile(
            self.post_request_access_code_enter_mobile_cy, 'cy', 'manager', override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'CE', 'W', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_questionnaire_select_manager_uac_post_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_get_select_how_to_receive_form_manager(
            self.get_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en',
                                         'manager', 'CE', override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'E', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_questionnaire_select_manager_uac_post_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_get_select_how_to_receive_form_manager(
            self.get_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en', override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en',
                                         'manager', 'CE', override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'CE', 'UAC', 'W', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_questionnaire_select_manager_uac_post_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_manager(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_get_select_how_to_receive_form_manager(
            self.get_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy', override_sub_user_journey='access-code')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy',
                                         'manager', 'CE', override_sub_user_journey='access-code')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'CE', 'UAC', 'W', 'false',
            override_sub_user_journey='access-code')

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_add_room_early_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'E', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_add_room_early_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_add_room_early_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_cy,
                                   self.post_request_paper_questionnaire_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'CE', 'QUESTIONNAIRE', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_add_room_early_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_ni,
                                   self.post_request_paper_questionnaire_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'CE', 'QUESTIONNAIRE', 'N', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'E', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_cy,
                                   self.post_request_paper_questionnaire_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'CE', 'QUESTIONNAIRE', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_ni,
                                   self.post_request_paper_questionnaire_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE',
                                         check_room_number=True)
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'CE', 'QUESTIONNAIRE', 'N', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_add_room_late_ce_m_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_e)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'E', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_add_room_late_ce_m_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_en, 'en')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_add_room_late_ce_m_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_m_w)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_cy, 'cy')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_cy,
                                   self.post_request_paper_questionnaire_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'CE', 'QUESTIONNAIRE', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_select_resident_add_room_late_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)
        await self.check_post_resident_or_manager_form_resident(
            self.post_request_paper_questionnaire_resident_or_manager_ni, 'ni')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_ni,
                                   self.post_request_paper_questionnaire_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'CE', 'QUESTIONNAIRE', 'N', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_late_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'E', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_late_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_late_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_cy,
                                   self.post_request_paper_questionnaire_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'CE', 'QUESTIONNAIRE', 'W', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_late_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_ni,
                                   self.post_request_paper_questionnaire_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'CE', 'QUESTIONNAIRE', 'N', 'true',
            check_room_number=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_empty_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', no_data=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_empty_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', no_data=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_empty_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_cy,
                                   self.post_request_paper_questionnaire_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress', no_data=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_empty_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_ni,
                                   self.post_request_paper_questionnaire_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress', no_data=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_over_length_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', data_over_length=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_over_length_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', data_over_length=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_over_length_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_cy,
                                   self.post_request_paper_questionnaire_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress', data_over_length=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_over_length_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_ni,
                                   self.post_request_paper_questionnaire_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress', data_over_length=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_check_for_value_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', check_for_value=False)
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', check_for_value=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_check_for_value_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', check_for_value=False)
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmAddress', check_for_value=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_check_for_value_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_cy,
                                   self.post_request_paper_questionnaire_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress', check_for_value=False)
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_cy,
                                   self.post_request_paper_questionnaire_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmAddress', check_for_value=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_early_check_for_value_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_ni,
                                   self.post_request_paper_questionnaire_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress', check_for_value=False)
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_ni,
                                   self.post_request_paper_questionnaire_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmAddress', check_for_value=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_late_long_surname_ce_r_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_e)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE',
                                         long_surname=True)
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'E', 'true',
            check_room_number=True, long_surname=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_late_long_surname_ce_r_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'individual', 'CE',
                                         long_surname=True)
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_en,
                                   self.post_request_paper_questionnaire_enter_room_number_en,
                                   'en', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'CE', 'QUESTIONNAIRE', 'W', 'true',
            check_room_number=True, long_surname=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_late_long_surname_ce_r_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_ce_r_w)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'individual', 'CE',
                                         long_surname=True)
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_cy,
                                   self.post_request_paper_questionnaire_enter_room_number_cy,
                                   'cy', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'CE', 'QUESTIONNAIRE', 'W', 'true',
            check_room_number=True, long_surname=True)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_add_room_late_long_surname_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE')
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'individual', 'CE',
                                         long_surname=True)
        await self.add_room_number(self.get_request_paper_questionnaire_enter_room_number_ni,
                                   self.post_request_paper_questionnaire_enter_room_number_ni,
                                   'ni', 'individual', 'ConfirmNameAddress')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'CE', 'QUESTIONNAIRE', 'N', 'true',
            check_room_number=True, long_surname=True)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_in_northern_ireland_ew(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(
            self.post_request_paper_questionnaire_select_address_en, 'en', 'HH', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_address_in_northern_ireland(
            self.post_request_paper_questionnaire_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_in_northern_ireland_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(
            self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_address_in_northern_ireland(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_in_northern_ireland_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_in_northern_ireland_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG', self.ai_uprn_result_northern_ireland)
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_in_northern_ireland_ce_m_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE',
            self.ai_uprn_result_northern_ireland_ce)
        await self.check_post_confirm_address_input_yes_ce(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_m_n)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_in_northern_ireland_ce_r_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_questionnaire_select_address_ni, 'ni', 'CE',
            self.ai_uprn_result_northern_ireland_ce)
        await self.check_post_confirm_address_input_yes_form_individual(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_ce_r_n)

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_not_in_northern_ireland_region_e_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH', self.ai_uprn_result_england)
        await self.check_post_confirm_address_address_in_england(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_get_request_paper_questionnaire_address_not_in_northern_ireland_region_w_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(
            self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH', self.ai_uprn_result_wales)
        await self.check_post_confirm_address_address_in_wales(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni')

    @unittest_run_loop
    async def test_request_paper_questionnaire_individual_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_get_request_individual_form(self.get_request_individual_form_en, 'en')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_individual_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_get_request_individual_form(self.get_request_individual_form_en, 'en')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_individual_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_get_request_individual_form(self.get_request_individual_form_cy, 'cy')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_cy, 'cy')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_cy, 'cy', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_cy, 'cy', 'HH', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_individual_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_get_request_individual_form(self.get_request_individual_form_ni, 'ni')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_ni, 'ni')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_ni, 'ni', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_ni, 'ni', 'HH', 'QUESTIONNAIRE', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_individual_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_get_request_individual_form(self.get_request_individual_form_en, 'en')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_en, 'en', 'individual', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_individual_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_get_request_individual_form(self.get_request_individual_form_en, 'en')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_en, 'en', 'individual', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_individual_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_get_request_individual_form(self.get_request_individual_form_cy, 'cy')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_cy, 'cy')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_cy, 'cy', 'individual', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_cy, 'cy', 'SPG', 'QUESTIONNAIRE', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_individual_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_get_request_individual_form(self.get_request_individual_form_ni, 'ni')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_ni, 'ni')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_ni, 'ni', 'individual', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_ni, 'ni', 'SPG', 'QUESTIONNAIRE', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_individual_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_get_request_individual_form(self.get_request_individual_form_en, 'en')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_en, 'en', 'HH', 'LARGE_PRINT', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_individual_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_get_request_individual_form(self.get_request_individual_form_en, 'en')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_en, 'en', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_en, 'en', 'HH', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_individual_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_get_request_individual_form(self.get_request_individual_form_cy, 'cy')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_cy, 'cy')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_cy, 'cy', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_cy, 'cy', 'HH', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_individual_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_get_request_individual_form(self.get_request_individual_form_ni, 'ni')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_ni, 'ni')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_ni, 'ni', 'individual', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_ni, 'ni', 'HH', 'LARGE_PRINT', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_individual_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_get_request_individual_form(self.get_request_individual_form_en, 'en')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_en, 'en', 'individual', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_en, 'en', 'SPG', 'LARGE_PRINT', 'E', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_individual_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_get_request_individual_form(self.get_request_individual_form_en, 'en')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_en, 'en')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_en, 'en', 'individual', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_en, 'en', 'SPG', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_individual_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_get_request_individual_form(self.get_request_individual_form_cy, 'cy')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_cy, 'cy')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_cy, 'cy', 'individual', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_cy, 'cy', 'SPG', 'LARGE_PRINT', 'W', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_individual_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_get_request_individual_form(self.get_request_individual_form_ni, 'ni')
        await self.check_post_request_individual_form_journey_switch(self.post_request_individual_form_ni, 'ni')
        await self.check_post_enter_name(self.post_request_individual_form_enter_name_ni, 'ni', 'individual', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_individual_form_confirm_send_by_post_ni, 'ni', 'SPG', 'LARGE_PRINT', 'N', 'true')

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_0_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'E', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_0_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_0_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'HH', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_0_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'HH', 'QUESTIONNAIRE', 'N', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_0_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'E', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_0_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_0_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'SPG', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_0_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'SPG', 'QUESTIONNAIRE', 'N', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_6_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '6')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'E', 'false',
            number_in_household=6)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_6_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '6')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=6)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_6_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '6')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'HH', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=6)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_6_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '6')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'HH', 'QUESTIONNAIRE', 'N', 'false',
            number_in_household=6)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_6_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '6')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'E', 'false',
            number_in_household=6)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_6_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '6')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=6)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_6_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '6')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'SPG', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=6)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_6_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '6')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'SPG', 'QUESTIONNAIRE', 'N', 'false',
            number_in_household=6)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_7_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'E', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_7_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_7_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'HH', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_7_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'HH', 'QUESTIONNAIRE', 'N', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_7_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'E', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_7_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_7_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'SPG', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_7_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'SPG', 'QUESTIONNAIRE', 'N', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_18_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '18')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'E', 'false',
            number_in_household=18)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_18_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '18')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=18)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_18_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '18')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'HH', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=18)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_18_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '18')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'HH', 'QUESTIONNAIRE', 'N', 'false',
            number_in_household=18)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_18_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '18')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'E', 'false',
            number_in_household=18)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_18_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '18')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=18)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_18_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '18')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'SPG', 'QUESTIONNAIRE', 'W', 'false',
            number_in_household=18)

    @unittest_run_loop
    async def test_request_paper_questionnaire_sent_post_no_in_household_18_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '18')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'SPG', 'QUESTIONNAIRE', 'N', 'false',
            number_in_household=18)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_0_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'LARGE_PRINT', 'E', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_0_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'LARGE_PRINT', 'W', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_0_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'HH', 'LARGE_PRINT', 'W', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_0_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'HH', 'LARGE_PRINT', 'N', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_0_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'LARGE_PRINT', 'E', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_0_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'LARGE_PRINT', 'W', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_0_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'SPG', 'LARGE_PRINT', 'W', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_0_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '0')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'SPG', 'LARGE_PRINT', 'N', 'false',
            number_in_household=0)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_7_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'LARGE_PRINT', 'E', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_7_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'HH', 'LARGE_PRINT', 'W', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_7_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'HH', 'LARGE_PRINT', 'W', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_7_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'HH')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'HH', 'LARGE_PRINT', 'N', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_7_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'LARGE_PRINT', 'E', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_7_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_en, 'en', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_en, 'en', 'SPG', 'LARGE_PRINT', 'W', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_7_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_cy, 'cy', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_cy, 'cy', 'SPG', 'LARGE_PRINT', 'W', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_large_print_sent_post_no_in_household_7_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '7')
        await self.check_post_enter_name(self.post_request_paper_questionnaire_enter_name_ni, 'ni', 'household', 'SPG')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_paper_questionnaire_confirm_send_by_post_ni, 'ni', 'SPG', 'LARGE_PRINT', 'N', 'false',
            number_in_household=7)

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_empty_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_empty_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_empty_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_empty_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_empty_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_nan_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', 'aaa')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_nan_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', 'aaa')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_nan_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', 'aaa')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_nan_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', 'aaa')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_nan_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', 'aaa')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_nan_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', 'aaa')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_nan_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', 'aaa')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_nan_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', 'aaa')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_31_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '31')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_31_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '31')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_31_hh_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_hh_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '31')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_31_hh_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'HH')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_hh_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '31')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_31_spg_ew_e(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_e)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '31')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_31_spg_ew_w(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_en, 'en', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_en, 'en', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_en, 'en')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_en, 'en', '31')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_31_spg_cy(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_cy, 'cy', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_cy, 'cy', self.rhsvc_case_by_uprn_spg_w)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_cy, 'cy')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_cy, 'cy', '31')

    @unittest_run_loop
    async def test_request_paper_questionnaire_people_in_household_31_spg_ni(self):
        await self.check_get_enter_address(self.get_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_enter_address(self.post_request_paper_questionnaire_enter_address_ni, 'ni')
        await self.check_post_select_address(self.post_request_paper_questionnaire_select_address_ni, 'ni', 'SPG')
        await self.check_post_confirm_address_input_yes_form(
            self.post_request_paper_questionnaire_confirm_address_ni, 'ni', self.rhsvc_case_by_uprn_spg_n)
        await self.check_post_household_information_form(
            self.post_request_paper_questionnaire_household_ni, 'ni')
        await self.check_post_people_in_household_invalid(
            self.post_request_paper_questionnaire_people_in_household_ni, 'ni', '31')
