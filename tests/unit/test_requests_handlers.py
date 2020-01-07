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
    async def test_post_request_access_code_enter_mobile_invalid_hh_en(self):
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
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('What is your mobile phone number?', contents)
                self.assertIn('Enter a valid UK mobile phone number', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_cy(self):
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
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn('Beth yw eich rhif', contents)
                self.assertIn(' dilys yn y Deyrnas Unedig', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ni(self):
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
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('What is your mobile phone number?', contents)
                self.assertIn('Enter a valid UK mobile phone number', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hi_en(self):
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
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('What is your mobile phone number?', contents)
                self.assertIn('Enter a valid UK mobile phone number', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hi_cy(self):
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
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn('Beth yw eich rhif', contents)
                self.assertIn(' dilys yn y Deyrnas Unedig', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hi_ni(self):
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
                                                         data=self.request_code_enter_mobile_form_data_invalid)
                self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-mobile'")
                self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")
                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('What is your mobile phone number?', contents)
                self.assertIn('Enter a valid UK mobile phone number', contents)

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hh_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'request-access-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('Select an address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hh_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'request-access-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Dewiswch eich cyfeiriad', str(resp_content))
            self.assertIn('Dewiswch gyfeiriad', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hh_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'request-access-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('Select an address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hi_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'request-individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('Select an address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hi_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'request-individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Dewiswch eich cyfeiriad', str(resp_content))
            self.assertIn('Dewiswch gyfeiriad', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_hi_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_code_select_address_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'request-individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('Select an address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hh_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_code_confirm_address_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('Check and confirm the address', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hh_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_code_confirm_address_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Ydy&#39;r cyfeiriad hwn yn gywir?', str(resp_content))
            self.assertIn("Edrychwch eto ar y cyfeiriad a\\\'i gadarnhau", str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hh_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_code_confirm_address_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('Check and confirm the address', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hi_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_code_confirm_address_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('Check and confirm the address', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hi_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_code_confirm_address_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Ydy&#39;r cyfeiriad hwn yn gywir?', str(resp_content))
            self.assertIn("Edrychwch eto ar y cyfeiriad a\\\'i gadarnhau", str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_hi_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_code_confirm_address_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('Check and confirm the address', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hh_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_code_address_confirmation_data_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('Check and confirm the address', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))


    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hh_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_code_address_confirmation_data_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Ydy&#39;r cyfeiriad hwn yn gywir?', str(resp_content))
            self.assertIn("Edrychwch eto ar y cyfeiriad a\\\'i gadarnhau", str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hh_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_code_address_confirmation_data_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('Check and confirm the address', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hi_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_code_address_confirmation_data_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('Check and confirm the address', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hi_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_code_address_confirmation_data_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Ydy&#39;r cyfeiriad hwn yn gywir?', str(resp_content))
            self.assertIn("Edrychwch eto ar y cyfeiriad a\\\'i gadarnhau", str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_hi_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_code_address_confirmation_data_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('Check and confirm the address', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hh_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_code_address_confirmation_data_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'request-access-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('What is your postcode?', str(resp_content))
            self.assertIn('To text you a new code we need to know the address for which you are answering.', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hh_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_code_address_confirmation_data_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'request-access-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('What is your postcode?', str(resp_content))
            self.assertIn('To text you a new code we need to know the address for which you are answering.', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hh_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_code_address_confirmation_data_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'request-access-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Beth yw eich cod post?', str(resp_content))
            self.assertIn("Er mwyn i ni anfon cod newydd atoch chi, mae angen i ni wybod ar gyfer pa gyfeiriad rydych chi\\\'n ateb.", str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hh_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_code_address_confirmation_data_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'request-access-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('What is your postcode?', str(resp_content))
            self.assertIn('To text you a new code we need to know the address for which you are answering.', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hi_en(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_code_address_confirmation_data_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'request-individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('What is your postcode?', str(resp_content))
            self.assertIn('To text you a new code we need to know the address for which you are answering.', str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hi_cy(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_code_address_confirmation_data_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'request-individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Beth yw eich cod post?', str(resp_content))
            self.assertIn("Er mwyn i ni anfon cod newydd atoch chi, mae angen i ni wybod ar gyfer pa gyfeiriad rydych chi\\\'n ateb.", str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_hi_ni(
            self):
        with mock.patch('app.requests_handlers.RequestCodeCommon.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_code_select_address_form_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_code_address_confirmation_data_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'request-individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('What is your postcode?', str(resp_content))
            self.assertIn('To text you a new code we need to know the address for which you are answering.', str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hh_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCodeCommon.request_fulfilment') as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_household_en)
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Request a new access code', contents)
            self.assertIn('You will need to provide:', contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hh_en)
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('What is your postcode?', contents)
            self.assertIn('To text you a new code we need to know the address for which you are answering.', contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_code_select_address_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_code_address_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('What is your mobile phone number?', str(resp_content))
            self.assertIn('We will send an access code by text to this number.', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Is this mobile phone number correct?', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('We have sent an access code', str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCodeCommon.request_fulfilment') as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_household_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Gofyn am god mynediad newydd', contents)
            self.assertIn('Bydd angen i chi ddarparu:', contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hh_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Beth yw eich cod post?', contents)
            self.assertIn('Er mwyn i ni anfon cod newydd atoch chi, mae angen i ni wybod ar gyfer pa gyfeiriad rydych chi\\\'n ateb.', contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Dewiswch eich cyfeiriad', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_code_select_address_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn("Ydy\\\'r cyfeiriad hwn yn gywir?", str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_code_address_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Beth yw eich rhif ff\\xc3\\xb4n symudol?', str(resp_content))
            self.assertIn("Byddwn ni\\\'n anfon cod mynediad drwy neges destun i\\\'r rhif hwn.", str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn("Ydy\\\'r rhif ff\\xc3\\xb4n symudol hwn yn gywir?", str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Rydym ni wedi anfon cod mynediad', str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCodeCommon.request_fulfilment') as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_household_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Request a new access code', contents)
            self.assertIn('You will need to provide:', contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hh_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('What is your postcode?', contents)
            self.assertIn('To text you a new code we need to know the address for which you are answering.', contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_code_select_address_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_code_address_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('What is your mobile phone number?', str(resp_content))
            self.assertIn('We will send an access code by text to this number.', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Is this mobile phone number correct?', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('We have sent an access code', str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hi_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCodeCommon.request_fulfilment') as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_en)
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Request an individual access code', contents)
            self.assertIn('You will need to provide:', contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hi_en)
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('What is your postcode?', contents)
            self.assertIn('To text you a new code we need to know the address for which you are answering.', contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_code_select_address_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_code_address_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('What is your mobile phone number?', str(resp_content))
            self.assertIn('We will send an access code by text to this number.', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Is this mobile phone number correct?', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('We have sent an access code', str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hi_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCodeCommon.request_fulfilment') as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Gofyn am god mynediad unigryw', contents)
            self.assertIn('Bydd angen i chi ddarparu:', contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hi_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Beth yw eich cod post?', contents)
            self.assertIn('Er mwyn i ni anfon cod newydd atoch chi, mae angen i ni wybod ar gyfer pa gyfeiriad rydych chi\\\'n ateb.', contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_cy,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Dewiswch eich cyfeiriad', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_cy,
                    data=self.request_code_select_address_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn("Ydy\\\'r cyfeiriad hwn yn gywir?", str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_cy,
                    data=self.request_code_address_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Beth yw eich rhif ff\\xc3\\xb4n symudol?', str(resp_content))
            self.assertIn("Byddwn ni\\\'n anfon cod mynediad drwy neges destun i\\\'r rhif hwn.", str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn("Ydy\\\'r rhif ff\\xc3\\xb4n symudol hwn yn gywir?", str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Rydym ni wedi anfon cod mynediad', str(resp_content))

    @unittest_run_loop
    async def test_request_code_happy_path_hi_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_fulfilment') as mocked_get_fulfilment, mock.patch(
            'app.requests_handlers.RequestCodeCommon.request_fulfilment') as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_requestcode_individual_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Request an individual access code', contents)
            self.assertIn('You will need to provide:', contents)

            response = await self.client.request('GET',
                                                 self.get_requestcode_enter_address_hi_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('What is your postcode?', contents)
            self.assertIn('To text you a new code we need to know the address for which you are answering.', contents)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_code_select_address_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Is this address correct?', str(resp_content))
            self.assertIn('1 Gate Reach, Exeter, EX2 6GA', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_code_address_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('What is your mobile phone number?', str(resp_content))
            self.assertIn('We will send an access code by text to this number.', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Is this mobile phone number correct?', str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('We have sent an access code', str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hh_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn

            await self.client.request('GET', self.get_requestcode_household_en)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_en)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_en,
                    data=self.request_code_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_en,
                    data=self.request_code_select_address_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_en,
                    data=self.request_code_address_confirmation_data_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('What is your mobile phone number?', str(resp_content))
            self.assertIn('We will send an access code by text to this number.', str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn

            await self.client.request('GET', self.get_requestcode_household_cy)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_cy)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_code_select_address_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_code_address_confirmation_data_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_cy,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Beth yw eich rhif ff\\xc3\\xb4n symudol?', str(resp_content))
            self.assertIn("Byddwn ni\\\'n anfon cod mynediad drwy neges destun i\\\'r rhif hwn.", str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn

            await self.client.request('GET', self.get_requestcode_household_ni)

            await self.client.request('GET', self.get_requestcode_enter_address_hh_ni)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_ni,
                    data=self.request_code_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_ni,
                    data=self.request_code_select_address_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_ni,
                    data=self.request_code_address_confirmation_data_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hh_ni,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'request-access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('What is your mobile phone number?', str(resp_content))
            self.assertIn('We will send an access code by text to this number.', str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hi_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn

            await self.client.request('GET', self.get_requestcode_individual_en)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_en)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_en,
                    data=self.request_code_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_en,
                    data=self.request_code_select_address_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_en,
                    data=self.request_code_address_confirmation_data_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_en,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_en,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('What is your mobile phone number?', str(resp_content))
            self.assertIn('We will send an access code by text to this number.', str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hi_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn

            await self.client.request('GET', self.get_requestcode_individual_cy)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_cy)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hh_cy,
                    data=self.request_code_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hh_cy,
                    data=self.request_code_select_address_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hh_cy,
                    data=self.request_code_address_confirmation_data_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hh_cy,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_cy,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Beth yw eich rhif ff\\xc3\\xb4n symudol?', str(resp_content))
            self.assertIn("Byddwn ni\\\'n anfon cod mynediad drwy neges destun i\\\'r rhif hwn.", str(resp_content))

    @unittest_run_loop
    async def test_request_code_confirm_mobile_no_hi_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.requests_handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
            'app.requests_handlers.RequestCodeCommon.get_cases_by_uprn') as mocked_get_cases_by_uprn\
                :

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_cases_by_uprn.return_value = self.rhsvc_cases_by_uprn

            await self.client.request('GET', self.get_requestcode_individual_ni)

            await self.client.request('GET', self.get_requestcode_enter_address_hi_ni)

            await self.client.request(
                    'POST',
                    self.post_requestcode_enter_address_hi_ni,
                    data=self.request_code_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_selectaddress_hi_ni,
                    data=self.request_code_select_address_form_data_valid)

            await self.client.request(
                    'POST',
                    self.post_requestcode_address_confirmation_hi_ni,
                    data=self.request_code_address_confirmation_data_yes)

            await self.client.request(
                    'POST',
                    self.post_requestcode_entermobile_hi_ni,
                    data=self.request_code_enter_mobile_form_data_valid)

            response = await self.client.request(
                    'POST',
                    self.post_requestcode_confirm_mobile_hi_ni,
                    data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'request-individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'request-individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('What is your mobile phone number?', str(resp_content))
            self.assertIn('We will send an access code by text to this number.', str(resp_content))
