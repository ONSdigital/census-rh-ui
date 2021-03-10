from .helpers import TestHelpers
from aiohttp.test_utils import unittest_run_loop


class TestSessionHandling(TestHelpers):

    def clear_session(self):
        """
        Ensure session cleared from previous requests
        """
        jar = self.client._session.cookie_jar
        jar.clear()

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

    async def assert_no_session(
            self, class_name, method, display_region=None, user_journey='', sub_user_journey='', request_type=''):
        url = self.build_url(
            class_name, method, display_region, user_journey, sub_user_journey, request_type)
        self.clear_session()
        with self.assertLogs('respondent-home', 'WARN') as cm:
            if method == 'POST':
                response = await self.client.request('POST', url, allow_redirects=False)
            else:
                response = await self.client.request('GET', url, allow_redirects=False)
        self.assertLogEvent(cm, 'session timed out')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.get_logo(display_region if display_region else 'ni'), contents)
        if display_region == 'cy':
            self.assertNotIn(self.content_start_exit_button_cy, contents)
            self.assertIn(self.content_timeout_title_cy, contents)
            if 'start' in url.path:
                self.assertIn(self.content_start_timeout_forbidden_link_text_cy, contents)
                self.assertIn(self.content_start_timeout_secondary_cy, contents)
            else:
                self.assertIn(self.content_request_timeout_restart_cy, contents)
                self.assertIn(self.content_request_timeout_secondary_cy, contents)
        else:
            if display_region == 'ni':
                self.assertNotIn(self.content_start_exit_button_ni, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_en, contents)
            self.assertIn(self.content_timeout_title_en, contents)
            self.assertIn(self.content_timeout_secondary_en, contents)
            if 'start' in url.path:
                self.assertIn(self.content_start_timeout_forbidden_link_text_en, contents)
            else:
                self.assertIn(self.content_request_timeout_restart_en, contents)

    async def assert_forbidden(
            self, class_name, method, display_region=None, user_journey='', sub_user_journey=''):
        url = self.build_url(
            class_name, method, display_region, user_journey, sub_user_journey)
        self.clear_session()
        cookie = {'RH_SESSION': '{ "session": {"client_id": "36be6b97-b4de-4718-8a74-8b27fb03ca8c"}}'}
        header = {"X-Cloud-Trace-Context": "0123456789/0123456789012345678901;o=1"}
        with self.assertLogs('respondent-home', 'WARN') as cm:
            if method == 'POST':
                response = await self.client.request('POST', url, allow_redirects=False, cookies=cookie, headers=header)
            else:
                response = await self.client.request('GET', url, allow_redirects=False, cookies=cookie,  headers=header)
        self.assertLogEvent(cm, 'permission denied',
                            client_id='36be6b97-b4de-4718-8a74-8b27fb03ca8c', trace='0123456789')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.get_logo(display_region if display_region else 'ni'), contents)
        if display_region == 'cy':
            self.assertNotIn(self.content_start_exit_button_cy, contents)
            self.assertIn(self.content_start_forbidden_title_cy, contents)
            self.assertIn(self.content_start_timeout_forbidden_link_text_cy, contents)
        else:
            if display_region == 'ni':
                self.assertNotIn(self.content_start_exit_button_ni, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_en, contents)
            self.assertIn(self.content_start_forbidden_title_en, contents)
            self.assertIn(self.content_start_timeout_forbidden_link_text_en, contents)

    @unittest_run_loop
    async def test_no_direct_access_no_session_start_confirm_address(self):
        await self.assert_no_session('StartConfirmAddress', 'GET', 'en')
        await self.assert_no_session('StartConfirmAddress', 'GET', 'cy')
        await self.assert_no_session('StartConfirmAddress', 'GET', 'ni')
        await self.assert_no_session('StartConfirmAddress', 'POST', 'en')
        await self.assert_no_session('StartConfirmAddress', 'POST', 'cy')
        await self.assert_no_session('StartConfirmAddress', 'POST', 'ni')

    @unittest_run_loop
    async def test_forbidden_start_confirm_address(self):
        await self.assert_forbidden('StartConfirmAddress', 'GET', 'en')
        await self.assert_forbidden('StartConfirmAddress', 'GET', 'cy')
        await self.assert_forbidden('StartConfirmAddress', 'GET', 'ni')
        await self.assert_forbidden('StartConfirmAddress', 'POST', 'en')
        await self.assert_forbidden('StartConfirmAddress', 'POST', 'cy')
        await self.assert_forbidden('StartConfirmAddress', 'POST', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_no_session_start_ni_language_options(self):
        await self.assert_no_session('StartNILanguageOptions', 'GET')
        await self.assert_no_session('StartNILanguageOptions', 'POST')

    @unittest_run_loop
    async def test_forbidden_start_ni_language_options(self):
        await self.assert_forbidden('StartNILanguageOptions', 'GET')
        await self.assert_forbidden('StartNILanguageOptions', 'POST')

    @unittest_run_loop
    async def test_no_direct_access_no_session_start_ni_select_language(self):
        await self.assert_no_session('StartNISelectLanguage', 'GET')
        await self.assert_no_session('StartNISelectLanguage', 'POST')

    @unittest_run_loop
    async def test_forbidden_start_ni_select_language(self):
        await self.assert_forbidden('StartNISelectLanguage', 'GET')
        await self.assert_forbidden('StartNISelectLanguage', 'POST')

    @unittest_run_loop
    async def test_no_direct_access_no_session_start_transient_enter_town_name(self):
        await self.assert_no_session('StartTransientEnterTownName', 'GET', 'en')
        await self.assert_no_session('StartTransientEnterTownName', 'GET', 'cy')
        await self.assert_no_session('StartTransientEnterTownName', 'GET', 'ni')
        await self.assert_no_session('StartTransientEnterTownName', 'POST', 'en')
        await self.assert_no_session('StartTransientEnterTownName', 'POST', 'cy')
        await self.assert_no_session('StartTransientEnterTownName', 'POST', 'ni')

    @unittest_run_loop
    async def test_forbidden_start_transient_enter_town_name(self):
        await self.assert_forbidden('StartTransientEnterTownName', 'GET', 'en')
        await self.assert_forbidden('StartTransientEnterTownName', 'GET', 'cy')
        await self.assert_forbidden('StartTransientEnterTownName', 'GET', 'ni')
        await self.assert_forbidden('StartTransientEnterTownName', 'POST', 'en')
        await self.assert_forbidden('StartTransientEnterTownName', 'POST', 'cy')
        await self.assert_forbidden('StartTransientEnterTownName', 'POST', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_no_session_start_transient_accommodation_type(self):
        await self.assert_no_session('StartTransientAccommodationType', 'GET', 'en')
        await self.assert_no_session('StartTransientAccommodationType', 'GET', 'cy')
        await self.assert_no_session('StartTransientAccommodationType', 'GET', 'ni')
        await self.assert_no_session('StartTransientAccommodationType', 'POST', 'en')
        await self.assert_no_session('StartTransientAccommodationType', 'POST', 'cy')
        await self.assert_no_session('StartTransientAccommodationType', 'POST', 'ni')

    @unittest_run_loop
    async def test_forbidden_start_transient_accommodation_type(self):
        await self.assert_forbidden('StartTransientAccommodationType', 'GET', 'en')
        await self.assert_forbidden('StartTransientAccommodationType', 'GET', 'cy')
        await self.assert_forbidden('StartTransientAccommodationType', 'GET', 'ni')
        await self.assert_forbidden('StartTransientAccommodationType', 'POST', 'en')
        await self.assert_forbidden('StartTransientAccommodationType', 'POST', 'cy')
        await self.assert_forbidden('StartTransientAccommodationType', 'POST', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_no_session_start_common_enter_address(self):
        await self.assert_no_session('CommonEnterAddress', 'GET', 'en', 'start', 'change-address')
        await self.assert_no_session('CommonEnterAddress', 'GET', 'cy', 'start', 'change-address')
        await self.assert_no_session('CommonEnterAddress', 'GET', 'ni', 'start', 'change-address')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'en', 'start', 'change-address')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'cy', 'start', 'change-address')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'ni', 'start', 'change-address')

        await self.assert_no_session('CommonEnterAddress', 'GET', 'en', 'start', 'link-address')
        await self.assert_no_session('CommonEnterAddress', 'GET', 'cy', 'start', 'link-address')
        await self.assert_no_session('CommonEnterAddress', 'GET', 'ni', 'start', 'link-address')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'en', 'start', 'link-address')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'cy', 'start', 'link-address')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'ni', 'start', 'link-address')

    @unittest_run_loop
    async def test_forbidden_start_common_enter_address(self):
        await self.assert_forbidden('CommonEnterAddress', 'GET', 'en', 'start', 'change-address')
        await self.assert_forbidden('CommonEnterAddress', 'GET', 'cy', 'start', 'change-address')
        await self.assert_forbidden('CommonEnterAddress', 'GET', 'ni', 'start', 'change-address')
        await self.assert_forbidden('CommonEnterAddress', 'POST', 'en', 'start', 'change-address')
        await self.assert_forbidden('CommonEnterAddress', 'POST', 'cy', 'start', 'change-address')
        await self.assert_forbidden('CommonEnterAddress', 'POST', 'ni', 'start', 'change-address')

        await self.assert_forbidden('CommonEnterAddress', 'GET', 'en', 'start', 'link-address')
        await self.assert_forbidden('CommonEnterAddress', 'GET', 'cy', 'start', 'link-address')
        await self.assert_forbidden('CommonEnterAddress', 'GET', 'ni', 'start', 'link-address')
        await self.assert_forbidden('CommonEnterAddress', 'POST', 'en', 'start', 'link-address')
        await self.assert_forbidden('CommonEnterAddress', 'POST', 'cy', 'start', 'link-address')
        await self.assert_forbidden('CommonEnterAddress', 'POST', 'ni', 'start', 'link-address')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_enter_address(self):
        await self.assert_no_session('CommonEnterAddress', 'POST', 'en', 'request', 'access-code')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'cy', 'request', 'access-code')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'ni', 'request', 'access-code')

        await self.assert_no_session('CommonEnterAddress', 'POST', 'en', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'cy', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'ni', 'request', 'paper-questionnaire')

        await self.assert_no_session('CommonEnterAddress', 'POST', 'en', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'cy', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonEnterAddress', 'POST', 'ni', 'request', 'continuation-questionnaire')

    @unittest_run_loop
    async def test_no_direct_access_no_session_start_common_select_address(self):
        await self.assert_no_session('CommonSelectAddress', 'GET', 'en', 'start', 'change-address')
        await self.assert_no_session('CommonSelectAddress', 'GET', 'cy', 'start', 'change-address')
        await self.assert_no_session('CommonSelectAddress', 'GET', 'ni', 'start', 'change-address')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'en', 'start', 'change-address')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'cy', 'start', 'change-address')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'ni', 'start', 'change-address')

        await self.assert_no_session('CommonSelectAddress', 'GET', 'en', 'start', 'link-address')
        await self.assert_no_session('CommonSelectAddress', 'GET', 'cy', 'start', 'link-address')
        await self.assert_no_session('CommonSelectAddress', 'GET', 'ni', 'start', 'link-address')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'en', 'start', 'link-address')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'cy', 'start', 'link-address')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'ni', 'start', 'link-address')

    @unittest_run_loop
    async def test_forbidden_start_common_select_address(self):
        await self.assert_forbidden('CommonSelectAddress', 'GET', 'en', 'start', 'change-address')
        await self.assert_forbidden('CommonSelectAddress', 'GET', 'cy', 'start', 'change-address')
        await self.assert_forbidden('CommonSelectAddress', 'GET', 'ni', 'start', 'change-address')
        await self.assert_forbidden('CommonSelectAddress', 'POST', 'en', 'start', 'change-address')
        await self.assert_forbidden('CommonSelectAddress', 'POST', 'cy', 'start', 'change-address')
        await self.assert_forbidden('CommonSelectAddress', 'POST', 'ni', 'start', 'change-address')

        await self.assert_forbidden('CommonSelectAddress', 'GET', 'en', 'start', 'link-address')
        await self.assert_forbidden('CommonSelectAddress', 'GET', 'cy', 'start', 'link-address')
        await self.assert_forbidden('CommonSelectAddress', 'GET', 'ni', 'start', 'link-address')
        await self.assert_forbidden('CommonSelectAddress', 'POST', 'en', 'start', 'link-address')
        await self.assert_forbidden('CommonSelectAddress', 'POST', 'cy', 'start', 'link-address')
        await self.assert_forbidden('CommonSelectAddress', 'POST', 'ni', 'start', 'link-address')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_select_address(self):
        await self.assert_no_session('CommonSelectAddress', 'GET', 'en', 'request', 'access-code')
        await self.assert_no_session('CommonSelectAddress', 'GET', 'cy', 'request', 'access-code')
        await self.assert_no_session('CommonSelectAddress', 'GET', 'ni', 'request', 'access-code')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'en', 'request', 'access-code')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'cy', 'request', 'access-code')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'ni', 'request', 'access-code')

        await self.assert_no_session('CommonSelectAddress', 'GET', 'en', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonSelectAddress', 'GET', 'cy', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonSelectAddress', 'GET', 'ni', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'en', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'cy', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'ni', 'request', 'paper-questionnaire')

        await self.assert_no_session('CommonSelectAddress', 'GET', 'en', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonSelectAddress', 'GET', 'cy', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonSelectAddress', 'GET', 'ni', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'en', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'cy', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonSelectAddress', 'POST', 'ni', 'request', 'continuation-questionnaire')

    @unittest_run_loop
    async def test_no_direct_access_no_session_start_common_confirm_address(self):
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'en', 'start', 'change-address')
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'cy', 'start', 'change-address')
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'ni', 'start', 'change-address')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'en', 'start', 'change-address')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'cy', 'start', 'change-address')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'ni', 'start', 'change-address')

        await self.assert_no_session('CommonConfirmAddress', 'GET', 'en', 'start', 'link-address')
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'cy', 'start', 'link-address')
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'ni', 'start', 'link-address')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'en', 'start', 'link-address')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'cy', 'start', 'link-address')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'ni', 'start', 'link-address')

    @unittest_run_loop
    async def test_forbidden_start_common_confirm_address(self):
        await self.assert_forbidden('CommonConfirmAddress', 'GET', 'en', 'start', 'change-address')
        await self.assert_forbidden('CommonConfirmAddress', 'GET', 'cy', 'start', 'change-address')
        await self.assert_forbidden('CommonConfirmAddress', 'GET', 'ni', 'start', 'change-address')
        await self.assert_forbidden('CommonConfirmAddress', 'POST', 'en', 'start', 'change-address')
        await self.assert_forbidden('CommonConfirmAddress', 'POST', 'cy', 'start', 'change-address')
        await self.assert_forbidden('CommonConfirmAddress', 'POST', 'ni', 'start', 'change-address')

        await self.assert_forbidden('CommonConfirmAddress', 'GET', 'en', 'start', 'link-address')
        await self.assert_forbidden('CommonConfirmAddress', 'GET', 'cy', 'start', 'link-address')
        await self.assert_forbidden('CommonConfirmAddress', 'GET', 'ni', 'start', 'link-address')
        await self.assert_forbidden('CommonConfirmAddress', 'POST', 'en', 'start', 'link-address')
        await self.assert_forbidden('CommonConfirmAddress', 'POST', 'cy', 'start', 'link-address')
        await self.assert_forbidden('CommonConfirmAddress', 'POST', 'ni', 'start', 'link-address')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_confirm_address(self):
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'en', 'request', 'access-code')
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'cy', 'request', 'access-code')
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'ni', 'request', 'access-code')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'en', 'request', 'access-code')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'cy', 'request', 'access-code')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'ni', 'request', 'access-code')

        await self.assert_no_session('CommonConfirmAddress', 'GET', 'en', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'cy', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'ni', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'en', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'cy', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'ni', 'request', 'paper-questionnaire')

        await self.assert_no_session('CommonConfirmAddress', 'GET', 'en', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'cy', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonConfirmAddress', 'GET', 'ni', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'en', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'cy', 'request', 'continuation-questionnaire')
        await self.assert_no_session('CommonConfirmAddress', 'POST', 'ni', 'request', 'continuation-questionnaire')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_ce_manager(self):
        await self.assert_no_session('CommonCEMangerQuestion', 'GET', 'en', 'request', 'access-code')
        await self.assert_no_session('CommonCEMangerQuestion', 'GET', 'cy', 'request', 'access-code')
        await self.assert_no_session('CommonCEMangerQuestion', 'GET', 'ni', 'request', 'access-code')
        await self.assert_no_session('CommonCEMangerQuestion', 'POST', 'en', 'request', 'access-code')
        await self.assert_no_session('CommonCEMangerQuestion', 'POST', 'cy', 'request', 'access-code')
        await self.assert_no_session('CommonCEMangerQuestion', 'POST', 'ni', 'request', 'access-code')

        await self.assert_no_session('CommonCEMangerQuestion', 'GET', 'en', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonCEMangerQuestion', 'GET', 'cy', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonCEMangerQuestion', 'GET', 'ni', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonCEMangerQuestion', 'POST', 'en', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonCEMangerQuestion', 'POST', 'cy', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonCEMangerQuestion', 'POST', 'ni', 'request', 'paper-questionnaire')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_enter_room_number(self):
        await self.assert_no_session('CommonEnterRoomNumber', 'GET', 'en', 'request', 'access-code')
        await self.assert_no_session('CommonEnterRoomNumber', 'GET', 'cy', 'request', 'access-code')
        await self.assert_no_session('CommonEnterRoomNumber', 'GET', 'ni', 'request', 'access-code')
        await self.assert_no_session('CommonEnterRoomNumber', 'POST', 'en', 'request', 'access-code')
        await self.assert_no_session('CommonEnterRoomNumber', 'POST', 'cy', 'request', 'access-code')
        await self.assert_no_session('CommonEnterRoomNumber', 'POST', 'ni', 'request', 'access-code')

        await self.assert_no_session('CommonEnterRoomNumber', 'GET', 'en', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonEnterRoomNumber', 'GET', 'cy', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonEnterRoomNumber', 'GET', 'ni', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonEnterRoomNumber', 'POST', 'en', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonEnterRoomNumber', 'POST', 'cy', 'request', 'paper-questionnaire')
        await self.assert_no_session('CommonEnterRoomNumber', 'POST', 'ni', 'request', 'paper-questionnaire')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_individual_form(self):
        await self.assert_no_session('RequestIndividualForm', 'GET', 'en')
        await self.assert_no_session('RequestIndividualForm', 'GET', 'cy', )
        await self.assert_no_session('RequestIndividualForm', 'GET', 'ni')
        await self.assert_no_session('RequestIndividualForm', 'POST', 'en')
        await self.assert_no_session('RequestIndividualForm', 'POST', 'cy',)
        await self.assert_no_session('RequestIndividualForm', 'POST', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_household(self):
        await self.assert_no_session('RequestCodeHousehold', 'GET', 'en')
        await self.assert_no_session('RequestCodeHousehold', 'GET', 'cy')
        await self.assert_no_session('RequestCodeHousehold', 'GET', 'ni')
        await self.assert_no_session('RequestCodeHousehold', 'POST', 'en')
        await self.assert_no_session('RequestCodeHousehold', 'POST', 'cy')
        await self.assert_no_session('RequestCodeHousehold', 'POST', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_household_form(self):
        await self.assert_no_session('RequestHouseholdForm', 'GET', 'en')
        await self.assert_no_session('RequestHouseholdForm', 'GET', 'cy')
        await self.assert_no_session('RequestHouseholdForm', 'GET', 'ni')
        await self.assert_no_session('RequestHouseholdForm', 'POST', 'en')
        await self.assert_no_session('RequestHouseholdForm', 'POST', 'cy')
        await self.assert_no_session('RequestHouseholdForm', 'POST', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_select_how_to_receive(self):
        await self.assert_no_session('RequestCodeSelectHowToReceive', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeSelectHowToReceive', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCodeSelectHowToReceive', 'GET', 'ni', request_type='access-code')
        await self.assert_no_session('RequestCodeSelectHowToReceive', 'POST', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeSelectHowToReceive', 'POST', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCodeSelectHowToReceive', 'POST', 'ni', request_type='access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_enter_mobile(self):
        await self.assert_no_session('RequestCodeEnterMobile', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeEnterMobile', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCodeEnterMobile', 'GET', 'ni', request_type='access-code')
        await self.assert_no_session('RequestCodeEnterMobile', 'POST', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeEnterMobile', 'POST', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCodeEnterMobile', 'POST', 'ni', request_type='access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_confirm_send_by_text(self):
        await self.assert_no_session('RequestCodeConfirmSendByText', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeConfirmSendByText', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCodeConfirmSendByText', 'GET', 'ni', request_type='access-code')
        await self.assert_no_session('RequestCodeConfirmSendByText', 'POST', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeConfirmSendByText', 'POST', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCodeConfirmSendByText', 'POST', 'ni', request_type='access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_enter_name(self):
        await self.assert_no_session('RequestCommonEnterName', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCommonEnterName', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCommonEnterName', 'GET', 'ni', request_type='access-code')
        await self.assert_no_session('RequestCommonEnterName', 'POST', 'en', request_type='access-code')
        await self.assert_no_session('RequestCommonEnterName', 'POST', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCommonEnterName', 'POST', 'ni', request_type='access-code')
        await self.assert_no_session('RequestCommonEnterName', 'GET', 'en', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonEnterName', 'GET', 'cy', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonEnterName', 'GET', 'ni', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonEnterName', 'POST', 'en', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonEnterName', 'POST', 'cy', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonEnterName', 'POST', 'ni', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonEnterName', 'GET', 'en', request_type='continuation-questionnaire')
        await self.assert_no_session('RequestCommonEnterName', 'GET', 'cy', request_type='continuation-questionnaire')
        await self.assert_no_session('RequestCommonEnterName', 'GET', 'ni', request_type='continuation-questionnaire')
        await self.assert_no_session('RequestCommonEnterName', 'POST', 'en', request_type='continuation-questionnaire')
        await self.assert_no_session('RequestCommonEnterName', 'POST', 'cy', request_type='continuation-questionnaire')
        await self.assert_no_session('RequestCommonEnterName', 'POST', 'ni', request_type='continuation-questionnaire')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_confirm_send_by_post(self):
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'GET', 'ni', request_type='access-code')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'POST', 'en', request_type='access-code')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'POST', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'POST', 'ni', request_type='access-code')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'GET', 'en', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'GET', 'cy', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'GET', 'ni', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'POST', 'en', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'POST', 'cy', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'POST', 'ni', request_type='paper-questionnaire')
        await self.assert_no_session(
            'RequestCommonConfirmSendByPost', 'GET', 'en', request_type='continuation-questionnaire')
        await self.assert_no_session(
            'RequestCommonConfirmSendByPost', 'GET', 'cy', request_type='continuation-questionnaire')
        await self.assert_no_session(
            'RequestCommonConfirmSendByPost', 'GET', 'ni', request_type='continuation-questionnaire')
        await self.assert_no_session(
            'RequestCommonConfirmSendByPost', 'POST', 'en', request_type='continuation-questionnaire')
        await self.assert_no_session(
            'RequestCommonConfirmSendByPost', 'POST', 'cy', request_type='continuation-questionnaire')
        await self.assert_no_session(
            'RequestCommonConfirmSendByPost', 'POST', 'ni', request_type='continuation-questionnaire')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_sent_by_text(self):
        await self.assert_no_session('RequestCodeSentByText', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeSentByText', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCodeSentByText', 'GET', 'ni', request_type='access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_sent_by_post(self):
        await self.assert_no_session('RequestCodeSentByPost', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeSentByPost', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCodeSentByPost', 'GET', 'ni', request_type='access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_people_in_household(self):
        await self.assert_no_session('RequestCommonPeopleInHousehold', 'POST', 'en', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonPeopleInHousehold', 'POST', 'cy', request_type='paper-questionnaire')
        await self.assert_no_session('RequestCommonPeopleInHousehold', 'POST', 'ni', request_type='paper-questionnaire')
        await self.assert_no_session(
            'RequestCommonPeopleInHousehold', 'POST', 'en', request_type='continuation-questionnaire')
        await self.assert_no_session(
            'RequestCommonPeopleInHousehold', 'POST', 'cy', request_type='continuation-questionnaire')
        await self.assert_no_session(
            'RequestCommonPeopleInHousehold', 'POST', 'ni', request_type='continuation-questionnaire')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_questionnaire_sent(self):
        await self.assert_no_session('RequestQuestionnaireSent', 'GET', 'en')
        await self.assert_no_session('RequestQuestionnaireSent', 'GET', 'cy')
        await self.assert_no_session('RequestQuestionnaireSent', 'GET', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_continuation_sent(self):
        await self.assert_no_session('RequestContinuationSent', 'GET', 'en')
        await self.assert_no_session('RequestContinuationSent', 'GET', 'cy')
        await self.assert_no_session('RequestContinuationSent', 'GET', 'ni')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_large_print_sent_post(self):
        await self.assert_no_session('RequestLargePrintSentPost', 'GET', 'en')
        await self.assert_no_session('RequestLargePrintSentPost', 'GET', 'cy')
        await self.assert_no_session('RequestLargePrintSentPost', 'GET', 'ni')
