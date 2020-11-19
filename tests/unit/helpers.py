import datetime
import json

from urllib.parse import urlsplit, parse_qs
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

    def build_url_log_entry(self, page, display_region, request_type, include_sub_user_journey=True, include_page=True):
        if not include_page:
            link = "received " + request_type + " on endpoint '" + display_region + "/" + self.user_journey
        elif not include_sub_user_journey:
            link = "received " + request_type + " on endpoint '" + display_region + "/" + self.user_journey + "/" + \
                   page + "'"
        else:
            link = "received " + request_type + " on endpoint '" + display_region + "/" + self.user_journey + "/" + \
                   self.sub_user_journey + "/" + page + "'"
        return link

    def build_translation_link(self, page, display_region, include_sub_user_journey=True, include_page=True,
                               include_adlocation=False):
        if display_region == 'cy':
            if not include_page:
                if include_adlocation:
                    link = '<a href="/en/' + self.user_journey + '/?adlocation=' + self.adlocation + \
                           '" lang="en" >English</a>'
                else:
                    link = '<a href="/en/' + self.user_journey + '/" lang="en" >English</a>'
            elif not include_sub_user_journey:
                link = '<a href="/en/' + self.user_journey + '/' + page + '/" lang="en" >English</a>'
            else:
                link = '<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/' + page + \
                       params + '" lang="en" >English</a>'
        else:
            if not include_page:
                if include_adlocation:
                    link = '<a href="/cy/' + self.user_journey + '/?adlocation=' + self.adlocation + \
                           '" lang="cy" >Cymraeg</a>'
                else:
                    link = '<a href="/cy/' + self.user_journey + '/" lang="cy" >Cymraeg</a>'
            elif not include_sub_user_journey:
                link = '<a href="/cy/' + self.user_journey + '/' + page + '/" lang="cy" >Cymraeg</a>'
            else:
                link = '<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/' + page + \
                       params + '" lang="cy" >Cymraeg</a>'
        return link

    def check_text_enter_address(self, display_region, contents, check_empty=False, check_error=False):
        if display_region == 'cy':
            if check_empty:
                self.assertIn(self.content_common_enter_address_error_empty_cy, contents)
            if check_error:
                self.assertIn(self.content_common_enter_address_error_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            if self.sub_user_journey == 'paper-form':
                self.assertIn(self.content_request_form_enter_address_secondary_cy, contents)
            elif self.sub_user_journey == 'individual-code':
                self.assertIn(self.content_request_individual_code_enter_address_secondary_cy, contents)
            else:
                self.assertIn(self.content_request_access_code_enter_address_secondary_cy, contents)
        else:
            if check_empty:
                self.assertIn(self.content_common_enter_address_error_empty_en, contents)
            if check_error:
                self.assertIn(self.content_common_enter_address_error_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            if self.sub_user_journey == 'paper-form':
                self.assertIn(self.content_request_form_enter_address_secondary_en, contents)
            elif self.sub_user_journey == 'individual-code':
                self.assertIn(self.content_request_individual_code_enter_address_secondary_en, contents)
            else:
                self.assertIn(self.content_request_access_code_enter_address_secondary_en, contents)

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

    def check_text_confirm_address(self, display_region, contents, check_error=False, check_ce=False,
                                   check_room_number=False):
        if display_region == 'cy':
            if check_error:
                self.assertIn(self.content_common_confirm_address_error_cy, contents)
            self.assertIn(self.content_common_confirm_address_title_cy, contents)
            self.assertIn(self.content_common_confirm_address_value_yes_cy, contents)
            self.assertIn(self.content_common_confirm_address_value_no_cy, contents)
            if check_ce:
                if check_room_number:
                    self.assertIn(self.content_common_ce_room_number_text, contents)
                    self.assertIn(self.content_common_ce_room_number_change_link_cy, contents)
                    self.assertNotIn(self.content_common_ce_room_number_add_link_cy, contents)
                else:
                    self.assertNotIn(self.content_common_ce_room_number_text, contents)
                    self.assertNotIn(self.content_common_ce_room_number_change_link_cy, contents)
                    self.assertIn(self.content_common_ce_room_number_add_link_cy, contents)
            else:
                self.assertNotIn(self.content_common_ce_room_number_text, contents)
                self.assertNotIn(self.content_common_ce_room_number_change_link_cy, contents)
                self.assertNotIn(self.content_common_ce_room_number_add_link_cy, contents)
        else:
            if check_error:
                self.assertIn(self.content_common_confirm_address_error_en, contents)
            self.assertIn(self.content_common_confirm_address_title_en, contents)
            self.assertIn(self.content_common_confirm_address_value_yes_en, contents)
            self.assertIn(self.content_common_confirm_address_value_no_en, contents)
            if check_ce:
                if check_room_number:
                    self.assertIn(self.content_common_ce_room_number_text, contents)
                    self.assertIn(self.content_common_ce_room_number_change_link_en, contents)
                    self.assertNotIn(self.content_common_ce_room_number_add_link_en, contents)
                else:
                    self.assertNotIn(self.content_common_ce_room_number_text, contents)
                    self.assertNotIn(self.content_common_ce_room_number_change_link_en, contents)
                    self.assertIn(self.content_common_ce_room_number_add_link_en, contents)
            else:
                self.assertNotIn(self.content_common_ce_room_number_text, contents)
                self.assertNotIn(self.content_common_ce_room_number_change_link_en, contents)
                self.assertNotIn(self.content_common_ce_room_number_add_link_en, contents)

    def check_text_select_method(self, display_region, contents, user_type, check_error=False):
        if display_region == 'cy':
            if check_error:
                self.assertIn(self.content_request_code_select_method_error_cy, contents)
            if user_type == 'individual':
                self.assertIn(self.content_request_code_select_method_individual_title_cy, contents)
            elif user_type == 'manager':
                self.assertIn(self.content_request_code_select_method_manager_title_cy, contents)
            else:
                self.assertIn(self.content_request_code_select_method_household_title_cy, contents)
            self.assertIn(self.content_request_code_select_method_secondary_cy, contents)
            self.assertIn(self.content_request_code_select_method_option_text_cy, contents)
            self.assertIn(self.content_request_code_select_method_option_post_cy, contents)
        else:
            if check_error:
                self.assertIn(self.content_request_code_select_method_error_en, contents)
            if user_type == 'individual':
                self.assertIn(self.content_request_code_select_method_individual_title_en, contents)
            elif user_type == 'manager':
                self.assertIn(self.content_request_code_select_method_manager_title_en, contents)
            else:
                self.assertIn(self.content_request_code_select_method_household_title_en, contents)
            self.assertIn(self.content_request_code_select_method_secondary_en, contents)
            self.assertIn(self.content_request_code_select_method_option_text_en, contents)
            self.assertIn(self.content_request_code_select_method_option_post_en, contents)

    def check_text_resident_or_manager(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if check_error:
                self.assertIn(self.content_common_resident_or_manager_error_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_title_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_cy, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_cy, contents)
        else:
            if check_error:
                self.assertIn(self.content_common_resident_or_manager_error_en, contents)
            self.assertIn(self.content_common_resident_or_manager_title_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_resident_en, contents)
            self.assertIn(self.content_common_resident_or_manager_option_manager_en, contents)
            self.assertIn(self.content_common_resident_or_manager_description_manager_en, contents)

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

    def check_text_confirm_name_address(self, display_region, contents, user_type, check_error=False,
                                        override_sub_user_journey=False, check_ce=False, check_room_number=False):
        if display_region == 'cy':
            if check_error:
                self.assertIn(self.content_request_common_confirm_name_address_error_cy, contents)
            if (self.sub_user_journey == 'paper-form') and (override_sub_user_journey is False):
                self.assertIn(self.content_request_form_confirm_name_address_title_cy, contents)
                self.assertNotIn(self.content_request_common_confirm_name_address_individual_message_cy, contents)
            elif user_type == 'individual':
                self.assertIn(self.content_request_common_confirm_name_address_title_individual_cy, contents)
                self.assertIn(self.content_request_common_confirm_name_address_individual_message_cy, contents)
            elif user_type == 'manager':
                self.assertIn(self.content_request_common_confirm_name_address_title_manager_cy, contents)
                self.assertNotIn(self.content_request_common_confirm_name_address_individual_message_cy, contents)
            else:
                self.assertIn(self.content_request_common_confirm_name_address_title_household_cy, contents)
                self.assertNotIn(self.content_request_common_confirm_name_address_individual_message_cy, contents)

            if check_ce:
                if check_room_number:
                    self.assertIn(self.content_common_ce_room_number_text, contents)
                    self.assertIn(self.content_common_ce_room_number_change_link_cy, contents)
                    self.assertNotIn(self.content_common_ce_room_number_add_link_cy, contents)
                else:
                    self.assertNotIn(self.content_common_ce_room_number_text, contents)
                    self.assertNotIn(self.content_common_ce_room_number_change_link_cy, contents)
                    self.assertIn(self.content_common_ce_room_number_add_link_cy, contents)
            else:
                self.assertNotIn(self.content_common_ce_room_number_text, contents)
                self.assertNotIn(self.content_common_ce_room_number_change_link_cy, contents)
                self.assertNotIn(self.content_common_ce_room_number_add_link_cy, contents)

            if (self.sub_user_journey == 'paper-form') and (override_sub_user_journey is False):
                self.assertIn(self.content_request_form_confirm_name_address_option_yes_cy, contents)
                self.assertIn(self.content_request_form_confirm_name_address_option_no_cy, contents)
                self.assertIn(self.content_request_form_confirm_name_address_large_print_checkbox_cy, contents)
            else:
                self.assertIn(self.content_request_common_confirm_name_address_option_yes_cy, contents)
                self.assertIn(self.content_request_common_confirm_name_address_option_no_cy, contents)
        else:
            if check_error:
                self.assertIn(self.content_request_common_confirm_name_address_error_en, contents)
            if (self.sub_user_journey == 'paper-form') and (override_sub_user_journey is False):
                self.assertIn(self.content_request_form_confirm_name_address_title_en, contents)
                self.assertNotIn(self.content_request_common_confirm_name_address_individual_message_en, contents)
            elif user_type == 'individual':
                self.assertIn(self.content_request_common_confirm_name_address_title_individual_en, contents)
                self.assertIn(self.content_request_common_confirm_name_address_individual_message_en, contents)
            elif user_type == 'manager':
                self.assertIn(self.content_request_common_confirm_name_address_title_manager_en, contents)
                self.assertNotIn(self.content_request_common_confirm_name_address_individual_message_en, contents)
            else:
                self.assertIn(self.content_request_common_confirm_name_address_title_household_en, contents)
                self.assertNotIn(self.content_request_common_confirm_name_address_individual_message_en, contents)

            if check_ce:
                if check_room_number:
                    self.assertIn(self.content_common_ce_room_number_text, contents)
                    self.assertIn(self.content_common_ce_room_number_change_link_en, contents)
                    self.assertNotIn(self.content_common_ce_room_number_add_link_en, contents)
                else:
                    self.assertNotIn(self.content_common_ce_room_number_text, contents)
                    self.assertNotIn(self.content_common_ce_room_number_change_link_en, contents)
                    self.assertIn(self.content_common_ce_room_number_add_link_en, contents)
            else:
                self.assertNotIn(self.content_common_ce_room_number_text, contents)
                self.assertNotIn(self.content_common_ce_room_number_change_link_en, contents)
                self.assertNotIn(self.content_common_ce_room_number_add_link_en, contents)

            if (self.sub_user_journey == 'paper-form') and (override_sub_user_journey is False):
                self.assertIn(self.content_request_form_confirm_name_address_option_yes_en, contents)
                self.assertIn(self.content_request_form_confirm_name_address_option_no_en, contents)
                self.assertIn(self.content_request_form_confirm_name_address_large_print_checkbox_en, contents)
            else:
                self.assertIn(self.content_request_common_confirm_name_address_option_yes_en, contents)
                self.assertIn(self.content_request_common_confirm_name_address_option_no_en, contents)

    def check_text_error_500(self, display_region, contents):
        if display_region == 'cy':
            self.assertIn(self.content_common_500_error_cy, contents)
        else:
            self.assertIn(self.content_common_500_error_en, contents)

    def check_text_enter_room_number(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            self.assertIn(self.content_common_enter_room_number_title_cy, contents)
            if check_error:
                self.assertIn(self.content_common_enter_room_number_error_cy, contents)
        else:
            self.assertIn(self.content_common_enter_room_number_title_en, contents)
            if check_error:
                self.assertIn(self.content_common_enter_room_number_error_en, contents)

    async def check_get_enter_address(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-address', display_region), contents)
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=False)

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
            self.check_text_enter_address(display_region, contents, check_empty=True, check_error=False)

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
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=True)

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

    async def check_post_select_address(self, url, display_region, address_type, ai_uprn_return_value=None):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            if ai_uprn_return_value:
                mocked_get_ai_uprn.return_value = ai_uprn_return_value
            elif display_region == 'ni':
                if address_type == 'CE':
                    mocked_get_ai_uprn.return_value = self.ai_uprn_result_northern_ireland_ce
                else:
                    mocked_get_ai_uprn.return_value = self.ai_uprn_result_northern_ireland
            else:
                if address_type == 'CE':
                    mocked_get_ai_uprn.return_value = self.ai_uprn_result_ce
                elif address_type == 'SPG':
                    mocked_get_ai_uprn.return_value = self.ai_uprn_result_spg
                else:
                    mocked_get_ai_uprn.return_value = self.ai_uprn_result_hh

            response = await self.client.request('POST', url, data=self.common_select_address_input_valid)

            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('confirm-address', display_region), contents)
            if address_type == 'CE':
                self.check_text_confirm_address(display_region, contents, check_error=False, check_ce=True)
            else:
                self.check_text_confirm_address(display_region, contents, check_error=False, check_ce=False)

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
            if display_region == 'ni':
                self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)
                self.assertIn(self.content_call_centre_number_ni, contents)
            elif display_region == 'cy':
                self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, contents)
                self.assertIn(self.content_call_centre_number_cy, contents)
            else:
                self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)
                self.assertIn(self.content_call_centre_number_ew, contents)

    async def check_post_confirm_address_input_invalid_or_no_selection(self, url, display_region, data, is_ce=False):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_hh

            response = await self.client.request('POST', url, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, "address confirmation error")
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('confirm-address', display_region), contents)
            if is_ce:
                self.check_text_confirm_address(display_region, contents, check_error=True, check_ce=True)
            else:
                self.check_text_confirm_address(display_region, contents, check_error=True, check_ce=False)

    async def check_post_confirm_address_input_no(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_hh

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'GET'))

            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-address', display_region), contents)
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=False)

    async def check_post_confirm_address_input_yes(self, url, display_region, case_by_uprn_return, user_type):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn:

            mocked_get_case_by_uprn.return_value = case_by_uprn_return

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('select-method', display_region, 'GET'))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('select-method', display_region), contents)
            self.check_text_select_method(display_region, contents, user_type)

    async def check_post_confirm_address_input_yes_new_case(self, url, display_region, create_case_return, user_type):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.RHService.post_case_create') as mocked_post_case_create, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            if display_region == 'ni':
                mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn_ni, status=404)
            else:
                mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)
            mocked_post_case_create.return_value = create_case_return

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'get cases by uprn error - unable to match uprn (404)')
            self.assertLogEvent(cm, 'requesting new case')
            self.assertLogEvent(cm, self.build_url_log_entry('select-method', display_region, 'GET'))

            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('select-method', display_region), contents)
            self.check_text_select_method(display_region, contents, user_type)

    async def check_post_confirm_address_input_yes_form(self, url, display_region, case_by_uprn_return):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn:

            mocked_get_case_by_uprn.return_value = case_by_uprn_return

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-name', display_region, 'GET'))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-name', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_common_enter_name_title_cy, contents)
            else:
                self.assertIn(self.content_request_common_enter_name_title_en, contents)

    async def check_post_confirm_address_input_yes_form_new_case(self, url, display_region, create_case_return):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.RHService.post_case_create') as mocked_post_case_create, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            if display_region == 'ni':
                mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn_ni, status=404)
            else:
                mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)
            mocked_post_case_create.return_value = create_case_return

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'get cases by uprn error - unable to match uprn (404)')
            self.assertLogEvent(cm, 'requesting new case')
            self.assertLogEvent(cm, self.build_url_log_entry('enter-name', display_region, 'GET'))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-name', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_common_enter_name_title_cy, contents)
            else:
                self.assertIn(self.content_request_common_enter_name_title_en, contents)

    async def check_post_confirm_address_input_yes_ce(self, url, display_region, case_by_uprn_return):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn:

            mocked_get_case_by_uprn.return_value = case_by_uprn_return

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('resident-or-manager', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('resident-or-manager', display_region), contents)
            self.check_text_resident_or_manager(display_region, contents)

    async def check_post_confirm_address_input_yes_ce_new_case(self, url, display_region, create_case_return):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.RHService.post_case_create') as mocked_post_case_create, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            if display_region == 'ni':
                mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn_ni, status=404)
            else:
                mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)
            mocked_post_case_create.return_value = create_case_return

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'get cases by uprn error - unable to match uprn (404)')
            self.assertLogEvent(cm, 'requesting new case')
            self.assertLogEvent(cm, self.build_url_log_entry('resident-or-manager', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('resident-or-manager', display_region), contents)
            self.check_text_resident_or_manager(display_region, contents)

    async def check_post_confirm_address_address_in_northern_ireland(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('address-in-northern-ireland', display_region, 'GET',
                                                             False))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('address-in-northern-ireland', display_region, False),
                              contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_address_in_northern_ireland_cy, contents)
            else:
                self.assertIn(self.content_common_address_in_northern_ireland_en, contents)

    async def check_post_confirm_address_address_in_england(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('address-in-england', display_region, 'GET',
                                                             False))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.content_common_address_not_in_northern_ireland, contents)
            self.assertIn(self.content_common_address_in_england_secondary, contents)

    async def check_post_confirm_address_address_in_wales(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('address-in-wales', display_region, 'GET',
                                                             False))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.content_common_address_not_in_northern_ireland, contents)
            self.assertIn(self.content_common_address_in_wales_secondary, contents)

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
            if display_region == 'ni':
                self.assertIn(self.content_common_call_contact_centre_title_en, contents)
                self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, contents)
                self.assertIn(self.content_call_centre_number_ni, contents)
            elif display_region == 'cy':
                self.assertIn(self.content_common_call_contact_centre_title_cy, contents)
                self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_cy, contents)
                self.assertIn(self.content_call_centre_number_cy, contents)
            else:
                self.assertIn(self.content_common_call_contact_centre_title_en, contents)
                self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, contents)
                self.assertIn(self.content_call_centre_number_ew, contents)

    async def check_post_confirm_address_error_from_get_cases(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_get_case_by_uprn:

            if display_region == 'ni':
                mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn_ni, status=400)
            else:
                mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_confirm_address_error_from_create_case(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_rhsvc:

            if display_region == 'ni':
                mocked_rhsvc.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn_ni, status=404)
            else:
                mocked_rhsvc.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)
            mocked_rhsvc.post(self.rhsvc_post_create_case_url, status=400)

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'get cases by uprn error - unable to match uprn (404)')
            self.assertLogEvent(cm, 'requesting new case')
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_get_select_method_form_manager(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, self.build_url_log_entry('access-code/select-method',
                                                             display_region, 'GET', False))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('access-code/select-method', display_region, False),
                              contents)
            self.check_text_select_method(display_region, contents, 'manager')

    async def check_post_select_method_input_sms(self, url, display_region, override_sub_user_journey=None):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=self.request_code_select_method_data_sms)
            if override_sub_user_journey:
                self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/select-method',
                                                                 display_region, 'POST', False))
                self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/enter-mobile',
                                                                 display_region, 'GET', False))
            else:
                self.assertLogEvent(cm, self.build_url_log_entry('select-method', display_region, 'POST'))
                self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET'))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                if override_sub_user_journey:
                    self.assertIn(self.build_translation_link(override_sub_user_journey + '/enter-mobile',
                                                              display_region, False), contents)
                else:
                    self.assertIn(self.build_translation_link('enter-mobile', display_region), contents)
            self.check_text_enter_mobile(display_region, contents)

    async def check_post_select_method_input_post(self, url, display_region, override_sub_user_journey=None):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=self.request_code_select_method_data_post)
            if override_sub_user_journey:
                self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/select-method',
                                                                 display_region, 'POST', False))
                self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/enter-name',
                                                                 display_region, 'GET', False))
            else:
                self.assertLogEvent(cm, self.build_url_log_entry('select-method', display_region, 'POST'))
                self.assertLogEvent(cm, self.build_url_log_entry('enter-name', display_region, 'GET'))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                if override_sub_user_journey:
                    self.assertIn(self.build_translation_link(override_sub_user_journey + '/enter-name',
                                                              display_region, False), contents)
                else:
                    self.assertIn(self.build_translation_link('enter-name', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_common_enter_name_title_cy, contents)
            else:
                self.assertIn(self.content_request_common_enter_name_title_en, contents)

    async def check_post_select_method_input_invalid_or_no_selection(self, url, display_region, data, user_type):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('select-method', display_region, 'POST'))
            self.assertLogEvent(cm, "request method selection error")
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('select-method', display_region), contents)
            self.check_text_select_method(display_region, contents, user_type, check_error=True)

    async def check_post_resident_or_manager(self, url, display_region, data, user_type):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('resident-or-manager', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('select-method', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('select-method', display_region), contents)
            self.check_text_select_method(display_region, contents, user_type)

    async def check_post_resident_or_manager_form_resident(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_resident_or_manager_input_resident)
            self.assertLogEvent(cm, self.build_url_log_entry('resident-or-manager', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-name', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-name', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_common_enter_name_title_cy, contents)
            else:
                self.assertIn(self.content_request_common_enter_name_title_en, contents)

    async def check_post_resident_or_manager_form_manager(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_resident_or_manager_input_manager)
            self.assertLogEvent(cm, self.build_url_log_entry('resident-or-manager', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('form-manager', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('form-manager', display_region), contents)
            if display_region == 'ni':
                self.assertIn(self.content_request_form_manager_title_en, contents)
                self.assertIn(self.content_call_centre_number_ni, contents)
            elif display_region == 'cy':
                self.assertIn(self.content_request_form_manager_title_cy, contents)
                self.assertIn(self.content_call_centre_number_cy, contents)
            else:
                self.assertIn(self.content_request_form_manager_title_en, contents)
                self.assertIn(self.content_call_centre_number_ew, contents)

    async def check_post_resident_or_manager_input_invalid_or_no_selection(self, url, display_region, data):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('resident-or-manager', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('resident-or-manager', display_region), contents)
            self.check_text_resident_or_manager(display_region, contents, check_error=True)

    async def check_post_enter_mobile(self, url, display_region, override_sub_user_journey=None):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=self.request_code_enter_mobile_form_data_valid)
            if override_sub_user_journey:
                self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/enter-mobile',
                                                                 display_region, 'POST', False))
                self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/confirm-mobile',
                                                                 display_region, 'GET', False))
            else:
                self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST'))
                self.assertLogEvent(cm, self.build_url_log_entry('confirm-mobile', display_region, 'GET'))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                if override_sub_user_journey:
                    self.assertIn(self.build_translation_link(override_sub_user_journey + '/confirm-mobile',
                                                              display_region, False), contents)
                else:
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

    async def check_post_confirm_mobile(self, url, display_region, case_type, region, individual,
                                        override_sub_user_journey=None):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_sms
            mocked_request_fulfilment_sms.return_value = self.rhsvc_request_fulfilment_sms

            response = await self.client.request('POST', url, data=self.request_code_mobile_confirmation_data_yes)
            if override_sub_user_journey:
                self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/confirm-mobile',
                                                                 display_region, 'POST', False))
            else:
                self.assertLogEvent(cm, self.build_url_log_entry('confirm-mobile', display_region, 'POST'))
            self.assertLogEvent(cm, "fulfilment query: case_type=" + case_type + ", region=" + region +
                                ", individual=" + individual)
            if override_sub_user_journey:
                self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/code-sent-sms',
                                                                 display_region, 'GET', False))
            else:
                self.assertLogEvent(cm, self.build_url_log_entry('code-sent-sms', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                if override_sub_user_journey:
                    self.assertIn(self.build_translation_link(override_sub_user_journey + '/code-sent-sms',
                                                              display_region, False), contents)
                else:
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

    async def check_post_confirm_mobile_error_429_from_request_fulfilment(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_sms
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=429)

            response = await self.client.request('POST', url, data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-mobile', display_region, 'POST'))
            self.assertLogEvent(cm, 'error in response', status_code=429)

            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_429_error_uac_title_cy, contents)
            else:
                self.assertIn(self.content_common_429_error_uac_title_en, contents)

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

    async def check_post_enter_name(self, url, display_region, user_type, case_type, override_sub_user_journey=None,
                                    check_room_number=False, long_surname=False):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            if long_surname:
                response = await self.client.request('POST', url,
                                                     data=self.request_common_enter_name_form_data_long_surname)
            else:
                response = await self.client.request('POST', url, data=self.request_common_enter_name_form_data_valid)
            if override_sub_user_journey:
                self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/enter-name',
                                                                 display_region, 'POST', False))
                self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/confirm-name-address',
                                                                 display_region, 'GET', False))
            else:
                self.assertLogEvent(cm, self.build_url_log_entry('enter-name', display_region, 'POST'))
                self.assertLogEvent(cm, self.build_url_log_entry('confirm-name-address', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)

            if not display_region == 'ni':
                if override_sub_user_journey:
                    self.assertIn(self.build_translation_link(override_sub_user_journey + '/confirm-name-address',
                                                              display_region, False), contents)
                else:
                    self.assertIn(self.build_translation_link('confirm-name-address', display_region), contents)

            if override_sub_user_journey:
                if case_type == 'CE':
                    if check_room_number:
                        self.check_text_confirm_name_address(display_region, contents, user_type, check_error=False,
                                                             override_sub_user_journey=True, check_ce=True,
                                                             check_room_number=True)
                    else:
                        self.check_text_confirm_name_address(display_region, contents, user_type, check_error=False,
                                                             override_sub_user_journey=True, check_ce=True,
                                                             check_room_number=False)
                else:
                    self.check_text_confirm_name_address(display_region, contents, user_type, check_error=False,
                                                         override_sub_user_journey=True, check_ce=False)
            else:
                if case_type == 'CE':
                    if check_room_number:
                        self.check_text_confirm_name_address(display_region, contents, user_type, check_error=False,
                                                             override_sub_user_journey=False, check_ce=True,
                                                             check_room_number=True)
                    else:
                        self.check_text_confirm_name_address(display_region, contents, user_type, check_error=False,
                                                             override_sub_user_journey=False, check_ce=True,
                                                             check_room_number=False)
                else:
                    self.check_text_confirm_name_address(display_region, contents, user_type, check_error=False,
                                                         override_sub_user_journey=False, check_ce=False)

    async def check_post_enter_name_inputs_error(self, url, display_region, data, value_first=True, value_last=True):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-name', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-name', display_region), contents)
            if display_region == 'cy':
                if not value_first:
                    self.assertIn(self.content_request_common_enter_name_error_first_name_cy, contents)
                if not value_last:
                    self.assertIn(self.content_request_common_enter_name_error_last_name_cy, contents)
                self.assertIn(self.content_request_common_enter_name_title_cy, contents)
            else:
                if not value_first:
                    self.assertIn(self.content_request_common_enter_name_error_first_name_en, contents)
                if not value_last:
                    self.assertIn(self.content_request_common_enter_name_error_last_name_en, contents)
                self.assertIn(self.content_request_common_enter_name_title_en, contents)

    async def check_post_confirm_name_address_input_yes(self, url, display_region, case_type, fulfilment_type,
                                                        region, individual, override_sub_user_journey=None,
                                                        check_room_number=False, long_surname=False):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, \
                mock.patch('app.utils.RHService.request_fulfilment_post') as mocked_request_fulfilment_post:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            if fulfilment_type == 'LARGE_PRINT':
                data = self.request_common_confirm_name_address_data_yes_large_print
            else:
                data = self.request_common_confirm_name_address_data_yes
            response = await self.client.request('POST', url, data=data)

            if override_sub_user_journey:
                self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/confirm-name-address',
                                                                 display_region, 'POST', False))
            else:
                self.assertLogEvent(cm, self.build_url_log_entry('confirm-name-address', display_region, 'POST'))
            self.assertLogEvent(cm, "fulfilment query: case_type=" + case_type +
                                ", fulfilment_type=" + fulfilment_type +
                                ", region=" + region + ", individual=" + individual)
            if self.sub_user_journey == 'paper-form' and not override_sub_user_journey:
                if fulfilment_type == 'LARGE_PRINT':
                    self.assertLogEvent(cm, self.build_url_log_entry('large-print-sent-post', display_region, 'GET'))
                else:
                    self.assertLogEvent(cm, self.build_url_log_entry('form-sent-post', display_region, 'GET'))
            else:
                if override_sub_user_journey:
                    self.assertLogEvent(cm, self.build_url_log_entry(override_sub_user_journey + '/code-sent-post',
                                                                     display_region, 'GET', False))
                else:
                    self.assertLogEvent(cm, self.build_url_log_entry('code-sent-post', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if self.sub_user_journey == 'paper-form' and not override_sub_user_journey:
                if not display_region == 'ni':
                    if fulfilment_type == 'LARGE_PRINT':
                        self.assertIn(self.build_translation_link('large-print-sent-post', display_region), contents)
                    else:
                        self.assertIn(self.build_translation_link('form-sent-post', display_region), contents)
                if display_region == 'ni':
                    if fulfilment_type == 'LARGE_PRINT':
                        if case_type == 'CE':
                            if check_room_number:
                                if long_surname:
                                    self.assertIn(
                                        self.content_request_form_sent_post_title_lp_ce_with_room_long_surname_en,
                                        contents)
                                else:
                                    self.assertIn(self.content_request_form_sent_post_title_large_print_ce_with_room_en,
                                                  contents)
                            else:
                                self.assertIn(self.content_request_form_sent_post_title_large_print_ce_en, contents)
                        else:
                            self.assertIn(self.content_request_form_sent_post_title_large_print_ni, contents)
                    else:
                        if case_type == 'CE':
                            if check_room_number:
                                if long_surname:
                                    self.assertIn(
                                        self.content_request_form_sent_post_title_ce_with_room_long_surname_en,
                                        contents)
                                else:
                                    self.assertIn(self.content_request_form_sent_post_title_ce_with_room_en, contents)
                            else:
                                self.assertIn(self.content_request_form_sent_post_title_ce_en, contents)
                        else:
                            self.assertIn(self.content_request_form_sent_post_title_ni, contents)
                    self.assertIn(self.content_request_form_sent_post_secondary_en, contents)
                elif display_region == 'cy':
                    if fulfilment_type == 'LARGE_PRINT':
                        if case_type == 'CE':
                            if check_room_number:
                                if long_surname:
                                    self.assertIn(
                                        self.content_request_form_sent_post_title_lp_ce_with_room_long_surname_cy,
                                        contents)
                                else:
                                    self.assertIn(self.content_request_form_sent_post_title_large_print_ce_with_room_cy,
                                                  contents)
                            else:
                                self.assertIn(self.content_request_form_sent_post_title_large_print_ce_cy, contents)
                        else:
                            self.assertIn(self.content_request_form_sent_post_title_large_print_cy, contents)
                    else:
                        if case_type == 'CE':
                            if check_room_number:
                                if long_surname:
                                    self.assertIn(
                                        self.content_request_form_sent_post_title_ce_with_room_long_surname_cy,
                                        contents)
                                else:
                                    self.assertIn(self.content_request_form_sent_post_title_ce_with_room_cy, contents)
                            else:
                                self.assertIn(self.content_request_form_sent_post_title_ce_cy, contents)
                        else:
                            self.assertIn(self.content_request_form_sent_post_title_cy, contents)
                    self.assertIn(self.content_request_form_sent_post_secondary_cy, contents)
                else:
                    if fulfilment_type == 'LARGE_PRINT':
                        if case_type == 'CE':
                            if check_room_number:
                                if long_surname:
                                    self.assertIn(
                                        self.content_request_form_sent_post_title_lp_ce_with_room_long_surname_en,
                                        contents)
                                else:
                                    self.assertIn(self.content_request_form_sent_post_title_large_print_ce_with_room_en,
                                                  contents)
                            else:
                                self.assertIn(self.content_request_form_sent_post_title_large_print_ce_en, contents)
                        else:
                            self.assertIn(self.content_request_form_sent_post_title_large_print_en, contents)
                    else:
                        if case_type == 'CE':
                            if check_room_number:
                                if long_surname:
                                    self.assertIn(
                                        self.content_request_form_sent_post_title_ce_with_room_long_surname_en,
                                        contents)
                                else:
                                    self.assertIn(self.content_request_form_sent_post_title_ce_with_room_en, contents)
                            else:
                                self.assertIn(self.content_request_form_sent_post_title_ce_en, contents)
                        else:
                            self.assertIn(self.content_request_form_sent_post_title_en, contents)
                    self.assertIn(self.content_request_form_sent_post_secondary_en, contents)
            else:
                if not display_region == 'ni':
                    if override_sub_user_journey:
                        self.assertIn(self.build_translation_link(override_sub_user_journey + '/code-sent-post',
                                                                  display_region, False), contents)
                    else:
                        self.assertIn(self.build_translation_link('code-sent-post', display_region), contents)
                if display_region == 'ni':
                    if case_type == 'CE':
                        if check_room_number:
                            if long_surname:
                                self.assertIn(self.content_request_code_sent_post_title_ce_with_room_long_surname_en,
                                              contents)
                            else:
                                self.assertIn(self.content_request_code_sent_post_title_ce_with_room_en, contents)
                        else:
                            self.assertIn(self.content_request_code_sent_post_title_ce_en, contents)
                    else:
                        self.assertIn(self.content_request_code_sent_post_title_ni, contents)
                    if individual == 'true':
                        self.assertIn(self.content_request_code_sent_post_secondary_individual_en, contents)
                    elif case_type == 'CE':
                        self.assertIn(self.content_request_code_sent_post_secondary_manager_en, contents)
                    else:
                        self.assertIn(self.content_request_code_sent_post_secondary_household_en, contents)
                elif display_region == 'cy':
                    if case_type == 'CE':
                        if check_room_number:
                            if long_surname:
                                self.assertIn(self.content_request_code_sent_post_title_ce_with_room_long_surname_cy,
                                              contents)
                            else:
                                self.assertIn(self.content_request_code_sent_post_title_ce_with_room_cy, contents)
                        else:
                            self.assertIn(self.content_request_code_sent_post_title_ce_cy, contents)
                    else:
                        self.assertIn(self.content_request_code_sent_post_title_cy, contents)
                    if individual == 'true':
                        self.assertIn(self.content_request_code_sent_post_secondary_individual_cy, contents)
                    elif case_type == 'CE':
                        self.assertIn(self.content_request_code_sent_post_secondary_manager_cy, contents)
                    else:
                        self.assertIn(self.content_request_code_sent_post_secondary_household_cy, contents)
                else:
                    if case_type == 'CE':
                        if check_room_number:
                            if long_surname:
                                self.assertIn(self.content_request_code_sent_post_title_ce_with_room_long_surname_en,
                                              contents)
                            else:
                                self.assertIn(self.content_request_code_sent_post_title_ce_with_room_en, contents)
                        else:
                            self.assertIn(self.content_request_code_sent_post_title_ce_en, contents)
                    else:
                        self.assertIn(self.content_request_code_sent_post_title_en, contents)
                    if individual == 'true':
                        self.assertIn(self.content_request_code_sent_post_secondary_individual_en, contents)
                    elif case_type == 'CE':
                        self.assertIn(self.content_request_code_sent_post_secondary_manager_en, contents)
                    else:
                        self.assertIn(self.content_request_code_sent_post_secondary_household_en, contents)

    async def check_post_confirm_name_address_input_no(self, url, display_region, user_type):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-name-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('select-method', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('select-method', display_region), contents)
            self.check_text_select_method(display_region, contents, user_type, check_error=False)

    async def check_post_confirm_name_address_input_no_form(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=self.request_common_confirm_name_address_data_no)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-name-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('request-cancelled', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('request-cancelled', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_form_request_cancelled_title_cy, contents)
            else:
                self.assertIn(self.content_request_form_request_cancelled_title_en, contents)

    async def check_post_confirm_name_address_input_invalid_or_no_selection(self, url, display_region, data, user_type,
                                                                            case_type):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-name-address', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('confirm-name-address', display_region), contents)
            if case_type == 'CE':
                self.check_text_confirm_name_address(display_region, contents, user_type,
                                                     check_error=True, check_ce=True)
            else:
                self.check_text_confirm_name_address(display_region, contents, user_type,
                                                     check_error=True, check_ce=False)

    async def check_post_confirm_name_address_error_from_get_fulfilment(self, url, display_region,
                                                                        case_type, region, product_group, individual):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=' + case_type + '&region=' + region +
                                    '&deliveryChannel=POST&productGroup=' + product_group +
                                    '&individual=' + individual, status=400)

            response = await self.client.request('POST', url, data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-name-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_confirm_name_address_error_from_request_fulfilment(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            response = await self.client.request('POST', url, data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-name-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_confirm_name_address_error_429_from_request_fulfilment_uac(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=429)

            response = await self.client.request('POST', url, data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-name-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'error in response', status_code=429)

            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_429_error_uac_title_cy, contents)
            else:
                self.assertIn(self.content_common_429_error_uac_title_en, contents)

    async def check_post_confirm_name_address_error_429_from_request_fulfilment_form(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=429)

            response = await self.client.request('POST', url, data=self.request_common_confirm_name_address_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-name-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'error in response', status_code=429)

            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_429_error_form_title_cy, contents)
            else:
                self.assertIn(self.content_common_429_error_form_title_en, contents)

    async def assert_no_direct_access(self, url, display_region, method, data=None):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            if method == 'POST':
                if data:
                    response = await self.client.request('POST', url, allow_redirects=False, data=data)
                else:
                    response = await self.client.request('POST', url, allow_redirects=False)
            else:
                response = await self.client.request('GET', url, allow_redirects=False)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.get_logo(display_region), contents)
        if display_region == 'cy':
            self.assertNotIn(self.content_common_save_and_exit_link_cy, contents)
            self.assertIn(self.content_start_timeout_title_cy, contents)
            self.assertIn(self.content_start_timeout_secondary_cy, contents)
            self.assertIn(self.content_start_timeout_restart_cy, contents)
        else:
            self.assertNotIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_timeout_title_en, contents)
            self.assertIn(self.content_start_timeout_secondary_en, contents)
            self.assertIn(self.content_start_timeout_restart_en, contents)

    async def check_get_request_individual_code(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, self.build_url_log_entry('individual-code', display_region, 'GET', False))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('individual-code', display_region, False), contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_individual_title_cy, contents)
                self.assertIn(self.content_request_individual_secondary_cy, contents)
            else:
                self.assertIn(self.content_request_individual_title_en, contents)
                self.assertIn(self.content_request_individual_secondary_en, contents)

    async def check_post_request_individual_code_journey_switch(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url)
            self.assertLogEvent(cm, self.build_url_log_entry('individual-code', display_region, 'POST', False))
            self.assertLogEvent(cm, 'have session and case_type - directing to select method')
            self.assertLogEvent(cm, self.build_url_log_entry('individual-code/select-method', display_region, 'GET',
                                                             False))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('individual-code/select-method', display_region, False),
                              contents)
            self.check_text_select_method(display_region, contents, 'individual')

    async def add_room_number(self, url_get, url_post, display_region, user_type, return_page, no_data=False):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            if display_region == 'ni':
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_northern_ireland_ce
            else:
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_ce

            response = await self.client.request('GET', url_get)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-room-number', display_region, 'GET'))

            self.assertEqual(200, response.status)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-room-number', display_region), contents)
            self.check_text_enter_room_number(display_region, contents)

            if no_data:
                response = await self.client.request('POST', url_post, data=self.common_room_number_input_empty)
                self.assertLogEvent(cm, self.build_url_log_entry('enter-room-number', display_region, 'POST'))
                self.assertLogEvent(cm, self.build_url_log_entry('enter-room-number', display_region, 'GET'))

                self.assertEqual(200, response.status)
                contents = str(await response.content.read())
                self.assertIn(self.get_logo(display_region), contents)
                if not display_region == 'ni':
                    self.assertIn(self.build_translation_link('enter-room-number', display_region), contents)
                self.check_text_enter_room_number(display_region, contents, check_error=True)

            else:
                response = await self.client.request('POST', url_post, data=self.common_room_number_input_valid)
                self.assertLogEvent(cm, self.build_url_log_entry('enter-room-number', display_region, 'POST'))

                if return_page == 'ConfirmAddress':
                    self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'GET'))

                    self.assertEqual(200, response.status)
                    contents = str(await response.content.read())
                    self.assertIn(self.get_logo(display_region), contents)
                    if not display_region == 'ni':
                        self.assertIn(self.build_translation_link('confirm-address', display_region), contents)
                    self.check_text_confirm_address(display_region, contents, check_error=False, check_ce=True,
                                                    check_room_number=True)
                else:
                    self.assertLogEvent(cm, self.build_url_log_entry('confirm-name-address', display_region, 'GET'))

                    self.assertEqual(200, response.status)
                    contents = str(await response.content.read())
                    self.assertIn(self.get_logo(display_region), contents)
                    if not display_region == 'ni':
                        self.assertIn(self.build_translation_link('confirm-name-address', display_region), contents)
                    self.check_text_confirm_name_address(display_region, contents, user_type,
                                                         check_error=False, check_ce=True, check_room_number=True)

    async def assert_start_page_correct(self, url, display_region, ad_location=False):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, self.build_url_log_entry(self.sub_user_journey, display_region, 'GET',
                                                             include_sub_user_journey=False,
                                                             include_page=False))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                if ad_location:
                    self.assertIn(self.build_translation_link(self.sub_user_journey, display_region,
                                                              include_sub_user_journey=False,
                                                              include_page=False, include_adlocation=True), contents)
                else:
                    self.assertIn(self.build_translation_link(self.sub_user_journey, display_region,
                                                              include_sub_user_journey=False,
                                                              include_page=False, include_adlocation=False), contents)
            if display_region == 'cy':
                self.assertIn(self.content_start_title_cy, contents)
                self.assertIn(self.content_start_uac_title_cy, contents)
            else:
                self.assertIn(self.content_start_title_en, contents)
                self.assertIn(self.content_start_uac_title_en, contents)
            if ad_location:
                self.assertLogEvent(cm, "assisted digital query parameter found")
                self.assertIn('type="hidden"', contents)
                self.assertIn('value="' + self.adlocation + '"', contents)
                self.assertEqual(contents.count('input--text'), 2)
            else:
                self.assertEqual(contents.count('input--text'), 1)
            self.assertIn('type="submit"', contents)

    async def assert_start_page_post_returns_address_in_northern_ireland(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)]) \
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            response = await self.client.request('POST', url, data=self.start_data_valid)
            self.assertLogEvent(cm, self.build_url_log_entry(self.sub_user_journey, display_region, 'POST',
                                                             include_sub_user_journey=False,
                                                             include_page=False))
            self.assertLogEvent(cm, self.build_url_log_entry('code-for-northern-ireland', display_region, 'GET',
                                                             include_sub_user_journey=False,
                                                             include_page=True))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('code-for-northern-ireland', display_region,
                                                          include_sub_user_journey=False,
                                                          include_page=True), contents)
            if display_region == 'cy':
                self.assertIn(self.content_start_code_for_northern_ireland_title_cy, contents)
            else:
                self.assertIn(self.content_start_code_for_northern_ireland_title_en, contents)

    async def assert_start_page_post_returns_address_in_england(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)]) \
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            response = await self.client.request('POST', url, data=self.start_data_valid)
            self.assertLogEvent(cm, self.build_url_log_entry(self.sub_user_journey, display_region, 'POST',
                                                             include_sub_user_journey=False,
                                                             include_page=False))
            self.assertLogEvent(cm, self.build_url_log_entry('code-for-england', display_region, 'GET',
                                                             include_sub_user_journey=False,
                                                             include_page=True))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.content_start_code_not_for_northern_ireland_title, contents)
            self.assertIn(self.content_start_code_for_england_secondary, contents)

    async def assert_start_page_post_returns_address_in_wales(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)]) \
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            response = await self.client.request('POST', url, data=self.start_data_valid)
            self.assertLogEvent(cm, self.build_url_log_entry(self.sub_user_journey, display_region, 'POST',
                                                             include_sub_user_journey=False,
                                                             include_page=False))
            self.assertLogEvent(cm, self.build_url_log_entry('code-for-wales', display_region, 'GET',
                                                             include_sub_user_journey=False,
                                                             include_page=True))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.content_start_code_not_for_northern_ireland_title, contents)
            self.assertIn(self.content_start_code_for_wales_secondary, contents)

    def check_text_start_transient_enter_town_name(self, display_region, contents,
                                                   after_census_day=False, check_error=False):
        if display_region == 'cy':
            if check_error:
                self.assertIn(self.content_start_transient_enter_town_name_error_cy, contents)
            if after_census_day:
                self.assertIn(self.content_start_transient_enter_town_name_post_census_day_title_cy, contents)
            else:
                self.assertIn(self.content_start_transient_enter_town_name_pre_census_day_title_cy, contents)
        else:
            if check_error:
                self.assertIn(self.content_start_transient_enter_town_name_error_en, contents)
            if after_census_day:
                self.assertIn(self.content_start_transient_enter_town_name_post_census_day_title_cy, contents)
            else:
                self.assertIn(self.content_start_transient_enter_town_name_pre_census_day_title_cy, contents)

    def check_text_start_transient_accommodation_type(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if check_error:
                self.assertIn(self.content_start_transient_accommodation_type_error_cy, contents)
            self.assertIn(self.content_start_transient_accommodation_type_title_cy, contents)
            self.assertIn(self.content_start_transient_accommodation_type_value_barge_cy, contents)
            self.assertIn(self.content_start_transient_accommodation_type_value_caravan_cy, contents)
            self.assertIn(self.content_start_transient_accommodation_type_value_tent_cy, contents)
        else:
            if check_error:
                self.assertIn(self.content_start_transient_accommodation_type_error_en, contents)
            self.assertIn(self.content_start_transient_accommodation_type_title_en, contents)
            self.assertIn(self.content_start_transient_accommodation_type_value_barge_en, contents)
            self.assertIn(self.content_start_transient_accommodation_type_value_caravan_en, contents)
            self.assertIn(self.content_start_transient_accommodation_type_value_tent_en, contents)

    def check_text_start_transient_ni_select_language(self, contents, check_error=False):
        if check_error:
            self.assertIn(self.content_start_ni_select_language_error, contents)
        self.assertIn(self.content_common_save_and_exit_link_en, contents)
        self.assertIn(self.content_start_ni_select_language_title, contents)
        self.assertIn(self.content_start_ni_select_language_option, contents)
        self.assertIn(self.content_start_ni_select_language_switch_back, contents)

    def check_text_start_transient_ni_language_options(self, contents, check_error=False):
        if check_error:
            self.assertIn(self.content_start_ni_language_options_error, contents)
        self.assertIn(self.content_common_save_and_exit_link_en, contents)
        self.assertIn(self.content_start_ni_language_options_title, contents)
        self.assertIn(self.content_start_ni_language_options_option_yes, contents)

    async def check_get_start(self, display_region, adlocation=False):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            if adlocation:
                response = await self.client.request('GET', self.get_url_from_class(
                    'Start', 'get', display_region, {"adlocation": "1234567890"}))
            else:
                response = await self.client.request('GET', self.get_url_from_class('Start', 'get', display_region))
            self.assertLogEvent(cm, self.build_url_log_entry('', display_region, 'GET', include_sub_user_journey=False))
            self.assertEqual(200, response.status)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('', display_region, include_sub_user_journey=False,
                                                          adlocation=adlocation), contents)
            if display_region == 'cy':
                self.assertIn(self.content_start_title_cy, contents)
                self.assertIn(self.content_start_uac_title_cy, contents)
            else:
                self.assertIn(self.content_start_title_en, contents)
                self.assertIn(self.content_start_uac_title_en, contents)
            if adlocation:
                self.assertLogEvent(cm, "assisted digital query parameter found")
                self.assertIn('type="submit"', contents)
                self.assertIn('type="hidden"', contents)
                self.assertIn('value="1234567890"', contents)
            if adlocation:
                self.assertEqual(contents.count('input--text'), 2)
            else:
                self.assertEqual(contents.count('input--text'), 1)
            self.assertIn('type="submit"', contents)

    async def check_post_start_transient(self, display_region, region, after_census_day=False, adlocation=False):
        if after_census_day:
            mocked_now_utc = datetime.datetime(2021, 3, 22, 0, 0, 0, 0)
        else:
            mocked_now_utc = datetime.datetime(2021, 3, 21, 0, 0, 0, 0)
        if region == 'N':
            uac_payload = self.transient_uac_json_n
        elif region == 'W':
            uac_payload = self.transient_uac_json_w
        else:
            uac_payload = self.transient_uac_json_e
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.View.get_now_utc') as mocked_get_now_utc, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked_get_now_utc.return_value = mocked_now_utc
            mocked.get(self.rhsvc_url, payload=uac_payload)
            if adlocation:
                data = self.start_data_valid_with_adlocation
            else:
                data = self.start_data_valid
            response = await self.client.request('POST', self.get_url_from_class('Start', 'post', display_region),
                                                 allow_redirects=True, data=data)

            self.assertLogEvent(cm, self.build_url_log_entry('', display_region, 'POST',
                                                             include_sub_user_journey=False))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-town-name', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-town-name', display_region), contents)
            if after_census_day:
                self.check_text_start_transient_enter_town_name(display_region, contents,
                                                                after_census_day=True, check_error=False)
            else:
                self.check_text_start_transient_enter_town_name(display_region, contents,
                                                                after_census_day=False, check_error=False)

    async def check_post_start_transient_enter_town_name_valid(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'POST', self.get_url_from_class('StartTransientEnterTownName', 'post', display_region),
                data=self.start_transient_town_name_input_valid)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-town-name', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('accommodation-type', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('accommodation-type', display_region), contents)
            self.check_text_start_transient_accommodation_type(display_region, contents, check_error=False)

    async def check_post_start_transient_enter_town_name_empty(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'POST', self.get_url_from_class('StartTransientEnterTownName', 'post', display_region),
                data=self.start_transient_town_name_input_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-town-name', display_region, 'POST'))
            self.assertLogEvent(cm, "error town name empty")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('enter-town-name', display_region), contents)
            self.check_text_start_transient_enter_town_name(display_region, contents, check_error=True)

    async def check_post_start_transient_accommodation_type_selection(
            self, display_region, selection, region, adlocation=False):
        if display_region == 'cy':
            if selection == 'barge':
                data = self.start_transient_accommodation_type_input_barge_cy
                accommodation_type_text = self.content_start_transient_accommodation_type_value_barge_cy
            elif selection == 'caravan':
                data = self.start_transient_accommodation_type_input_caravan_cy
                accommodation_type_text = self.content_start_transient_accommodation_type_value_caravan_cy
            else:
                data = self.start_transient_accommodation_type_input_tent_cy
                accommodation_type_text = self.content_start_transient_accommodation_type_value_tent_cy
        else:
            if selection == 'barge':
                data = self.start_transient_accommodation_type_input_barge_en
                accommodation_type_text = self.content_start_transient_accommodation_type_value_barge_en
            elif selection == 'caravan':
                data = self.start_transient_accommodation_type_input_caravan_en
                accommodation_type_text = self.content_start_transient_accommodation_type_value_caravan_en
            else:
                data = self.start_transient_accommodation_type_input_tent_en
                accommodation_type_text = self.content_start_transient_accommodation_type_value_tent_en
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            if region == 'W':
                eq_payload['region_code'] = 'GB-WLS'
            else:
                eq_payload['region_code'] = 'GB-ENG'
            if display_region == 'cy':
                eq_payload['language_code'] = 'cy'
            else:
                eq_payload['language_code'] = 'en'
            if adlocation:
                eq_payload['channel'] = 'ad'
                eq_payload['user_id'] = '1234567890'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/' + display_region
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = '9999999999999'
            eq_payload['case_type'] = 'SPG'
            eq_payload['display_address'] = accommodation_type_text + ' near ' + self.data_start_transient_town_name

            response = await self.client.request(
                'POST',
                self.get_url_from_class('StartTransientAccommodationType', 'post', display_region),
                allow_redirects=False,
                data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('accommodation-type', display_region, 'POST'))
            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    async def check_post_start_transient_accommodation_type_selection_ni(self, selection):
        display_region = 'ni'
        if selection == 'barge':
            data = self.start_transient_accommodation_type_input_barge_en
        elif selection == 'caravan':
            data = self.start_transient_accommodation_type_input_caravan_en
        else:
            data = self.start_transient_accommodation_type_input_tent_en
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'POST',
                self.get_url_from_class('StartTransientAccommodationType', 'post', display_region), data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('accommodation-type', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('language-options', display_region,
                                                             'GET', include_sub_user_journey=False))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_start_transient_ni_language_options(contents, check_error=False)

    async def check_post_start_transient_accommodation_type_no_selection(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'POST', self.get_url_from_class('StartTransientAccommodationType', 'post', display_region),
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('accommodation-type', display_region, 'POST'))
            self.assertLogEvent(cm, "transient accommodation type error")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('accommodation-type', display_region), contents)
            self.check_text_start_transient_accommodation_type(display_region, contents, check_error=True)

    async def check_post_start_transient_ni_language_options_yes(self, selection, adlocation=False):
        display_region = 'ni'
        if selection == 'barge':
            accommodation_type_text = self.content_start_transient_accommodation_type_value_barge_en
        elif selection == 'caravan':
            accommodation_type_text = self.content_start_transient_accommodation_type_value_caravan_en
        else:
            accommodation_type_text = self.content_start_transient_accommodation_type_value_tent_en
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            if adlocation:
                eq_payload['channel'] = 'ad'
                eq_payload['user_id'] = '1234567890'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/' + display_region
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = '9999999999999'
            eq_payload['case_type'] = 'SPG'
            eq_payload['display_address'] = accommodation_type_text + ' near ' + self.data_start_transient_town_name

            response = await self.client.request(
                'POST',
                self.get_url_from_class('StartNILanguageOptions', 'post'),
                allow_redirects=False,
                data=self.start_ni_language_option_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('language-options', display_region,
                                                             'POST', include_sub_user_journey=False))
            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    async def check_post_start_transient_ni_language_options_no(self):
        display_region = 'ni'
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'POST', self.get_url_from_class('StartNILanguageOptions', 'post'),
                data=self.start_ni_language_option_data_no)
            self.assertLogEvent(cm, self.build_url_log_entry('language-options', display_region,
                                                             'POST', include_sub_user_journey=False))
            self.assertLogEvent(cm, self.build_url_log_entry('select-language', display_region,
                                                             'GET', include_sub_user_journey=False))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_start_transient_ni_select_language(contents, check_error=False)

    async def check_post_start_transient_ni_language_options_no_selection(self):
        display_region = 'ni'
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'POST', self.get_url_from_class('StartNILanguageOptions', 'post'),
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('language-options', display_region,
                                                             'POST', include_sub_user_journey=False))
            self.assertLogEvent(cm, 'ni language option error')
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_start_transient_ni_language_options(contents, check_error=True)

    async def check_post_start_transient_ni_select_language(self, selection, language_selection, adlocation=False):
        display_region = 'ni'
        if selection == 'barge':
            accommodation_type_text = self.content_start_transient_accommodation_type_value_barge_en
        elif selection == 'caravan':
            accommodation_type_text = self.content_start_transient_accommodation_type_value_caravan_en
        else:
            accommodation_type_text = self.content_start_transient_accommodation_type_value_tent_en
        if language_selection == 'ga':
            data = self.start_ni_select_language_data_ga
        elif language_selection == 'ul':
            data = self.start_ni_select_language_data_ul
        else:
            data = self.start_ni_select_language_data_en
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            if language_selection == 'ga':
                eq_payload['language_code'] = 'ga'
            elif language_selection == 'ul':
                eq_payload['language_code'] = 'eo'
            else:
                eq_payload['language_code'] = 'en'
            if adlocation:
                eq_payload['channel'] = 'ad'
                eq_payload['user_id'] = '1234567890'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/' + display_region
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = '9999999999999'
            eq_payload['case_type'] = 'SPG'
            eq_payload['display_address'] = accommodation_type_text + ' near ' + self.data_start_transient_town_name

            response = await self.client.request(
                'POST',
                self.get_url_from_class('StartNISelectLanguage', 'post'),
                allow_redirects=False,
                data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('select-language', display_region,
                                                             'POST', include_sub_user_journey=False))
            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    async def check_post_start_transient_ni_select_language_no_selection(self):
        display_region = 'ni'
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request(
                'POST', self.get_url_from_class('StartNISelectLanguage', 'post'),
                data=self.common_form_data_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('select-language', display_region,
                                                             'POST', include_sub_user_journey=False))
            self.assertLogEvent(cm, 'ni language option error')
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_start_transient_ni_select_language(contents, check_error=True)
