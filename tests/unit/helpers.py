from unittest import mock

from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses

from . import RHTestCase

attempts_retry_limit = 5


# noinspection PyTypeChecker
class TestHelpers(RHTestCase):
    # Tests of pages/steps in all paths

    user_journey = ''
    sub_user_journey = ''

    def get_logo(self, display_region):
        if display_region == 'ni':
            logo = self.nisra_logo
        elif display_region == 'cy':
            logo = self.ons_logo_cy
        else:
            logo = self.ons_logo_en
        return logo

    def build_url_log_entry(self, page, display_region, request_type, include_sub_user_journey=True):
        if not include_sub_user_journey:
            link = "received " + request_type + " on endpoint '" + display_region + "/" + self.user_journey + "/" + \
                   page + "'"
        else:
            link = "received " + request_type + " on endpoint '" + display_region + "/" + self.user_journey + "/" + \
                   self.sub_user_journey + "/" + page + "'"
        return link

    def build_translation_link(self, page, display_region, include_sub_user_journey=True):
        if display_region == 'cy':
            if not include_sub_user_journey:
                link = '<a href="/en/' + self.user_journey + '/' + page + '/" lang="en" >English</a>'
            else:
                link = '<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/' + page + \
                       '/" lang="en" >English</a>'
        else:
            if not include_sub_user_journey:
                link = '<a href="/cy/' + self.user_journey + '/' + page + '/" lang="cy" >Cymraeg</a>'
            else:
                link = '<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/' + page + \
                       '/" lang="cy" >Cymraeg</a>'
        return link

    def check_text_enter_address(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if check_error:
                self.assertIn(self.content_common_enter_address_error_empty_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)
        else:
            if check_error:
                self.assertIn(self.content_common_enter_address_error_empty_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

    def check_text_select_address(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if check_error:
                self.assertIn(self.content_common_select_address_error_cy, contents)
            self.assertIn(self.content_common_select_address_title_cy, contents)
            self.assertIn(self.content_common_select_address_value_cy, contents)
        else:
            if check_error:
                self.assertIn(self.content_common_select_address_error_en, contents)
            self.assertIn(self.content_common_select_address_title_en, contents)
            self.assertIn(self.content_common_select_address_value_en, contents)

    def check_text_confirm_address(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if check_error:
                self.assertIn(self.content_common_confirm_address_error_cy, contents)
            self.assertIn(self.content_common_confirm_address_title_cy, contents)
            self.assertIn(self.content_common_confirm_address_value_yes_cy, contents)
            self.assertIn(self.content_common_confirm_address_value_no_cy, contents)
        else:
            if check_error:
                self.assertIn(self.content_common_confirm_address_error_en, contents)
            self.assertIn(self.content_common_confirm_address_title_en, contents)
            self.assertIn(self.content_common_confirm_address_value_yes_en, contents)
            self.assertIn(self.content_common_confirm_address_value_no_en, contents)

    def check_text_enter_mobile(self, display_region, contents):
        if display_region == 'cy':
            self.assertIn(self.content_request_code_enter_mobile_title_cy, contents)
            self.assertIn(self.content_request_code_enter_mobile_secondary_cy, contents)
        else:
            self.assertIn(self.content_request_code_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_code_enter_mobile_secondary_en, contents)

    def check_text_confirm_mobile(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if check_error:
                self.assertIn(self.content_request_code_confirm_mobile_error_cy, contents)
            self.assertIn(self.content_request_code_confirm_mobile_title_cy, contents)
        else:
            if check_error:
                self.assertIn(self.content_request_code_confirm_mobile_error_en, contents)
            self.assertIn(self.content_request_code_confirm_mobile_title_en, contents)

    def check_text_error_500(self, display_region, contents):
        if display_region == 'cy':
            self.assertIn(self.content_common_500_error_cy, contents)
        else:
            self.assertIn(self.content_common_500_error_en, contents)

    async def check_get_enter_address(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-address', display_region), contents)
            self.check_text_enter_address(display_region, contents, check_error=False)

    async def check_post_enter_address(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request('POST', url, data=self.common_postcode_input_valid)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'valid postcode')
            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('select-address', display_region), contents)
            self.check_text_select_address(display_region, contents, check_error=False)

    async def check_post_enter_address_input_returns_no_results(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request('POST', url, data=self.common_postcode_input_valid)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'valid postcode')
            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('select-address', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_select_address_no_results_cy, contents)
            else:
                self.assertIn(self.content_common_select_address_no_results_en, contents)

    async def check_post_enter_address_input_empty(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_postcode_input_empty)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'invalid postcode')
            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-address', display_region), contents)
            self.check_text_enter_address(display_region, contents, check_error=True)

    async def check_post_enter_address_input_invalid(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_postcode_input_invalid)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'invalid postcode')
            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-address', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_enter_address_error_cy, contents)
                self.assertIn(self.content_request_enter_address_title_cy, contents)
                self.assertIn(self.content_request_enter_address_secondary_cy, contents)
            else:
                self.assertIn(self.content_common_enter_address_error_en, contents)
                self.assertIn(self.content_request_enter_address_title_en, contents)
                self.assertIn(self.content_request_enter_address_secondary_en, contents)

    async def check_post_select_address_no_selection_made(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request('POST', url, data=self.common_form_data_empty)

            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'no address selected')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('select-address', display_region), contents)
            self.check_text_select_address(display_region, contents, check_error=True)

    async def check_post_select_address(self, url, display_region, ai_uprn_return_value=None):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            if ai_uprn_return_value:
                mocked_get_ai_uprn.return_value = ai_uprn_return_value
            else:
                mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request('POST', url, data=self.common_select_address_input_valid)

            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('confirm-address', display_region), contents)
            self.check_text_confirm_address(display_region, contents, check_error=False)

    async def check_post_select_address_address_not_found(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_select_address_input_not_listed_en)

            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('call-contact-centre/address-not-found',
                                                             display_region, 'GET', False))
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('call-contact-centre/address-not-found',
                                                          display_region, False), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, contents)
            else:
                self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    async def check_post_confirm_address_input_invalid_or_no_selection(self, url, display_region, data):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request('POST', url, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, "address confirmation error")
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('confirm-address', display_region), contents)
            self.check_text_confirm_address(display_region, contents, check_error=True)

    async def check_post_confirm_address_input_no(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'GET'))

            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-address', display_region), contents)
            self.check_text_enter_address(display_region, contents, check_error=False)

    async def check_post_confirm_address_input_yes(self, url, display_region, case_by_uprn_return):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
                'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = case_by_uprn_return

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET'))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-mobile', display_region), contents)
            self.check_text_enter_mobile(display_region, contents)

    async def check_post_confirm_address_address_in_scotland(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('address-in-scotland', display_region, 'GET', False))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('address-in-scotland', display_region, False), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_address_in_scotland_cy, contents)
            else:
                self.assertIn(self.content_common_address_in_scotland_en, contents)

    async def check_post_confirm_address_returns_addresstype_na(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('call-contact-centre/unable-to-match-address',
                                                             display_region, 'GET', False))

            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('call-contact-centre/unable-to-match-address',
                                                          display_region, False), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_call_contact_centre_title_cy, contents)
                self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_cy, contents)
            else:
                self.assertIn(self.content_common_call_contact_centre_title_en, contents)
                self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, contents)

    async def check_post_confirm_address_error_from_get_cases(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_get_case_by_uprn:

            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_enter_mobile(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-mobile', display_region, 'GET'))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('confirm-mobile', display_region), contents)
            self.check_text_confirm_mobile(display_region, contents, check_error=False)

    async def check_post_enter_mobile_input_invalid(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-mobile', display_region), contents)
            self.check_text_enter_mobile(display_region, contents)

    async def check_post_confirm_mobile(self, url, display_region, case_type, region, individual):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_sms
            mocked_request_fulfilment_sms.return_value = self.rhsvc_request_fulfilment_sms

            response = await self.client.request('POST', url, data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-mobile', display_region, 'POST'))
            self.assertLogEvent(cm, "fulfilment query: case_type=" + case_type + ", region=" + region +
                                ", individual=" + individual)
            self.assertLogEvent(cm, self.build_url_log_entry('code-sent-sms', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('code-sent-sms', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_code_sent_sms_title_cy, contents)
                if individual == 'true':
                    self.assertIn(self.content_request_code_sent_sms_secondary_individual_cy, contents)
                elif case_type == 'CE':
                    self.assertIn(self.content_request_code_sent_sms_secondary_manager_cy, contents)
                else:
                    self.assertIn(self.content_request_code_sent_sms_secondary_household_cy, contents)
            else:
                self.assertIn(self.content_request_code_sent_sms_title_en, contents)
                if individual == 'true':
                    self.assertIn(self.content_request_code_sent_sms_secondary_individual_en, contents)
                elif case_type == 'CE':
                    self.assertIn(self.content_request_code_sent_sms_secondary_manager_en, contents)
                else:
                    self.assertIn(self.content_request_code_sent_sms_secondary_household_en, contents)

    async def check_post_confirm_mobile_error_from_get_fulfilment(self, url, display_region,
                                                                  case_type, region, individual):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=' + case_type + '&region=' + region +
                                    '&deliveryChannel=SMS&productGroup=UAC&individual=' + individual, status=400)

            response = await self.client.request('POST', url, data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-mobile', display_region, 'POST'))
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_confirm_mobile_input_no(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-mobile', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-mobile', display_region), contents)
            self.check_text_enter_mobile(display_region, contents)

    async def check_post_confirm_mobile_error_from_request_fulfilment(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_sms
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            response = await self.client.request('POST', url, data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-mobile', display_region, 'POST'))
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_confirm_mobile_input_invalid_or_no_selection(self, url, display_region, data):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-mobile', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('confirm-mobile', display_region), contents)
            self.check_text_confirm_mobile(display_region, contents, check_error=True)

    async def check_post_enter_address_error_from_ai(self, url, display_region, status):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=status)

            response = await self.client.request('POST', url, data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=status)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    def mock_ai_503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

    async def check_post_enter_address_error_503_from_ai(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock_ai_503s(mocked, attempts_retry_limit)

            response = await self.client.request('POST', url, data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_enter_address_connection_error_from_ai(self, url, display_region, epoch=None):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            if epoch:
                self.app['ADDRESS_INDEX_EPOCH'] = epoch
                param = self.address_index_epoch_param_test
            else:
                param = self.address_index_epoch_param

            response = await self.client.request('POST', url, data=self.common_postcode_input_valid)

            self.assertLogEvent(cm, 'client failed to connect', url=self.addressindexsvc_url +
                                self.postcode_valid + param)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.get_logo(display_region), contents)
        self.check_text_error_500(display_region, contents)

    async def check_get_timeout(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, self.build_url_log_entry('timeout', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('timeout', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_timeout_cy, contents)
                self.assertIn(self.content_request_timeout_error_cy, contents)
            else:
                self.assertIn(self.content_common_timeout_en, contents)
                self.assertIn(self.content_request_timeout_error_en, contents)
