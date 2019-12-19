from unittest import mock

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses
from aiohttp_session import get_session

from app import (POSTCODE_INVALID_MSG,
                 POSTCODE_INVALID_MSG_CY)

from . import RHTestCase


class TestRequestsHandlers(RHTestCase):

    @unittest_run_loop
    async def test_get_request_access_code_hh_en(self):
        response = await self.client.request('GET',
                                             self.get_requestcode_household_en)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Request a new access code', contents)
        self.assertIn('You will need to provide:', contents)

    @unittest_run_loop
    async def test_get_request_access_code_hh_cy(self):
        response = await self.client.request('GET',
                                             self.get_requestcode_household_cy)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Gofyn am god mynediad newydd', contents)
        self.assertIn('Bydd angen i chi ddarparu:', contents)

    @unittest_run_loop
    async def test_get_request_access_code_hh_ni(self):
        response = await self.client.request('GET',
                                             self.get_requestcode_household_ni)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Request a new access code', contents)
        self.assertIn('You will need to provide:', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hh_en(
            self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hh_en,
                data=self.request_code_form_data_invalid)
        self.assertLogEvent(cm, 'attempt to use an invalid postcode')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hh_cy(
            self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hh_cy,
                data=self.request_code_form_data_invalid)
        self.assertLogEvent(cm, 'attempt to use an invalid postcode')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hh_ni(
            self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hh_ni,
                data=self.request_code_form_data_invalid)
        self.assertLogEvent(cm, 'attempt to use an invalid postcode')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hh_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hh_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Dewiswch eich cyfeiriad', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hh_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hh_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('We cannot find your address', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hh_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn('Allwn ni ddim dod o hyd', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hh_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('We cannot find your address', contents)

    # Commented out as session not maintaining the new data between pages - to be revisited.
    # @unittest_run_loop
    # async def test_get_request_code_confirm_address_hh_en(self):
    #
    #     with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
    #         mocked_get_ai_postcode.return_value = self.ai_postcode_results
    #
    #         with self.assertLogs('respondent-home', 'INFO') as cm:
    #             response = await self.client.request('POST',
    #                                                  self.post_requestcode_enter_address_hh_en,
    #                                                  data=self.request_code_form_data_valid)
    #             self.assertLogEvent(cm, 'valid postcode')
    #
    #             self.assertEqual(response.status, 200)
    #             self.assertIn('1 Gate Reach', str(await response.content.read()))
    #
    #             with self.assertLogs('respondent-home', 'INFO') as cm:
    #                 response = await self.client.request('POST', self.post_requestcode_selectaddress_hh_en,
    #                                                      data=self.post_requestcode_address_confirmation_data)
    #                 self.assertLogEvent(cm, 'session updated')
    #                 self.assertEqual(response.status, 200)

    @unittest_run_loop
    async def test_get_request_access_code_hi_en(self):
        response = await self.client.request(
            'GET', self.get_requestcode_individual_en)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Request an individual access code', contents)
        self.assertIn('You will need to provide:', contents)

    @unittest_run_loop
    async def test_get_request_access_code_hi_cy(self):
        response = await self.client.request(
            'GET', self.get_requestcode_individual_cy)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Gofyn am god mynediad unigryw', contents)
        self.assertIn('Bydd angen i chi ddarparu:', contents)

    @unittest_run_loop
    async def test_get_request_access_code_hi_ni(self):
        response = await self.client.request(
            'GET', self.get_requestcode_individual_ni)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Request an individual access code', contents)
        self.assertIn('You will need to provide:', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_address_hi_en(self):
        response = await self.client.request(
            'GET', self.get_requestcode_enter_address_hi_en)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('What is your postcode?', contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('UK postcode', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_address_hi_cy(self):
        response = await self.client.request(
            'GET', self.get_requestcode_enter_address_hi_cy)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Beth yw eich cod post?', contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('Cod post yn y Deyrnas Unedig', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_address_hi_ni(self):
        response = await self.client.request(
            'GET', self.get_requestcode_enter_address_hi_ni)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('What is your postcode?', contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('UK postcode', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hi_en(
            self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hi_en,
                data=self.request_code_form_data_invalid)
        self.assertLogEvent(cm, 'attempt to use an invalid postcode')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hi_cy(
            self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hi_cy,
                data=self.request_code_form_data_invalid)
        self.assertLogEvent(cm, 'attempt to use an invalid postcode')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hi_ni(
            self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request(
                'POST',
                self.post_requestcode_enter_address_hi_ni,
                data=self.request_code_form_data_invalid)
        self.assertLogEvent(cm, 'attempt to use an invalid postcode')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hi_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hi_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Dewiswch eich cyfeiriad', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hi_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hi_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('We cannot find your address', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hi_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_code_form_data_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn('Allwn ni ddim dod o hyd', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hi_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)
                self.assertLogEvent(cm, 'valid postcode')

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('We cannot find your address', contents)

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
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

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
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le", contents)

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
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le", contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le", contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le",
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
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le",
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
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le",
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
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_get_request_access_code_not_required_hh_en(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO'):
                    response = await self.client.request(
                        'GET', self.get_requestcode_notrequired_hh_en)

                    self.assertEqual(response.status, 200)
                    contents = str(await response.content.read())
                    self.assertIn(self.ons_logo_en, contents)
                    self.assertIn('Your address is not part of the 2019 rehearsal', contents)

    @unittest_run_loop
    async def test_get_request_access_code_not_required_hh_cy(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO'):
                    response = await self.client.request(
                        'GET', self.get_requestcode_notrequired_hh_cy)

                    self.assertEqual(response.status, 200)
                    contents = str(await response.content.read())
                    self.assertIn(self.ons_logo_cy, contents)
                    self.assertIn('Nid yw eich cyfeiriad yn rhan o ymarfer 2019', contents)

    @unittest_run_loop
    async def test_get_request_access_code_not_required_hh_ni(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO'):
                    response = await self.client.request(
                        'GET', self.get_requestcode_notrequired_hh_ni)

                    self.assertEqual(response.status, 200)
                    contents = str(await response.content.read())
                    self.assertIn(self.nisra_logo, contents)
                    self.assertIn('Your address is not part of the 2019 rehearsal', contents)

    @unittest_run_loop
    async def test_get_request_access_code_not_required_hi_en(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO'):
                    response = await self.client.request(
                        'GET', self.get_requestcode_notrequired_hi_en)

                    self.assertEqual(response.status, 200)
                    contents = str(await response.content.read())
                    self.assertIn(self.ons_logo_en, contents)
                    self.assertIn('Your address is not part of the 2019 rehearsal', contents)

    @unittest_run_loop
    async def test_get_request_access_code_not_required_hi_cy(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO'):
                    response = await self.client.request(
                        'GET', self.get_requestcode_notrequired_hi_cy)

                    self.assertEqual(response.status, 200)
                    contents = str(await response.content.read())
                    self.assertIn(self.ons_logo_cy, contents)
                    self.assertIn('Nid yw eich cyfeiriad yn rhan o ymarfer 2019', contents)

    @unittest_run_loop
    async def test_get_request_access_code_not_required_hi_ni(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO'):
                    response = await self.client.request(
                        'GET', self.get_requestcode_notrequired_hi_ni)

                    self.assertEqual(response.status, 200)
                    contents = str(await response.content.read())
                    self.assertIn(self.nisra_logo, contents)
                    self.assertIn('Your address is not part of the 2019 rehearsal', contents)

    @unittest_run_loop
    async def test_get_request_access_code_code_sent_hh_en(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_codesent_hh_en)
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/code-sent'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('We have sent an access code', contents)

    @unittest_run_loop
    async def test_get_request_access_code_code_sent_hh_cy(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_codesent_hh_cy)
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/code-sent'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn('Rydym ni wedi anfon cod mynediad', contents)

    @unittest_run_loop
    async def test_get_request_access_code_code_sent_hh_ni(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_codesent_hh_ni)
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/code-sent'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('We have sent an access code', contents)

    @unittest_run_loop
    async def test_get_request_access_code_code_sent_hi_en(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_codesent_hi_en)
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/code-sent'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('We have sent an access code', contents)

    @unittest_run_loop
    async def test_get_request_access_code_code_sent_hi_cy(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_codesent_hi_cy)
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/code-sent'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn('Rydym ni wedi anfon cod mynediad', contents)

    @unittest_run_loop
    async def test_get_request_access_code_code_sent_hi_ni(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_codesent_hi_ni)
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/code-sent'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('We have sent an access code', contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_hh_en(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET',
                                                 self.get_requestcode_household_timeout_en)
        self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Your session has timed out due to inactivity', contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_hh_cy(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET',
                                                 self.get_requestcode_household_timeout_cy)
        self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch', contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_hh_ni(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET',
                                                 self.get_requestcode_household_timeout_ni)
        self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Your session has timed out due to inactivity', contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_hi_en(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_timeout_en)
        self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Your session has timed out due to inactivity', contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_hi_cy(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_timeout_cy)
        self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch', contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_hi_ni(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_timeout_ni)
        self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Your session has timed out due to inactivity', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_mobile_hh_en(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_entermobile_hh_en)
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('What is your mobile phone number?', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_mobile_hh_cy(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_entermobile_hh_cy)
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn('Beth yw eich rhif', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_mobile_hh_ni(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_entermobile_hh_ni)
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('What is your mobile phone number?', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_mobile_hi_en(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_entermobile_hi_en)
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('What is your mobile phone number?', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_mobile_hi_cy(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_entermobile_hi_cy)
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn('Beth yw eich rhif', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_mobile_hi_ni(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('GET',
                                                         self.get_requestcode_entermobile_hi_ni)
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('What is your mobile phone number?', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_hh_en(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hh_en,
                                                         data=self.request_code_enter_mobile_form_data_valid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/confirm-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('Is this mobile phone number correct?', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_hh_cy(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hh_cy,
                                                         data=self.request_code_enter_mobile_form_data_valid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/confirm-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn(' symudol hwn yn gywir?', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_hh_ni(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hh_ni,
                                                         data=self.request_code_enter_mobile_form_data_valid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/confirm-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('Is this mobile phone number correct?', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_hi_en(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hi_en,
                                                         data=self.request_code_enter_mobile_form_data_valid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/confirm-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('Is this mobile phone number correct?', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_hi_cy(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hi_cy,
                                                         data=self.request_code_enter_mobile_form_data_valid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/confirm-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn(' symudol hwn yn gywir?', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_hi_ni(self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO'):
                await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)

                with self.assertLogs('respondent-home', 'INFO') as cm:
                    response = await self.client.request('POST',
                                                         self.post_requestcode_entermobile_hi_ni,
                                                         data=self.request_code_enter_mobile_form_data_valid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/confirm-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('Is this mobile phone number correct?', contents)
