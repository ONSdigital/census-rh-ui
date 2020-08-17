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

    async def get_common_enter_address(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/enter-address/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/enter-address/" '
                              'lang="en" >English</a>', contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_enter_address_title_cy, contents)
                self.assertIn(self.content_request_enter_address_secondary_cy, contents)
            else:
                self.assertIn(self.content_request_enter_address_title_en, contents)
                self.assertIn(self.content_request_enter_address_secondary_en, contents)

    async def post_common_enter_address(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request('POST', url, data=self.common_postcode_input_valid)

            self.assertLogEvent(cm, "received POST on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/enter-address'")
            self.assertLogEvent(cm, 'valid postcode')
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/select-address/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/select-address/" '
                              'lang="en" >English</a>', contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_select_address_title_cy, contents)
                self.assertIn(self.content_common_select_address_value_cy, contents)
            else:
                self.assertIn(self.content_common_select_address_title_en, contents)
                self.assertIn(self.content_common_select_address_value_en, contents)

    async def post_common_enter_address_no_results(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request('POST', url, data=self.common_postcode_input_valid)

            self.assertLogEvent(cm, "received POST on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/enter-address'")
            self.assertLogEvent(cm, 'valid postcode')
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/select-address/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/select-address/" '
                              'lang="en" >English</a>', contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_select_address_no_results_cy, contents)
            else:
                self.assertIn(self.content_common_select_address_no_results_en, contents)

    async def post_common_enter_address_empty(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_postcode_input_empty)

            self.assertLogEvent(cm, "received POST on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/enter-address'")
            self.assertLogEvent(cm, 'invalid postcode')
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/enter-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/enter-address/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/enter-address/" '
                              'lang="en" >English</a>', contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_enter_address_error_empty_cy, contents)
            else:
                self.assertIn(self.content_common_enter_address_error_empty_en, contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_enter_address_title_cy, contents)
                self.assertIn(self.content_request_enter_address_secondary_cy, contents)
            else:
                self.assertIn(self.content_request_enter_address_title_en, contents)
                self.assertIn(self.content_request_enter_address_secondary_en, contents)

    async def post_common_enter_address_invalid(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=self.common_postcode_input_invalid)

            self.assertLogEvent(cm, "received POST on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/enter-address'")
            self.assertLogEvent(cm, 'invalid postcode')
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/enter-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/enter-address/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/enter-address/" '
                              'lang="en" >English</a>', contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_enter_address_error_cy, contents)
            else:
                self.assertIn(self.content_common_enter_address_error_en, contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_enter_address_title_cy, contents)
                self.assertIn(self.content_request_enter_address_secondary_cy, contents)
            else:
                self.assertIn(self.content_request_enter_address_title_en, contents)
                self.assertIn(self.content_request_enter_address_secondary_en, contents)

    async def post_common_select_address_empty(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request('POST', url, data=self.common_form_data_empty)

            self.assertLogEvent(cm, "received POST on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/select-address'")
            self.assertLogEvent(cm, 'no address selected')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/select-address/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/select-address/" '
                              'lang="en" >English</a>', contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_select_address_error_cy, contents)
                self.assertIn(self.content_common_select_address_title_cy, contents)
                self.assertIn(self.content_common_select_address_value_cy, contents)
            else:
                self.assertIn(self.content_common_select_address_error_en, contents)
                self.assertIn(self.content_common_select_address_title_en, contents)
                self.assertIn(self.content_common_select_address_value_en, contents)

    async def post_common_select_address(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request('POST', url, data=self.common_select_address_input_valid)

            self.assertLogEvent(cm, "received POST on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/confirm-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/confirm-address/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/confirm-address/" '
                              'lang="en" >English</a>', contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_confirm_address_title_cy, contents)
                self.assertIn(self.content_common_confirm_address_value_yes_cy, contents)
                self.assertIn(self.content_common_confirm_address_value_no_cy, contents)
            else:
                self.assertIn(self.content_common_confirm_address_title_en, contents)
                self.assertIn(self.content_common_confirm_address_value_yes_en, contents)
                self.assertIn(self.content_common_confirm_address_value_no_en, contents)

    async def post_common_confirm_address_invalid_or_no_selection(self, url, display_region, data):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request('POST', url, data=self.common_form_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/confirm-address'")
            self.assertLogEvent(cm, "address confirmation error")
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/confirm-address/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/confirm-address/" '
                              'lang="en" >English</a>', contents)

            if display_region == 'cy':
                self.assertIn(self.content_common_confirm_address_error_cy, contents)
                self.assertIn(self.content_common_confirm_address_title_cy, contents)
                self.assertIn(self.content_common_confirm_address_value_yes_cy, contents)
                self.assertIn(self.content_common_confirm_address_value_no_cy, contents)
            else:
                self.assertIn(self.content_common_confirm_address_error_en, contents)
                self.assertIn(self.content_common_confirm_address_title_en, contents)
                self.assertIn(self.content_common_confirm_address_value_yes_en, contents)
                self.assertIn(self.content_common_confirm_address_value_no_en, contents)

    async def post_common_confirm_address_no(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm, "received POST on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/enter-address'")
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/enter-address/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/enter-address/" '
                              'lang="en" >English</a>', contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_enter_address_title_cy, contents)
                self.assertIn(self.content_request_enter_address_secondary_cy, contents)
            else:
                self.assertIn(self.content_request_enter_address_title_en, contents)
                self.assertIn(self.content_request_enter_address_secondary_en, contents)

    async def post_common_confirm_address_yes(self, url, display_region, case_by_uprn_return):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
                'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = case_by_uprn_return

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/enter-mobile'")
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/enter-mobile/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/enter-mobile/" '
                              'lang="en" >English</a>', contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_code_enter_mobile_title_cy, contents)
                self.assertIn(self.content_request_code_enter_mobile_secondary_cy, contents)
            else:
                self.assertIn(self.content_request_code_enter_mobile_title_en, contents)
                self.assertIn(self.content_request_code_enter_mobile_secondary_en, contents)

    async def post_common_enter_mobile(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST', url, data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/confirm-mobile'")
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'en':
                self.assertIn('<a href="/cy/' + self.user_journey + '/' + self.sub_user_journey + '/confirm-mobile/" '
                              'lang="cy" >Cymraeg</a>', contents)
            elif display_region == 'cy':
                self.assertIn('<a href="/en/' + self.user_journey + '/' + self.sub_user_journey + '/confirm-mobile/" '
                              'lang="en" >English</a>', contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_code_confirm_mobile_title_cy, contents)
            else:
                self.assertIn(self.content_request_code_confirm_mobile_title_en, contents)

    async def post_common_enter_address_ai_error(self, url, display_region, status):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=status)

            response = await self.client.request('POST', url, data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=status)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_500_error_cy, contents)
            else:
                self.assertIn(self.content_common_500_error_en, contents)

    def mock_ai_503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

    async def post_common_enter_address_ai_error_503(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock_ai_503s(mocked, attempts_retry_limit)

            response = await self.client.request('POST', url, data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_500_error_cy, contents)
            else:
                self.assertIn(self.content_common_500_error_en, contents)

    async def post_common_enter_address_ai_connection_error(self, url, display_region, epoch=None):
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
        if display_region == 'cy':
            self.assertIn(self.content_common_500_error_cy, contents)
        else:
            self.assertIn(self.content_common_500_error_en, contents)

    async def post_common_confirm_address_get_cases_error(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_get_case_by_uprn:

            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            response = await self.client.request('POST', url, data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint '" + display_region +
                                "/" + self.user_journey + "/" + self.sub_user_journey + "/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_500_error_cy, contents)
            else:
                self.assertIn(self.content_common_500_error_en, contents)
