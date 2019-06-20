import json
import datetime
from unittest import mock
from urllib.parse import urlsplit, parse_qs

from aiohttp.client_exceptions import ClientConnectionError, ClientConnectorError
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app import (
    BAD_CODE_MSG, BAD_RESPONSE_MSG, INVALID_CODE_MSG, NOT_AUTHORIZED_MSG, WEBCHAT_MISSING_QUERY_MSG,
    WEBCHAT_MISSING_LANGUAGE_MSG, WEBCHAT_MISSING_NAME_MSG)
from app.exceptions import InactiveCaseError, InvalidEqPayLoad, WebChatClosedError
from app.handlers import Index, WebChat

from . import RHTestCase, build_eq_raises, skip_build_eq, skip_encrypt


class TestHandlers(RHTestCase):

    @unittest_run_loop
    async def test_get_index(self):
        response = await self.client.request("GET", self.get_index)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('Your 16 character access code is on the letter we sent you', contents)
        self.assertEqual(contents.count('input-text'), 4)
        self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_cookies_privacy(self):
        response = await self.client.request("GET", self.get_cookies_privacy)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('Cookies and Privacy', contents)

    @unittest_run_loop
    async def test_get_contact_us(self):
        response = await self.client.request("GET", self.get_contact_us)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('Contact us', contents)

    @skip_build_eq
    @unittest_run_loop
    async def test_post_index(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)

            response = await self.client.request("POST", self.post_index, allow_redirects=False, data=self.form_data)

        self.assertEqual(response.status, 200)
        self.assertIn('Is this address correct', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_connector_error(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, exception=ClientConnectorError(mock.MagicMock(), mock.MagicMock()))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index, allow_redirects=False, data=self.form_data)
            self.assertLogLine(cm, "Service connection error")

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_no_iac_json(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, content_type='text')

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index, allow_redirects=False, data=self.form_data)
            self.assertLogLine(cm, "Service failed to return expected JSON payload")

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_case_connector_error(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, exception=ClientConnectorError(mock.MagicMock(), mock.MagicMock()))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Service connection error")

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_with_build_connection_error(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index, allow_redirects=False, data=self.form_data)
            self.assertLogLine(cm, "Service connection error", message='Failed')

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)

            response = await self.client.request("POST", self.post_index, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(self.eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in self.eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(self.eq_payload[key], token[key], key)  # outputs failed key as msg

    @build_eq_raises
    @unittest_run_loop
    async def test_post_index_build_raises_InvalidEqPayLoad(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)

            response = await self.client.request("POST", self.post_index, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request("POST", self.post_address_confirmation, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Service failed to build eQ payload")

        # then error handler catches exception and renders error.html
        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_malformed(self):
        form_data = self.form_data.copy()
        del form_data['iac4']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)

            with self.assertLogs('respondent-home', 'WARNING') as cm:
                response = await self.client.request("POST", self.post_index, data=form_data)
            self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(BAD_CODE_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_iac_active_missing(self):
        iac_json = self.uac_json.copy()
        del iac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=iac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an inactive access code")

        self.assertEqual(response.status, 200)
        self.assertIn('Survey complete', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_iac_inactive(self):
        iac_json = self.uac_json.copy()
        iac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=iac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an inactive access code")

        self.assertEqual(response.status, 200)
        self.assertIn('Survey complete', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_iac_service_connection_error(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Client failed to connect to RH service")

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_iac_service_500(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=500)

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_iac_service_503(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=503)

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_iac_service_404(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an invalid access code", client_ip=None)

        self.assertEqual(response.status, 202)
        self.assertMessagePanel(INVALID_CODE_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_iac_service_403(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Unauthorized access to RH service attempted", client_ip=None)

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(NOT_AUTHORIZED_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_iac_service_401(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Unauthorized access to RH service attempted", client_ip=None)

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(NOT_AUTHORIZED_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_iac_service_400(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Client error when accessing RH service", client_ip=None, status=400)

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(BAD_RESPONSE_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_check_open_weekday_open(self):
        mocked_now = datetime.datetime(2019, 6, 17, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            WebChat.check_open()

    @unittest_run_loop
    async def test_check_open_weekday_closed(self):
        mocked_now = datetime.datetime(2019, 6, 16, 19, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            with self.assertRaises(WebChatClosedError):
                WebChat.check_open()

    @unittest_run_loop
    async def test_check_open_saturday_open(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            WebChat.check_open()

    @unittest_run_loop
    async def test_check_open_saturday_closed(self):
        mocked_now = datetime.datetime(2019, 6, 15, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            with self.assertRaises(WebChatClosedError):
                WebChat.check_open()

    @unittest_run_loop
    async def test_check_open_sunday_closed(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            with self.assertRaises(WebChatClosedError):
                WebChat.check_open()

    @unittest_run_loop
    async def test_get_webchat_open(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            response = await self.client.request("GET", self.get_webchat)
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn('Enter your name', contents)
            self.assertEqual(contents.count('radio__input'), 9)
            self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            response = await self.client.request("GET", self.get_webchat)

            self.assertRaises(WebChatClosedError)
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_query(self):
        form_data = self.webchat_form_data.copy()
        del form_data['query']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.get_webchat)

            with self.assertLogs('respondent-home', 'WARNING') as cm:
                response = await self.client.request("POST", self.post_webchat, data=form_data)
            self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(WEBCHAT_MISSING_QUERY_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_webchat_incomplete_query(self):
        form_data = self.webchat_form_data.copy()
        del form_data['language']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.get_webchat)

            with self.assertLogs('respondent-home', 'WARNING') as cm:
                response = await self.client.request("POST", self.post_webchat, data=form_data)
            self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(WEBCHAT_MISSING_LANGUAGE_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_webchat_chat(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.get_webchat)

            response = await self.client.request("POST", self.post_webchat, allow_redirects=False, data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        self.assertIn('iframe', str(await response.content.read()))

    def test_join_iac(self):
        # Given some post data
        post_data = {'iac1': '1234', 'iac2': '5678', 'iac3': '9012', 'iac4': '1314', 'action[save_continue]': ''}

        # When join_iac is called
        result = Index.join_iac(post_data)

        # Then a single string built from the iac values is returned
        self.assertEqual(result, post_data['iac1'] + post_data['iac2'] + post_data['iac3'] + post_data['iac4'])

    def test_join_iac_missing(self):
        # Given some missing post data
        post_data = {'action[save_continue]': ''}

        # When join_iac is called
        with self.assertRaises(TypeError):
            Index.join_iac(post_data)
        # Then a TypeError is raised

    def test_join_iac_some_missing(self):
        # Given some missing post data
        post_data = {'iac1': '1234', 'iac2': '5678', 'iac3': '1234', 'iac4': '', 'action[save_continue]': ''}

        # When join_iac is called
        with self.assertRaises(TypeError):
            Index.join_iac(post_data)
        # Then a TypeError is raised

    def test_validate_case(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'OK'}

        # When validate_case is called
        Index.validate_case(case_json)

        # Nothing happens

    def test_validate_case_inactive(self):
        # Given a dict with an active key and value
        case_json = {'active': False, 'caseStatus': 'OK'}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            Index.validate_case(case_json)

        # Then an InactiveCaseError is raised

    def test_validate_caseStatus_notfound(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'NOT_FOUND'}

        # When validate_case is called
        with self.assertRaises(InvalidEqPayLoad):
            Index.validate_case(case_json)

        # Then an InvalidEqPayload is raised

    def test_validate_case_empty(self):
        # Given an empty dict
        case_json = {}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            Index.validate_case(case_json)

        # Then an InactiveCaseError is raised