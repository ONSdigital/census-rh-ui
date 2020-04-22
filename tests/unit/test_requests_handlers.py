from unittest import mock

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from . import RHTestCase


# noinspection PyTypeChecker
class TestRequestsHandlers(RHTestCase):

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hh_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn(self.content_request_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hh_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn(self.content_request_select_address_no_results_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hh_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn(self.content_request_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hi_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn(self.content_request_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hi_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn(self.content_request_select_address_no_results_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hi_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn(self.content_request_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_hh_en(
            self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_hh_cy(
            self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_hh_ni(
            self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_en(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hh_en,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn(self.content_request_enter_mobile_title_en, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_cy(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hh_cy,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn(self.content_request_enter_mobile_title_cy, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ni(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hh_ni,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn(self.content_request_enter_mobile_title_en, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hi_en(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hi_en,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn(self.content_request_enter_mobile_title_en, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hi_cy(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hi_cy,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn(self.content_request_enter_mobile_title_cy, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hi_ni(self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hi_ni,
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn(self.content_request_enter_mobile_title_en, contents)
                self.assertIn(self.content_request_enter_mobile_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hh_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'en/requests/household-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_select_address_title_en, str(resp_content))
            self.assertIn(self.content_request_select_address_error_en, str(resp_content))
            self.assertIn(self.content_request_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hh_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'cy/requests/household-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_select_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_select_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hh_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'ni/requests/household-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_select_address_title_en, str(resp_content))
            self.assertIn(self.content_request_select_address_error_en, str(resp_content))
            self.assertIn(self.content_request_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hi_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'en/requests/individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_select_address_title_en, str(resp_content))
            self.assertIn(self.content_request_select_address_error_en, str(resp_content))
            self.assertIn(self.content_request_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hi_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'cy/requests/individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_select_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_select_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hi_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'ni/requests/individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_select_address_title_en, str(resp_content))
            self.assertIn(self.content_request_select_address_error_en, str(resp_content))
            self.assertIn(self.content_request_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hh_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_confirm_address_input_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hh_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hh_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_confirm_address_input_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hi_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_confirm_address_input_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hi_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_confirm_address_input_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hi_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_confirm_address_input_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hh_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))


    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hh_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hh_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hi_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hi_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hi_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hh_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'en/requests/household-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hh_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'cy/requests/household-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hh_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'ni/requests/household-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hi_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'en/requests/individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hi_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'cy/requests/individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hi_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'ni/requests/individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hh_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCommon.request_fulfilment') as mocked_request_fulfilment\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_household_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_household_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hh_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_select_address_title_en, str(resp_content))
            self.assertIn(self.content_request_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCommon.request_fulfilment') as mocked_request_fulfilment\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_household_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_household_title_cy, contents)
            self.assertIn(self.content_request_secondary_cy, contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hh_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCommon.request_fulfilment') as mocked_request_fulfilment\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_household_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_household_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hh_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_select_address_title_en, str(resp_content))
            self.assertIn(self.content_request_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hi_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCommon.request_fulfilment') as mocked_request_fulfilment\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_individual_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hi_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_select_address_title_en, str(resp_content))
            self.assertIn(self.content_request_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hi_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCommon.request_fulfilment') as mocked_request_fulfilment\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_individual_title_cy, contents)
            self.assertIn(self.content_request_secondary_cy, contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hi_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hi_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCommon.request_fulfilment') as mocked_request_fulfilment\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_individual_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hi_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_select_address_title_en, str(resp_content))
            self.assertIn(self.content_request_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hh_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en

            await self.client.request('GET', self.get_requestcode_household_en)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_en)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy

            await self.client.request('GET', self.get_requestcode_household_cy)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_cy)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_cy,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni

            await self.client.request('GET', self.get_requestcode_household_ni)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_ni)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_ni,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hi_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en

            await self.client.request('GET', self.get_requestcode_individual_en)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_en)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hi_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy

            await self.client.request('GET', self.get_requestcode_individual_cy)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_cy)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_cy,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hi_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni

            await self.client.request('GET', self.get_requestcode_individual_ni)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_ni)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_ni,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_empty_hh_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en

            await self.client.request('GET', self.get_requestcode_household_en)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_en)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_en,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_empty_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy

            await self.client.request('GET', self.get_requestcode_household_cy)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_cy)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_cy,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_empty_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni

            await self.client.request('GET', self.get_requestcode_household_ni)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_ni)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_ni,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_empty_hi_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en

            await self.client.request('GET', self.get_requestcode_individual_en)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_en)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_en,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_empty_hi_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy

            await self.client.request('GET', self.get_requestcode_individual_cy)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_cy)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_cy,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_empty_hi_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni

            await self.client.request('GET', self.get_requestcode_individual_ni)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_ni)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_confirm_address_input_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_ni,
                    data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_invalid_hh_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn \
                :
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en

            await self.client.request('GET', self.get_requestcode_household_en)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_en)

            await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hh_en,
                data=self.request_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_selectaddress_hh_en,
                data=self.request_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_address_confirmation_hh_en,
                data=self.request_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_requestcode_entermobile_hh_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_requestcode_confirm_mobile_hh_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_invalid_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn \
                :
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy

            await self.client.request('GET', self.get_requestcode_household_cy)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_cy)

            await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hh_cy,
                data=self.request_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_selectaddress_hh_cy,
                data=self.request_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_address_confirmation_hh_cy,
                data=self.request_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_requestcode_entermobile_hh_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_requestcode_confirm_mobile_hh_cy,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_invalid_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn \
                :
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni

            await self.client.request('GET', self.get_requestcode_household_ni)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_ni)

            await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hh_ni,
                data=self.request_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_selectaddress_hh_ni,
                data=self.request_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_address_confirmation_hh_ni,
                data=self.request_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_requestcode_entermobile_hh_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_requestcode_confirm_mobile_hh_ni,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_invalid_hi_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn \
                :
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en

            await self.client.request('GET', self.get_requestcode_individual_en)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_en)

            await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hi_en,
                data=self.request_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_selectaddress_hi_en,
                data=self.request_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_address_confirmation_hi_en,
                data=self.request_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_requestcode_entermobile_hi_en,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_requestcode_confirm_mobile_hi_en,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_invalid_hi_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn \
                :
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy

            await self.client.request('GET', self.get_requestcode_individual_cy)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_cy)

            await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hh_cy,
                data=self.request_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_selectaddress_hh_cy,
                data=self.request_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_address_confirmation_hh_cy,
                data=self.request_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_requestcode_entermobile_hh_cy,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_requestcode_confirm_mobile_hi_cy,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_invalid_hi_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn \
                :
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni

            await self.client.request('GET', self.get_requestcode_individual_ni)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_ni)

            await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hi_ni,
                data=self.request_postcode_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_selectaddress_hi_ni,
                data=self.request_select_address_input_valid)

            await self.client.request(
                'POST',
                self.post_requestcode_address_confirmation_hi_ni,
                data=self.request_confirm_address_input_yes)

            await self.client.request(
                'POST',
                self.post_requestcode_entermobile_hi_ni,
                data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                'POST',
                self.post_requestcode_confirm_mobile_hi_ni,
                data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_error_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_address_not_required_hh_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_requestcode_household_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/contact-centre'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_address_not_required_hh_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_requestcode_household_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/contact-centre'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_contact_centre_cy, contents)

    @unittest_run_loop
    async def test_get_request_address_not_required_hh_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_requestcode_household_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/contact-centre'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_address_not_required_hi_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_requestcode_individual_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/contact-centre'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_address_not_required_hi_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_requestcode_individual_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/contact-centre'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_contact_centre_cy, contents)

    @unittest_run_loop
    async def test_get_request_address_not_required_hi_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_requestcode_individual_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/contact-centre'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_code_confirm_address_get_cases_error_hh_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_requestcode_household_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_code_confirm_address_get_cases_error_hh_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_requestcode_household_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_500_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_code_confirm_address_get_cases_error_hh_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_requestcode_household_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_code_confirm_address_get_cases_error_hi_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_requestcode_individual_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_code_confirm_address_get_cases_error_hi_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_requestcode_individual_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_500_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_code_confirm_address_get_cases_error_hi_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_requestcode_individual_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_get_fulfilment_error_hh_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=E&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_requestcode_household_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_get_fulfilment_error_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=W&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_requestcode_household_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_get_fulfilment_error_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=N&deliveryChannel=SMS&productGroup=UAC&individual=false',
                                    status=400)

            await self.client.request('GET', self.get_requestcode_household_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_get_fulfilment_error_hi_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=E&deliveryChannel=SMS&productGroup=UAC&individual=true',
                                    status=400)

            await self.client.request('GET', self.get_requestcode_individual_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_get_fulfilment_error_hi_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=W&deliveryChannel=SMS&productGroup=UAC&individual=true',
                                    status=400)

            await self.client.request('GET', self.get_requestcode_individual_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_get_fulfilment_error_hi_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni
            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=N&deliveryChannel=SMS&productGroup=UAC&individual=true',
                                    status=400)

            await self.client.request('GET', self.get_requestcode_individual_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_request_fulfilment_error_hh_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
                'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_requestcode_household_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_request_fulfilment_error_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
                'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_requestcode_household_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_request_fulfilment_error_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
                'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_requestcode_household_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_request_fulfilment_error_hi_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
                'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_requestcode_individual_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_request_fulfilment_error_hi_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
                'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_requestcode_individual_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_500_error_cy, contents)

    @unittest_run_loop
    async def test_request_code_confirm_mobile_request_fulfilment_error_hi_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
                'app.requests_handlers.RequestCommon.get_fulfilment') as mocked_get_fulfilment, aioresponses(
            passthrough=[str(self.server._root)]) as mocked_aioresponses\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            await self.client.request('GET', self.get_requestcode_individual_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_confirm_address_input_yes)
            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_code_timeout_hh_en(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_requestcode_household_timeout_en)
        self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_timeout_en, contents)

    @unittest_run_loop
    async def test_get_request_code_timeout_hh_cy(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_requestcode_household_timeout_cy)
        self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_timeout_cy, contents)

    @unittest_run_loop
    async def test_get_request_code_timeout_hh_ni(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_requestcode_household_timeout_ni)
        self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_timeout_en, contents)

    @unittest_run_loop
    async def test_get_request_code_timeout_hi_en(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_timeout_en)
        self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_timeout_en, contents)

    @unittest_run_loop
    async def test_get_request_code_timeout_hi_cy(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_timeout_cy)
        self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_timeout_cy, contents)

    @unittest_run_loop
    async def test_get_request_code_timeout_hi_ni(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_timeout_ni)
        self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_timeout_en, contents)

    @unittest_run_loop
    async def test_post_request_code_enter_address_bad_postcode_hh_en(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_requestcode_household_en)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hh_en,
                data=self.request_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_request_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_code_enter_address_bad_postcode_hh_cy(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_requestcode_household_cy)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hh_cy,
                data=self.request_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_request_enter_address_title_cy, contents)
        self.assertIn(self.content_request_enter_address_error_cy, contents)
        self.assertIn(self.content_request_enter_address_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_code_enter_address_bad_postcode_hh_ni(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_requestcode_household_ni)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hh_ni,
                data=self.request_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_request_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hi_en(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_requestcode_individual_en)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hi_en,
                data=self.request_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_request_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hi_cy(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_requestcode_individual_cy)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hi_cy,
                data=self.request_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_request_enter_address_title_cy, contents)
        self.assertIn(self.content_request_enter_address_error_cy, contents)
        self.assertIn(self.content_request_enter_address_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hi_ni(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_requestcode_individual_ni)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hi_ni,
                data=self.request_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_request_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_get_request_address_not_listed_hh_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_requestcode_household_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/address-not-listed'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_address_not_listed_en, contents)

    @unittest_run_loop
    async def test_get_request_address_not_listed_hh_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_requestcode_household_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_not_listed_cy)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/address-not-listed'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_address_not_listed_cy, contents)

    @unittest_run_loop
    async def test_get_request_address_not_listed_hh_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_requestcode_household_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/address-not-listed'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_address_not_listed_en, contents)

    @unittest_run_loop
    async def test_get_request_address_not_listed_hi_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_requestcode_individual_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/address-not-listed'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_address_not_listed_en, contents)

    @unittest_run_loop
    async def test_get_request_address_not_listed_hi_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_requestcode_individual_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_select_address_input_not_listed_cy)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/address-not-listed'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_address_not_listed_cy, contents)

    @unittest_run_loop
    async def test_get_request_address_not_listed_hi_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_requestcode_individual_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/address-not-listed'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_address_not_listed_en, contents)

    @unittest_run_loop
    async def test_get_request_address_in_scotland_hh_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn'
        ) as mocked_get_cases_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en

            await self.client.request('GET', self.get_requestcode_household_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_select_address_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_address_in_scotland_hh_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn'
        ) as mocked_get_cases_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy

            await self.client.request('GET', self.get_requestcode_household_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_select_address_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_address_in_scotland_cy, contents)

    @unittest_run_loop
    async def test_get_request_address_in_scotland_hh_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn'
        ) as mocked_get_cases_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni

            await self.client.request('GET', self.get_requestcode_household_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hh_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_select_address_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_address_in_scotland_hi_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn'
        ) as mocked_get_cases_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_en

            await self.client.request('GET', self.get_requestcode_individual_en)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_en)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_select_address_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_address_in_scotland_hi_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn'
        ) as mocked_get_cases_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_cy

            await self.client.request('GET', self.get_requestcode_individual_cy)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_cy)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_select_address_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_address_in_scotland_cy, contents)

    @unittest_run_loop
    async def test_get_request_address_in_scotland_hi_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_cases_by_uprn'
        ) as mocked_get_cases_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn_ni

            await self.client.request('GET', self.get_requestcode_individual_ni)
            await self.client.request('GET', self.get_requestcode_enter_address_hi_ni)
            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_select_address_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)
