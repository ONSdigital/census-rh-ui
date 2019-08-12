import json
import datetime

from unittest import mock
from urllib.parse import urlsplit, parse_qs

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app import (
    BAD_CODE_MSG, INVALID_CODE_MSG, WEBCHAT_MISSING_QUERY_MSG, WEBCHAT_MISSING_LANGUAGE_MSG, WEBCHAT_MISSING_NAME_MSG,
    POSTCODE_INVALID_MSG)
from app.exceptions import InactiveCaseError, InvalidEqPayLoad
from app.handlers import Index, WebChat


from . import RHTestCase, build_eq_raises, skip_encrypt


class TestHandlers(RHTestCase):

    @unittest_run_loop
    async def test_get_index(self):
        response = await self.client.request("GET", self.get_index)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('Enter the 16 character code printed on the letter', contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_post_index(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)

            response = await self.client.request("POST", self.post_index, allow_redirects=False, data=self.form_data)

        self.assertEqual(response.status, 302)
        self.assertIn('/start/address-confirmation', response.headers['Location'])

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request("POST", self.post_index, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/address-confirmation', response.headers['Location'])

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
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request("POST", self.post_index, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request("POST", self.post_address_confirmation, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Service failed to build eQ payload")

        # then error handler catches exception and renders error.html
        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_invalid_blank(self):
        form_data = self.form_data.copy()
        del form_data['uac']

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(BAD_CODE_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_invalid_text_url(self):
        form_data = self.form_data.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(BAD_CODE_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_invalid_text_random(self):
        form_data = self.form_data.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(BAD_CODE_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_uac_active_missing(self):
        uac_json = self.uac_json.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an inactive access code")

        self.assertEqual(response.status, 200)
        self.assertIn('Survey complete', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_uac_inactive(self):
        uac_json = self.uac_json.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an inactive access code")

        self.assertEqual(response.status, 200)
        self.assertIn('Survey complete', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_uac_case_status_not_found(self):
        uac_json = self.uac_json.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Service failed to build eQ payload")

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_get_uac_connection_error(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Client failed to connect", url=self.rhsvc_url)

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_get_uac_500(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=500)

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_get_uac_503(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=503)

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_get_uac_404(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an invalid access code", client_ip=None)

        self.assertEqual(response.status, 401)
        self.assertMessagePanel(INVALID_CODE_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_get_uac_403(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=403)

            self.assertEqual(response.status, 500)
            self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_get_uac_401(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=401)

            self.assertEqual(response.status, 500)
            self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_index_get_uac_400(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=400)

            self.assertEqual(response.status, 500)
            self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @skip_encrypt
    @unittest_run_loop
    async def test_post_address_confirmation_survey_launched_connection_error(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched, exception=ClientConnectionError('Failed'))

            response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_address_confirmation, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Client failed to connect", url=self.rhsvc_url_surveylaunched)

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_401(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched, status=401)

            response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_address_confirmation, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Error in response", status_code=401)

            self.assertEqual(response.status, 500)
            self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_404(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched, status=404)

            response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertEqual(response.status, 200)

            response = await self.client.request("POST", self.post_address_confirmation, allow_redirects=False,
                                                 data=self.address_confirmation_data)

            self.assertEqual(response.status, 500)
            self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_500(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched, status=500)

            response = await self.client.request("POST", self.post_index, data=self.form_data)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_address_confirmation, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Error in response", status_code=500)

            self.assertEqual(response.status, 500)
            self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    def test_check_open_weekday_open_census_weekend(self):
        mocked_now = datetime.datetime(2019, 10, 12, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertTrue(WebChat.check_open())

    def test_check_open_weekday_closed_census_weekend(self):
        mocked_now = datetime.datetime(2019, 10, 13, 7, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    def test_check_open_weekday_open(self):
        mocked_now = datetime.datetime(2019, 6, 17, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertTrue(WebChat.check_open())

    def test_check_open_weekday_closed(self):
        mocked_now = datetime.datetime(2019, 6, 16, 19, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    def test_check_open_saturday_open(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertTrue(WebChat.check_open())

    def test_check_open_saturday_closed(self):
        mocked_now = datetime.datetime(2019, 6, 15, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    def test_check_open_sunday_closed(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

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
    async def test_get_webchat_not_open_200(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request("GET", self.get_webchat)

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_clientconnectionerror(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, exception=ClientConnectionError('Failed'))

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("GET", self.get_webchat)
                self.assertLogLine(cm, "Client failed to connect")
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_500(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=500)

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("GET", self.get_webchat)

                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_query(self):
        form_data = self.webchat_form_data.copy()
        del form_data['query']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(WEBCHAT_MISSING_QUERY_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_webchat_incomplete_language(self):
        form_data = self.webchat_form_data.copy()
        del form_data['language']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(WEBCHAT_MISSING_LANGUAGE_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_webchat_incomplete_name(self):
        form_data = self.webchat_form_data.copy()
        del form_data['screen_name']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(WEBCHAT_MISSING_NAME_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_webchat_open(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            
            response = await self.client.request("POST", self.post_webchat, allow_redirects=False,
                                                 data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        self.assertIn('iframe', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_webchat_not_open_200(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request("POST", self.post_webchat, allow_redirects=False,
                                                     data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_clientconnectionerror(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, exception=ClientConnectionError('Failed'))

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("POST", self.post_webchat, allow_redirects=False,
                                                         data=self.webchat_form_data)
                self.assertLogLine(cm, "Client failed to connect")
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_500(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=500)

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("POST", self.post_webchat, allow_redirects=False,
                                                         data=self.webchat_form_data)
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn('Bank Holidays', contents)

    def test_join_uac(self):
        # Given some post data
        post_data = {'uac': '1234567890121314', 'action[save_continue]': ''}

        # When join_uac is called
        result = Index.join_uac(post_data)

        # Then a single string built from the uac values is returned
        self.assertEqual(result, post_data['uac'])

    def test_join_uac_missing(self):
        # Given some missing post data
        post_data = {'uac': '', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            Index.join_uac(post_data)
        # Then a TypeError is raised

    def test_join_uac_some_missing(self):
        # Given some missing post data
        post_data = {'uac': '123456781234', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            Index.join_uac(post_data)
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

    @unittest_run_loop
    async def test_get_request_access_code(self):
        response = await self.client.request("GET", self.get_requestcode)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('What is your postcode?', contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('UK postcode', contents)

    @unittest_run_loop
    async def test_post_request_access_code_bad_postcode(self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_requestcode,
                                                 data=self.request_code_form_data_invalid)
        self.assertLogLine(cm, "Attempt to use an invalid postcode")

        self.assertEqual(response.status, 200)
        self.assertMessagePanel(POSTCODE_INVALID_MSG, str(await response.content.read()))

    @unittest_run_loop
    async def test_post_request_access_code_good_postcode(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Valid postcode")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_not_found(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode,
                                                     data=self.request_code_form_data_valid)
                self.assertLogLine(cm, "Valid postcode")

                self.assertEqual(response.status, 200)
                self.assertIn('We cannot find your address', str(await response.content.read()))

    # Commented out as session not maintaining the new data between pages - to be revisited.
    # @unittest_run_loop
    # async def test_get_request_code_confirm_address(self):
    #
    #     with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
    #         mocked_get_ai_postcode.return_value = self.ai_postcode_results
    #
    #         with self.assertLogs('respondent-home', 'INFO') as cm:
    #             response = await self.client.request("POST", self.post_requestcode, data=self.request_code_form_data_valid)
    #             self.assertLogLine(cm, "Valid postcode")
    #
    #             self.assertEqual(response.status, 200)
    #             self.assertIn('1 Gate Reach', str(await response.content.read()))
    #
    #             with self.assertLogs('respondent-home', 'INFO') as cm:
    #                 response = await self.client.request("POST", self.post_requestcode_selectaddress,
    #                                                      data=self.post_requestcode_address_confirmation_data)
    #                 self.assertLogLine(cm, "Session updated")
    #                 self.assertEqual(response.status, 200)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Client failed to connect", url=self.addressindexsvc_url + self.postcode_valid)

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=500)

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=503)

        self.assertEqual(response.status, 500)
        self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=403)

            self.assertEqual(response.status, 500)
            self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=401)

            self.assertEqual(response.status, 500)
            self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=400)

            self.assertEqual(response.status, 500)
            self.assertIn('Sorry, something went wrong', str(await response.content.read()))

    @unittest_run_loop
    async def test_get_address_confirmation_direct_access(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.get_address_confirmation, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        self.assertIn('Enter the 16 character code printed on the letter', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_address_confirmation_direct_access(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("POST", self.post_address_confirmation, allow_redirects=False,
                                                 data=self.address_confirmation_data)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        self.assertIn('Enter the 16 character code printed on the letter', str(await response.content.read()))

    @unittest_run_loop
    async def test_get_address_edit_direct_access(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.get_address_edit, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        self.assertIn('Enter the 16 character code printed on the letter', str(await response.content.read()))

    @unittest_run_loop
    async def test_post_address_edit_direct_access(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.post_address_edit, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        self.assertIn('Enter the 16 character code printed on the letter', str(await response.content.read()))
