from .helpers import TestHelpers
from aiohttp.test_utils import unittest_run_loop


class TestSessionHandling(TestHelpers):

    def build_url(self, class_name, method, display_region=None, user_journey='', sub_user_journey='', request_type=''):
        if not display_region:
            url = self.app.router[class_name + ':' + method.lower()].url_for()
        else:
            if request_type:
                url = self.app.router[class_name + ':' + method.lower()].url_for(
                    display_region=display_region, request_type=request_type)
            else:
                url = self.app.router[class_name + ':' + method.lower()].url_for(
                    display_region=display_region, user_journey=user_journey, sub_user_journey=sub_user_journey)
        return url

    async def assert_no_session_or_forbidden(
            self, class_name, method, display_region=None, user_journey='', sub_user_journey='', request_type='',
            permission=True):
        url = self.build_url(
            class_name, method, display_region, user_journey, sub_user_journey, request_type)
        with self.assertLogs('respondent-home', 'WARN') as cm:
            if method == 'POST':
                response = await self.client.request('POST', url, allow_redirects=False)
            else:
                response = await self.client.request('GET', url, allow_redirects=False)
        if permission:
            self.assertLogEvent(cm, 'permission denied')
        else:
            self.assertLogEvent(cm, 'session timed out')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.get_logo(display_region if display_region else 'ni'), contents)
        if display_region == 'cy':
            self.assertNotIn(self.content_start_exit_button_cy, contents)
            self.assertIn(self.content_timeout_title_cy, contents)
            if 'start' in url.path:
                self.assertIn(self.content_start_timeout_secondary_cy, contents)
                self.assertIn(self.content_start_timeout_restart_cy, contents)
            else:
                self.assertIn(self.content_request_timeout_secondary_cy, contents)
                self.assertIn(self.content_request_timeout_restart_cy, contents)
        else:
            if display_region == 'ni':
                self.assertNotIn(self.content_start_exit_button_ni, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_en, contents)
            self.assertIn(self.content_timeout_title_en, contents)
            self.assertIn(self.content_timeout_secondary_en, contents)
            if 'start' in url.path:
                self.assertIn(self.content_start_timeout_restart_en, contents)
            else:
                self.assertIn(self.content_request_timeout_restart_en, contents)

    @unittest_run_loop
    async def test_no_direct_access_forbidden_start_confirm_address(self):
        await self.assert_no_session_or_forbidden('StartConfirmAddress', 'GET', 'en')
        await self.assert_no_session_or_forbidden('StartConfirmAddress', 'GET', 'cy')
        await self.assert_no_session_or_forbidden('StartConfirmAddress', 'GET', 'ni')
        await self.assert_no_session_or_forbidden('StartConfirmAddress', 'POST', 'en')
        await self.assert_no_session_or_forbidden('StartConfirmAddress', 'POST', 'cy')
        await self.assert_no_session_or_forbidden('StartConfirmAddress', 'POST', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_forbidden_start_ni_language_options(self):
        await self.assert_no_session_or_forbidden('StartNILanguageOptions', 'GET')
        await self.assert_no_session_or_forbidden('StartNILanguageOptions', 'POST')

    @unittest_run_loop
    async def test_no_direct_access_forbidden_start_ni_select_language(self):
        await self.assert_no_session_or_forbidden('StartNISelectLanguage', 'GET')
        await self.assert_no_session_or_forbidden('StartNISelectLanguage', 'POST')

    @unittest_run_loop
    async def test_no_direct_access_forbidden_start_address_has_been_linked(self):
        await self.assert_no_session_or_forbidden('StartAddressHasBeenLinked', 'GET', 'en')
        await self.assert_no_session_or_forbidden('StartAddressHasBeenLinked', 'GET', 'cy')
        await self.assert_no_session_or_forbidden('StartAddressHasBeenLinked', 'GET', 'ni')
        await self.assert_no_session_or_forbidden('StartAddressHasBeenLinked', 'POST', 'en')
        await self.assert_no_session_or_forbidden('StartAddressHasBeenLinked', 'POST', 'cy')
        await self.assert_no_session_or_forbidden('StartAddressHasBeenLinked', 'POST', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_forbidden_start_address_has_been_changed(self):
        await self.assert_no_session_or_forbidden('StartAddressHasBeenChanged', 'GET', 'en')
        await self.assert_no_session_or_forbidden('StartAddressHasBeenChanged', 'GET', 'cy')
        await self.assert_no_session_or_forbidden('StartAddressHasBeenChanged', 'GET', 'ni')
        await self.assert_no_session_or_forbidden('StartAddressHasBeenChanged', 'POST', 'en')
        await self.assert_no_session_or_forbidden('StartAddressHasBeenChanged', 'POST', 'cy')
        await self.assert_no_session_or_forbidden('StartAddressHasBeenChanged', 'POST', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_forbidden_start_transient_enter_town_name(self):
        await self.assert_no_session_or_forbidden('StartTransientEnterTownName', 'GET', 'en')
        await self.assert_no_session_or_forbidden('StartTransientEnterTownName', 'GET', 'cy')
        await self.assert_no_session_or_forbidden('StartTransientEnterTownName', 'GET', 'ni')
        await self.assert_no_session_or_forbidden('StartTransientEnterTownName', 'POST', 'en')
        await self.assert_no_session_or_forbidden('StartTransientEnterTownName', 'POST', 'cy')
        await self.assert_no_session_or_forbidden('StartTransientEnterTownName', 'POST', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_forbidden_start_transient_accommodation_type(self):
        await self.assert_no_session_or_forbidden('StartTransientAccommodationType', 'GET', 'en')
        await self.assert_no_session_or_forbidden('StartTransientAccommodationType', 'GET', 'cy')
        await self.assert_no_session_or_forbidden('StartTransientAccommodationType', 'GET', 'ni')
        await self.assert_no_session_or_forbidden('StartTransientAccommodationType', 'POST', 'en')
        await self.assert_no_session_or_forbidden('StartTransientAccommodationType', 'POST', 'cy')
        await self.assert_no_session_or_forbidden('StartTransientAccommodationType', 'POST', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_forbidden_common_enter_address(self):
        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'GET', 'en', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'GET', 'cy', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'GET', 'ni', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'POST', 'en', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'POST', 'cy', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'POST', 'ni', 'start', 'change-address')

        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'GET', 'en', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'GET', 'cy', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'GET', 'ni', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'POST', 'en', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'POST', 'cy', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonEnterAddress', 'POST', 'ni', 'start', 'link-address')

    @unittest_run_loop
    async def test_no_direct_access_no_session_common_enter_address(self):
        await self.assert_no_session_or_forbidden(
            'CommonEnterAddress', 'POST', 'en', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterAddress', 'POST', 'cy', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterAddress', 'POST', 'ni', 'request', 'access-code', permission=False)

        await self.assert_no_session_or_forbidden(
            'CommonEnterAddress', 'POST', 'en', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterAddress', 'POST', 'cy', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterAddress', 'POST', 'ni', 'request', 'paper-questionnaire', permission=False)

        await self.assert_no_session_or_forbidden(
            'CommonEnterAddress', 'POST', 'en', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterAddress', 'POST', 'cy', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterAddress', 'POST', 'ni', 'request', 'continuation-questionnaire', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_forbidden_common_select_address(self):
        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'GET', 'en', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'GET', 'cy', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'GET', 'ni', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'POST', 'en', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'POST', 'cy', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'POST', 'ni', 'start', 'change-address')

        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'GET', 'en', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'GET', 'cy', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'GET', 'ni', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'POST', 'en', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'POST', 'cy', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonSelectAddress', 'POST', 'ni', 'start', 'link-address')

    @unittest_run_loop
    async def test_no_direct_access_no_session_common_select_address(self):
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'GET', 'en', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'GET', 'cy', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'GET', 'ni', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'POST', 'en', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'POST', 'cy', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'POST', 'ni', 'request', 'access-code', permission=False)

        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'GET', 'en', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'GET', 'cy', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'GET', 'ni', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'POST', 'en', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'POST', 'cy', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'POST', 'ni', 'request', 'paper-questionnaire', permission=False)

        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'GET', 'en', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'GET', 'cy', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'GET', 'ni', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'POST', 'en', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'POST', 'cy', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonSelectAddress', 'POST', 'ni', 'request', 'continuation-questionnaire', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_forbidden_common_confirm_address(self):
        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'GET', 'en', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'GET', 'cy', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'GET', 'ni', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'POST', 'en', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'POST', 'cy', 'start', 'change-address')
        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'POST', 'ni', 'start', 'change-address')

        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'GET', 'en', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'GET', 'cy', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'GET', 'ni', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'POST', 'en', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'POST', 'cy', 'start', 'link-address')
        await self.assert_no_session_or_forbidden('CommonConfirmAddress', 'POST', 'ni', 'start', 'link-address')

    @unittest_run_loop
    async def test_no_direct_access_no_session_common_confirm_address(self):
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'GET', 'en', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'GET', 'cy', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'GET', 'ni', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'POST', 'en', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'POST', 'cy', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'POST', 'ni', 'request', 'access-code', permission=False)

        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'GET', 'en', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'GET', 'cy', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'GET', 'ni', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'POST', 'en', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'POST', 'cy', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'POST', 'ni', 'request', 'paper-questionnaire', permission=False)

        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'GET', 'en', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'GET', 'cy', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'GET', 'ni', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'POST', 'en', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'POST', 'cy', 'request', 'continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonConfirmAddress', 'POST', 'ni', 'request', 'continuation-questionnaire', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_common_ce_manager(self):
        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'GET', 'en', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'GET', 'cy', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'GET', 'ni', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'POST', 'en', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'POST', 'cy', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'POST', 'ni', 'request', 'access-code', permission=False)

        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'GET', 'en', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'GET', 'cy', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'GET', 'ni', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'POST', 'en', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'POST', 'cy', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonCEMangerQuestion', 'POST', 'ni', 'request', 'paper-questionnaire', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_common_enter_room_number(self):
        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'GET', 'en', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'GET', 'cy', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'GET', 'ni', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'POST', 'en', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'POST', 'cy', 'request', 'access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'POST', 'ni', 'request', 'access-code', permission=False)

        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'GET', 'en', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'GET', 'cy', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'GET', 'ni', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'POST', 'en', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'POST', 'cy', 'request', 'paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'CommonEnterRoomNumber', 'POST', 'ni', 'request', 'paper-questionnaire', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_individual_form(self):
        await self.assert_no_session_or_forbidden(
            'RequestIndividualForm', 'POST', 'en', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestIndividualForm', 'POST', 'cy', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestIndividualForm', 'POST', 'ni', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_household(self):
        await self.assert_no_session_or_forbidden(
            'RequestCodeHousehold', 'POST', 'en', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeHousehold', 'POST', 'cy', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeHousehold', 'POST', 'ni', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_household_form(self):
        await self.assert_no_session_or_forbidden(
            'RequestHouseholdForm', 'POST', 'en', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestHouseholdForm', 'POST', 'cy', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestHouseholdForm', 'POST', 'ni', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_select_how_to_recieve(self):
        await self.assert_no_session_or_forbidden(
            'RequestCodeEnterMobile', 'GET', 'en', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeEnterMobile', 'GET', 'cy', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeEnterMobile', 'GET', 'ni', request_type='access-code', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_enter_mobile(self):
        await self.assert_no_session_or_forbidden(
            'RequestCodeEnterMobile', 'GET', 'en', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeEnterMobile', 'GET', 'cy', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeEnterMobile', 'GET', 'ni', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeEnterMobile', 'POST', 'en', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeEnterMobile', 'POST', 'cy', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeEnterMobile', 'POST', 'ni', request_type='access-code', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_confirm_send_by_text(self):
        await self.assert_no_session_or_forbidden(
            'RequestCodeConfirmSendByText', 'GET', 'en', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeConfirmSendByText', 'GET', 'cy', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeConfirmSendByText', 'GET', 'ni', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeConfirmSendByText', 'POST', 'en', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeConfirmSendByText', 'POST', 'cy', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeConfirmSendByText', 'POST', 'ni', request_type='access-code', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_enter_name(self):
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'GET', 'en', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'GET', 'cy', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'GET', 'ni', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'POST', 'en', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'POST', 'cy', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'POST', 'ni', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'GET', 'en', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'GET', 'cy', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'GET', 'ni', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'POST', 'en', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'POST', 'cy', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'POST', 'ni', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'GET', 'en', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'GET', 'cy', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'GET', 'ni', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'POST', 'en', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'POST', 'cy', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonEnterName', 'POST', 'ni', request_type='continuation-questionnaire', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_confirm_send_by_post(self):
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'GET', 'en', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'GET', 'cy', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'GET', 'ni', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'POST', 'en', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'POST', 'cy', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'POST', 'ni', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'GET', 'en', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'GET', 'cy', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'GET', 'ni', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'POST', 'en', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'POST', 'cy', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'POST', 'ni', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'GET', 'en', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'GET', 'cy', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'GET', 'ni', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'POST', 'en', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'POST', 'cy', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonConfirmSendByPost', 'POST', 'ni', request_type='continuation-questionnaire', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_sent_by_text(self):
        await self.assert_no_session_or_forbidden(
            'RequestCodeSentByText', 'GET', 'en', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeSentByText', 'GET', 'cy', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeSentByText', 'GET', 'ni', request_type='access-code', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_sent_by_post(self):
        await self.assert_no_session_or_forbidden(
            'RequestCodeSentByPost', 'GET', 'en', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeSentByPost', 'GET', 'cy', request_type='access-code', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCodeSentByPost', 'GET', 'ni', request_type='access-code', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_people_in_household(self):
        await self.assert_no_session_or_forbidden(
            'RequestCommonPeopleInHousehold', 'POST', 'en', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonPeopleInHousehold', 'POST', 'cy', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonPeopleInHousehold', 'POST', 'ni', request_type='paper-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonPeopleInHousehold', 'POST', 'en', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonPeopleInHousehold', 'POST', 'cy', request_type='continuation-questionnaire', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestCommonPeopleInHousehold', 'POST', 'ni', request_type='continuation-questionnaire', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_questionnaire_sent(self):
        await self.assert_no_session_or_forbidden(
            'RequestQuestionnaireSent', 'GET', 'en', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestQuestionnaireSent', 'GET', 'cy', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestQuestionnaireSent', 'GET', 'ni', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_continuation_sent(self):
        await self.assert_no_session_or_forbidden(
            'RequestContinuationSent', 'GET', 'en', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestContinuationSent', 'GET', 'cy', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestContinuationSent', 'GET', 'ni', permission=False)

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_large_print_sent_post(self):
        await self.assert_no_session_or_forbidden(
            'RequestLargePrintSentPost', 'GET', 'en', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestLargePrintSentPost', 'GET', 'cy', permission=False)
        await self.assert_no_session_or_forbidden(
            'RequestLargePrintSentPost', 'GET', 'ni', permission=False)
