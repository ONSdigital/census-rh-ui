import json

from urllib.parse import urlsplit, parse_qs

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app import (BAD_CODE_MSG, INVALID_CODE_MSG,
                 BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY)
from app.exceptions import InactiveCaseError, InvalidEqPayLoad
from app.start_handlers import Start

from . import build_eq_raises, skip_encrypt

from .helpers import TestHelpers

attempts_retry_limit = 5


# noinspection PyTypeChecker
class TestStartHandlers(TestHelpers):
    user_journey = 'start'

    @unittest_run_loop
    async def test_post_start_with_retry_503_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, 2)
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_503_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, 2)
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, 2)
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/cy/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_503_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, 2)
            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/ni/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_ConnectionError_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_ConnectionError_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_ConnectionError_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/cy/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_ConnectionError_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))
            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/ni/start/confirm-address', response.headers['Location'])

    @build_eq_raises
    @unittest_run_loop
    async def test_post_start_build_raises_InvalidEqPayLoad_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/confirm-address',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        # then error handler catches exception and renders error.html
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @build_eq_raises
    @unittest_run_loop
    async def test_post_start_build_raises_InvalidEqPayLoad_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/confirm-address',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        # then error handler catches exception and renders error.html
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @build_eq_raises
    @unittest_run_loop
    async def test_post_start_build_raises_InvalidEqPayLoad_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/cy/start/confirm-address/',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        # then error handler catches exception and renders error.html
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

    @build_eq_raises
    @unittest_run_loop
    async def test_post_start_build_raises_InvalidEqPayLoad_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_n)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/confirm-address/',
                          response.headers['Location'])

            response = await self.client.request('POST',
                                                 self.post_start_confirm_address_ni,
                                                 allow_redirects=False,
                                                 data=self.start_confirm_address_data_yes)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/language-options/',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request(
                    'POST',
                    self.post_start_language_options_ni,
                    allow_redirects=False,
                    data=self.start_ni_language_option_data_yes)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        # then error handler catches exception and renders error.html
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_invalid_blank_ew(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = ''

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'access code not supplied')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_start_invalid_blank_cy(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = ''

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'access code not supplied')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('<a href="/en/start/" lang="en" >English</a>', contents)
        self.assertMessagePanel(BAD_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_start_invalid_blank_ni(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = ''

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 data=form_data)
        self.assertLogEvent(cm, 'access code not supplied')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_start_invalid_text_url_ew(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_start_invalid_text_url_cy(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('<a href="/en/start/" lang="en" >English</a>', contents)
        self.assertMessagePanel(BAD_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_start_invalid_text_url_ni(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_start_invalid_text_random_ew(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_start_invalid_text_random_cy(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('<a href="/en/start/" lang="en" >English</a>', contents)
        self.assertMessagePanel(BAD_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_start_invalid_text_random_ni(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_start_uac_active_missing_ew_e(self):
        uac_json = self.uac_json_e.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_start_uac_expired_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_active_missing_ew_w(self):
        uac_json = self.uac_json_w.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_start_uac_expired_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_active_missing_cy(self):
        uac_json = self.uac_json_w.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_start_uac_expired_cy, contents)

    @unittest_run_loop
    async def test_post_start_uac_active_missing_ni(self):
        uac_json = self.uac_json_n.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_start_uac_expired_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_inactive_ew_e(self):
        uac_json = self.uac_json_e.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_start_uac_expired_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_inactive_ew_w(self):
        uac_json = self.uac_json_w.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_start_uac_expired_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_inactive_cy(self):
        uac_json = self.uac_json_w.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_start_uac_expired_cy, contents)

    @unittest_run_loop
    async def test_post_start_uac_inactive_ni(self):
        uac_json = self.uac_json_n.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_start_uac_expired_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_case_status_not_found_ew_e(self):
        uac_json = self.uac_json_e.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_case_status_not_found_ew_w(self):
        uac_json = self.uac_json_w.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_case_status_not_found_cy(self):
        uac_json = self.uac_json_w.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_uac_case_status_not_found_ni(self):
        uac_json = self.uac_json_n.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_connection_error_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_connection_error_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_connection_error_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_500_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_500_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    def mock503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.rhsvc_url, status=503)

    @unittest_run_loop
    async def test_post_start_get_uac_503_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_503_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_404_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'attempt to use an invalid access code',
                                client_ip=None)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', contents)
        self.assertMessagePanel(INVALID_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_404_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'attempt to use an invalid access code',
                                client_ip=None)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('<a href="/en/start/" lang="en" >English</a>', contents)
        self.assertMessagePanel(INVALID_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_404_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'attempt to use an invalid access code',
                                client_ip=None)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(INVALID_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_403_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_403_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_403_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_401_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_401_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_400_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_400_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_400_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_start_confirm_address_survey_launched_connection_error_ew_e(
            self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched,
                        exception=ClientConnectionError('Failed'))

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url_surveylaunched)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_start_confirm_address_survey_launched_connection_error_ew_w(
            self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched,
                        exception=ClientConnectionError('Failed'))

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url_surveylaunched)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_start_confirm_address_survey_launched_connection_error_cy(
            self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched,
                        exception=ClientConnectionError('Failed'))

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url_surveylaunched)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_start_confirm_address_survey_launched_connection_error_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_n)
            mocked.post(self.rhsvc_url_surveylaunched,
                        exception=ClientConnectionError('Failed'))

            await self.client.request('POST', self.post_start_ni, data=self.start_data_valid)

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      data=self.start_confirm_address_data_yes)

            await self.client.request('POST', self.post_start_language_options_ni,
                                      data=self.start_ni_language_option_data_no)

            response = await self.client.request(
                'POST',
                self.post_start_select_language_ni,
                allow_redirects=False,
                data=self.start_ni_select_language_data_ul)

            self.assertLogEvent(cm, 'client failed to connect', url=self.rhsvc_url_surveylaunched)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_401_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched, status=401)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_401_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=401)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=401)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_404_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched, status=404)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_404_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=404)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_404_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=404)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                'POST',
                self.post_start_confirm_address_cy,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_500_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched, status=500)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=500)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_500_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=500)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=500)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=500)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=500)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_429_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched, status=429)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=429)

            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_429_error_eq_launch_title_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_429_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=429)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=429)

            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_429_error_eq_launch_title_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_429_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=429)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=429)

            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_429_error_eq_launch_title_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_429_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_n)
            mocked.post(self.rhsvc_url_surveylaunched, status=429)

            await self.client.request('POST', self.post_start_ni, data=self.start_data_valid)

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      data=self.start_confirm_address_data_yes)

            await self.client.request('POST', self.post_start_language_options_ni,
                                      data=self.start_ni_language_option_data_no)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_select_language_ni,
                    allow_redirects=False,
                    data=self.start_ni_select_language_data_ul)
            self.assertLogEvent(cm, 'error in response', status_code=429)

            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_429_error_eq_launch_title_en, contents)
            self.assertIn(self.nisra_logo, contents)

    def test_uac_hash(self):
        # Given some post data
        post_data = {'uac': 'w4nw wpph jjpt p7fn', 'action[save_continue]': ''}

        # When join_uac is called
        result = Start.uac_hash(post_data['uac'])

        # Then a single string built from the uac values is returned
        self.assertEqual(result, '54598f02da027026a584fd0bc7176de55a3e6472f4b3c74f68d0ae7be206e17c')

    def test_join_uac_missing(self):
        # Given some missing post data
        post_data = {'uac': '', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            Start.uac_hash(post_data['uac'])
        # Then a TypeError is raised

    def test_join_uac_some_missing(self):
        # Given some missing post data
        post_data = {'uac': '123456781234', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            Start.uac_hash(post_data['uac'])
        # Then a TypeError is raised

    def test_validate_case(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'OK'}

        # When validate_case is called
        Start.validate_case(case_json)

        # Nothing happens

    def test_validate_case_inactive(self):
        # Given a dict with an active key and value
        case_json = {'active': False, 'caseStatus': 'OK'}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            Start.validate_case(case_json)

        # Then an InactiveCaseError is raised

    def test_validate_caseStatus_notfound(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'NOT_FOUND'}

        # When validate_case is called
        with self.assertRaises(InvalidEqPayLoad):
            Start.validate_case(case_json)

        # Then an InvalidEqPayload is raised

    def test_validate_case_empty(self):
        # Given an empty dict
        case_json = {}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            Start.validate_case(case_json)

        # Then an InactiveCaseError is raised

    @unittest_run_loop
    async def test_no_direct_access(self):
        await self.assert_no_direct_access(self.get_start_confirm_address_en, 'en', 'GET')
        await self.assert_no_direct_access(self.get_start_confirm_address_cy, 'cy', 'GET')
        await self.assert_no_direct_access(self.get_start_confirm_address_ni, 'ni', 'GET')
        await self.assert_no_direct_access(self.post_start_confirm_address_en, 'en', 'POST',
                                           self.start_confirm_address_data_yes)
        await self.assert_no_direct_access(self.post_start_confirm_address_cy, 'cy', 'POST',
                                           self.start_confirm_address_data_yes)
        await self.assert_no_direct_access(self.post_start_confirm_address_ni, 'ni', 'POST',
                                           self.start_confirm_address_data_yes)
        await self.assert_no_direct_access(self.get_start_language_options_ni, 'ni', 'GET')
        await self.assert_no_direct_access(self.post_start_language_options_ni, 'ni', 'POST')
        await self.assert_no_direct_access(self.get_start_select_language_ni, 'ni', 'GET')
        await self.assert_no_direct_access(self.post_start_select_language_ni, 'ni', 'POST')

    @unittest_run_loop
    async def test_post_start_confirm_address_empty_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 data=self.start_confirm_address_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_empty_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 data=self.start_confirm_address_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_empty_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            await self.client.request('GET', self.get_start_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")

            await self.client.request('POST', self.post_start_cy, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_cy,
                                                 data=self.start_confirm_address_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/start/confirm-address/" lang="en" >English</a>', contents)
            self.assertIn(self.content_common_save_and_exit_link_cy, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_cy, contents)
            self.assertIn(self.content_start_confirm_address_title_cy, contents)
            self.assertIn(self.content_start_confirm_address_error_cy, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_empty_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_ni,
                                                 data=self.start_confirm_address_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_invalid_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 data=self.start_confirm_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_invalid_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 data=self.start_confirm_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_invalid_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            await self.client.request('GET', self.get_start_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")

            await self.client.request('POST', self.post_start_cy, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_cy,
                                                 data=self.start_confirm_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/start/confirm-address/" lang="en" >English</a>', contents)
            self.assertIn(self.content_common_save_and_exit_link_cy, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_cy, contents)
            self.assertIn(self.content_start_confirm_address_title_cy, contents)
            self.assertIn(self.content_start_confirm_address_error_cy, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_invalid_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_ni,
                                                 data=self.start_confirm_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_ni_language_options_invalid(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)
            mocked.put(self.rhsvc_put_modify_address, payload={})

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            response = await self.client.request('POST', self.post_start_language_options_ni,
                                                 data=self.start_ni_language_option_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_ni_language_options_page_title_error, contents)
            self.assertIn(self.content_start_ni_language_options_title, contents)
            self.assertIn(self.content_start_ni_language_options_error, contents)

    @unittest_run_loop
    async def test_post_start_ni_language_options_empty(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)
            mocked.put(self.rhsvc_put_modify_address, payload={})

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            response = await self.client.request('POST', self.post_start_language_options_ni,
                                                 data=self.start_ni_language_option_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_ni_language_options_page_title_error, contents)
            self.assertIn(self.content_start_ni_language_options_title, contents)
            self.assertIn(self.content_start_ni_language_options_error, contents)

    @unittest_run_loop
    async def test_get_ni_select_language(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)
            mocked.put(self.rhsvc_put_modify_address, payload={})

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            response = await self.client.request('POST', self.post_start_language_options_ni,
                                                 allow_redirects=False,
                                                 data=self.start_ni_language_option_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")

            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/select-language', response.headers['Location'])

            response = await self.client.request('GET', self.get_start_select_language_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/select-language'")

            contents = str(await response.content.read())
            self.assertIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_ni_select_language_page_title, contents)
            self.assertIn(self.content_start_ni_select_language_title, contents)
            self.assertIn(self.content_start_ni_select_language_switch_back, contents)
            self.assertIn(self.nisra_logo, contents)

    @unittest_run_loop
    async def test_post_ni_select_language_empty(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)
            mocked.put(self.rhsvc_put_modify_address, payload={})

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            await self.client.request('POST', self.post_start_language_options_ni,
                                      allow_redirects=False,
                                      data=self.start_ni_language_option_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")

            response = await self.client.request('POST', self.post_start_select_language_ni,
                                                 data=self.start_ni_select_language_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/select-language'")

            contents = str(await response.content.read())
            self.assertIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_ni_select_language_page_title_error, contents)
            self.assertIn(self.content_start_ni_select_language_title, contents)
            self.assertIn(self.content_start_ni_select_language_error, contents)
            self.assertIn(self.content_start_ni_select_language_switch_back, contents)
            self.assertIn(self.nisra_logo, contents)

    @unittest_run_loop
    async def test_post_ni_select_language_invalid(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)
            mocked.put(self.rhsvc_put_modify_address, payload={})

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            await self.client.request('POST', self.post_start_language_options_ni,
                                      data=self.start_ni_language_option_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")

            response = await self.client.request('POST', self.post_start_select_language_ni,
                                                 data=self.start_ni_select_language_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/select-language'")

            contents = str(await response.content.read())
            self.assertIn(self.content_common_save_and_exit_link_en, contents)
            self.assertIn(self.content_start_ni_select_language_page_title_error, contents)
            self.assertIn(self.content_start_ni_select_language_title, contents)
            self.assertIn(self.content_start_ni_select_language_error, contents)
            self.assertIn(self.content_start_ni_select_language_switch_back, contents)
            self.assertIn(self.nisra_logo, contents)

    @unittest_run_loop
    async def test_get_signed_out_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_signed_out_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/signed-out'")
            self.assertLogEvent(cm, "identity not previously remembered")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_signed_out_page_title_en, contents)
            self.assertIn(self.content_signed_out_title_en, contents)
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/signed-out/" lang="cy" >Cymraeg</a>', contents)

    @unittest_run_loop
    async def test_get_signed_out_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_signed_out_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/signed-out'")
            self.assertLogEvent(cm, "identity not previously remembered")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_signed_out_page_title_cy, contents)
            self.assertIn(self.content_signed_out_title_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/signed-out/" lang="en" >English</a>', contents)

    @unittest_run_loop
    async def test_get_signed_out_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_signed_out_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/signed-out'")
            self.assertLogEvent(cm, "identity not previously remembered")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_signed_out_page_title_en, contents)
            self.assertIn(self.content_signed_out_title_en, contents)
            self.assertIn(self.nisra_logo, contents)

    @unittest_run_loop
    async def test_get_index_with_invalid_adlocation_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_adlocation_invalid_en)

        self.assertEqual(response.status, 200)
        self.assertLogEvent(cm, "assisted digital query parameter not numeric - ignoring")
        contents = str(await response.content.read())
        self.assertIn(self.content_start_uac_title_en, contents)
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('<a href="/cy/start/?adlocation=invalid" lang="cy" >Cymraeg</a>', contents)
        self.assertIn('type="submit"', contents)
        self.assertNotIn('type="hidden"', contents)
        self.assertNotIn('value="invalid"', contents)

    @unittest_run_loop
    async def test_get_index_with_invalid_adlocation_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_adlocation_invalid_cy)

        self.assertEqual(response.status, 200)
        self.assertLogEvent(cm, "assisted digital query parameter not numeric - ignoring")
        contents = str(await response.content.read())
        self.assertIn(self.content_start_uac_title_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('<a href="/en/start/?adlocation=invalid" lang="en" >English</a>', contents)
        self.assertIn('type="submit"', contents)
        self.assertNotIn('type="hidden"', contents)
        self.assertNotIn('value="invalid"', contents)

    @unittest_run_loop
    async def test_get_index_with_invalid_adlocation_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_adlocation_invalid_ni)

        self.assertEqual(response.status, 200)
        self.assertLogEvent(cm, "assisted digital query parameter not numeric - ignoring")
        contents = str(await response.content.read())
        self.assertIn(self.content_start_uac_title_en, contents)
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('type="submit"', contents)
        self.assertNotIn('type="hidden"', contents)
        self.assertNotIn('value="invalid"', contents)

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-ENG'
            eq_payload['language_code'] = 'en'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/en'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_en)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")
            start_contents = str(await get_start_response.content.read())
            self.assertIn(self.ons_logo_en, start_contents)
            self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', start_contents)
            self.assertIn(self.content_start_title_en, start_contents)
            self.assertIn(self.content_start_uac_title_en, start_contents)
            self.assertEqual(start_contents.count('input--text'), 1)
            self.assertIn('type="submit"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_en,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.ons_logo_en, confirm_address_content)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_confirm_address_response.status, 302)
        redirected_url = post_confirm_address_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_with_valid_adlocation_ew_e(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-ENG'
            eq_payload['language_code'] = 'en'
            eq_payload['channel'] = 'ad'
            eq_payload['user_id'] = '1234567890'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/en'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_adlocation_valid_en)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")
            self.assertLogEvent(cm, "assisted digital query parameter found")
            start_contents = str(await get_start_response.content.read())
            self.assertIn('type="submit"', start_contents)
            self.assertIn('type="hidden"', start_contents)
            self.assertIn('value="1234567890"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_en,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid_with_adlocation)

            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.ons_logo_en, confirm_address_content)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_confirm_address_response.status, 302)
        redirected_url = post_confirm_address_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-WLS'
            eq_payload['language_code'] = 'en'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/en'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_en)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")
            start_contents = str(await get_start_response.content.read())
            self.assertIn(self.ons_logo_en, start_contents)
            self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', start_contents)
            self.assertIn(self.content_start_title_en, start_contents)
            self.assertIn(self.content_start_uac_title_en, start_contents)
            self.assertEqual(start_contents.count('input--text'), 1)
            self.assertIn('type="submit"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_en,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.ons_logo_en, confirm_address_content)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_confirm_address_response.status, 302)
        redirected_url = post_confirm_address_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_with_valid_adlocation_ew_w(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-WLS'
            eq_payload['language_code'] = 'en'
            eq_payload['channel'] = 'ad'
            eq_payload['user_id'] = '1234567890'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/en'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_adlocation_valid_en)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")
            self.assertLogEvent(cm, "assisted digital query parameter found")
            start_contents = str(await get_start_response.content.read())
            self.assertIn('type="submit"', start_contents)
            self.assertIn('type="hidden"', start_contents)
            self.assertIn('value="1234567890"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_en,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid_with_adlocation)

            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.ons_logo_en, confirm_address_content)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_confirm_address_response.status, 302)
        redirected_url = post_confirm_address_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-WLS'
            eq_payload['language_code'] = 'cy'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/cy'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_cy)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")
            start_contents = str(await get_start_response.content.read())
            self.assertIn(self.ons_logo_cy, start_contents)
            self.assertIn('<a href="/en/start/" lang="en" >English</a>', start_contents)
            self.assertIn(self.content_start_title_cy, start_contents)
            self.assertIn(self.content_start_uac_title_cy, start_contents)
            self.assertEqual(start_contents.count('input--text'), 1)
            self.assertIn('type="submit"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_cy,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.ons_logo_cy, confirm_address_content)
            self.assertIn('<a href="/en/start/confirm-address/" lang="en" >English</a>', confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_cy, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_cy, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_cy, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_cy, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_cy, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_cy,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_confirm_address_response.status, 302)
        redirected_url = post_confirm_address_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_with_valid_adlocation_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-WLS'
            eq_payload['language_code'] = 'cy'
            eq_payload['channel'] = 'ad'
            eq_payload['user_id'] = '1234567890'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/cy'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_adlocation_valid_cy)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")
            self.assertLogEvent(cm, "assisted digital query parameter found")
            start_contents = str(await get_start_response.content.read())
            self.assertIn('type="submit"', start_contents)
            self.assertIn('type="hidden"', start_contents)
            self.assertIn('value="1234567890"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_cy,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid_with_adlocation)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.ons_logo_cy, confirm_address_content)
            self.assertIn('<a href="/en/start/confirm-address/" lang="en" >English</a>', confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_cy, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_cy, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_cy, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_cy,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_confirm_address_response.status, 302)
        redirected_url = post_confirm_address_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_ni)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")
            start_contents = str(await get_start_response.content.read())
            self.assertIn(self.nisra_logo, start_contents)
            self.assertIn(self.content_start_title_en, start_contents)
            self.assertIn(self.content_start_uac_title_en, start_contents)
            self.assertEqual(start_contents.count('input--text'), 1)
            self.assertIn('type="submit"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_ni,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.nisra_logo, confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_ni,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/language-options'")

            self.assertEqual(200, post_confirm_address_response.status)
            confirm_language_options_content = str(await post_confirm_address_response.content.read())
            self.assertIn(self.nisra_logo, confirm_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_page_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_option_yes, confirm_language_options_content)

            post_ni_select_language_response = await self.client.request(
                'POST',
                self.post_start_language_options_ni,
                allow_redirects=False,
                data=self.start_ni_language_option_data_yes)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")
            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_ni_select_language_response.status, 302)
        redirected_url = post_ni_select_language_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_with_valid_adlocation_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            eq_payload['channel'] = 'ad'
            eq_payload['user_id'] = '1234567890'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_adlocation_valid_ni)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")
            self.assertLogEvent(cm, "assisted digital query parameter found")
            start_contents = str(await get_start_response.content.read())
            self.assertIn('type="submit"', start_contents)
            self.assertIn('type="hidden"', start_contents)
            self.assertIn('value="1234567890"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_ni,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid_with_adlocation)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.nisra_logo, confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_ni,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/language-options'")

            self.assertEqual(200, post_confirm_address_response.status)
            confirm_language_options_content = str(await post_confirm_address_response.content.read())
            self.assertIn(self.nisra_logo, confirm_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_page_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_option_yes, confirm_language_options_content)

            post_ni_select_language_response = await self.client.request(
                'POST',
                self.post_start_language_options_ni,
                allow_redirects=False,
                data=self.start_ni_language_option_data_yes)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")
            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_ni_select_language_response.status, 302)
        redirected_url = post_ni_select_language_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_region_n_language_en_display_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_ni)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")
            start_contents = str(await get_start_response.content.read())
            self.assertIn(self.nisra_logo, start_contents)
            self.assertIn(self.content_start_title_en, start_contents)
            self.assertIn(self.content_start_uac_title_en, start_contents)
            self.assertEqual(start_contents.count('input--text'), 1)
            self.assertIn('type="submit"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_ni,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.nisra_logo, confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_ni,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/language-options'")

            self.assertEqual(200, post_confirm_address_response.status)
            confirm_language_options_content = str(await post_confirm_address_response.content.read())
            self.assertIn(self.nisra_logo, confirm_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_page_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_option_yes, confirm_language_options_content)

            post_ni_language_options_response = await self.client.request(
                'POST',
                self.post_start_language_options_ni,
                data=self.start_ni_language_option_data_no)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/select-language'")

            self.assertEqual(200, post_ni_language_options_response.status)
            select_language_options_content = str(await post_ni_language_options_response.content.read())
            self.assertIn(self.nisra_logo, select_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_page_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_option, select_language_options_content)

            post_ni_select_language_response = await self.client.request(
                'POST',
                self.post_start_select_language_ni,
                allow_redirects=False,
                data=self.start_ni_select_language_data_en)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/select-language'")
            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_ni_select_language_response.status, 302)
        redirected_url = post_ni_select_language_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_with_valid_adlocation_region_n_language_en_display_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            eq_payload['channel'] = 'ad'
            eq_payload['user_id'] = '1234567890'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_adlocation_valid_ni)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")
            self.assertLogEvent(cm, "assisted digital query parameter found")
            start_contents = str(await get_start_response.content.read())
            self.assertIn('type="submit"', start_contents)
            self.assertIn('type="hidden"', start_contents)
            self.assertIn('value="1234567890"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_ni,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid_with_adlocation)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.nisra_logo, confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_ni,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/language-options'")

            self.assertEqual(200, post_confirm_address_response.status)
            confirm_language_options_content = str(await post_confirm_address_response.content.read())
            self.assertIn(self.nisra_logo, confirm_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_page_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_option_yes, confirm_language_options_content)

            post_ni_language_options_response = await self.client.request(
                'POST',
                self.post_start_language_options_ni,
                data=self.start_ni_language_option_data_no)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/select-language'")

            self.assertEqual(200, post_ni_language_options_response.status)
            select_language_options_content = str(await post_ni_language_options_response.content.read())
            self.assertIn(self.nisra_logo, select_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_page_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_option, select_language_options_content)

            post_ni_select_language_response = await self.client.request(
                'POST',
                self.post_start_select_language_ni,
                allow_redirects=False,
                data=self.start_ni_select_language_data_en)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/select-language'")
            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_ni_select_language_response.status, 302)
        redirected_url = post_ni_select_language_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_region_n_language_ga_display_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'ga'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_ni)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")
            start_contents = str(await get_start_response.content.read())
            self.assertIn(self.nisra_logo, start_contents)
            self.assertIn(self.content_start_title_en, start_contents)
            self.assertIn(self.content_start_uac_title_en, start_contents)
            self.assertEqual(start_contents.count('input--text'), 1)
            self.assertIn('type="submit"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_ni,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.nisra_logo, confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_ni,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/language-options'")

            self.assertEqual(200, post_confirm_address_response.status)
            confirm_language_options_content = str(await post_confirm_address_response.content.read())
            self.assertIn(self.nisra_logo, confirm_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_page_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_option_yes, confirm_language_options_content)

            post_ni_language_options_response = await self.client.request(
                'POST',
                self.post_start_language_options_ni,
                data=self.start_ni_language_option_data_no)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/select-language'")

            self.assertEqual(200, post_ni_language_options_response.status)
            select_language_options_content = str(await post_ni_language_options_response.content.read())
            self.assertIn(self.nisra_logo, select_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_page_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_option, select_language_options_content)

            post_ni_select_language_response = await self.client.request(
                'POST',
                self.post_start_select_language_ni,
                allow_redirects=False,
                data=self.start_ni_select_language_data_ga)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/select-language'")
            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_ni_select_language_response.status, 302)
        redirected_url = post_ni_select_language_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_with_valid_adlocation_region_n_language_ga_display_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'ga'
            eq_payload['channel'] = 'ad'
            eq_payload['user_id'] = '1234567890'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_adlocation_valid_ni)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")
            self.assertLogEvent(cm, "assisted digital query parameter found")
            start_contents = str(await get_start_response.content.read())
            self.assertIn('type="submit"', start_contents)
            self.assertIn('type="hidden"', start_contents)
            self.assertIn('value="1234567890"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_ni,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid_with_adlocation)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.nisra_logo, confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_ni,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/language-options'")

            self.assertEqual(200, post_confirm_address_response.status)
            confirm_language_options_content = str(await post_confirm_address_response.content.read())
            self.assertIn(self.nisra_logo, confirm_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_page_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_option_yes, confirm_language_options_content)

            post_ni_language_options_response = await self.client.request(
                'POST',
                self.post_start_language_options_ni,
                data=self.start_ni_language_option_data_no)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/select-language'")

            self.assertEqual(200, post_ni_language_options_response.status)
            select_language_options_content = str(await post_ni_language_options_response.content.read())
            self.assertIn(self.nisra_logo, select_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_page_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_option, select_language_options_content)

            post_ni_select_language_response = await self.client.request(
                'POST',
                self.post_start_select_language_ni,
                allow_redirects=False,
                data=self.start_ni_select_language_data_ga)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/select-language'")
            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_ni_select_language_response.status, 302)
        redirected_url = post_ni_select_language_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_region_n_language_ul_display_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'eo'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_ni)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")
            start_contents = str(await get_start_response.content.read())
            self.assertIn(self.nisra_logo, start_contents)
            self.assertIn(self.content_start_title_en, start_contents)
            self.assertIn(self.content_start_uac_title_en, start_contents)
            self.assertEqual(start_contents.count('input--text'), 1)
            self.assertIn('type="submit"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_ni,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.nisra_logo, confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_ni,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/language-options'")

            self.assertEqual(200, post_confirm_address_response.status)
            confirm_language_options_content = str(await post_confirm_address_response.content.read())
            self.assertIn(self.nisra_logo, confirm_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_page_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_option_yes, confirm_language_options_content)

            post_ni_language_options_response = await self.client.request(
                'POST',
                self.post_start_language_options_ni,
                data=self.start_ni_language_option_data_no)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/select-language'")

            self.assertEqual(200, post_ni_language_options_response.status)
            select_language_options_content = str(await post_ni_language_options_response.content.read())
            self.assertIn(self.nisra_logo, select_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_page_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_option, select_language_options_content)

            post_ni_select_language_response = await self.client.request(
                'POST',
                self.post_start_select_language_ni,
                allow_redirects=False,
                data=self.start_ni_select_language_data_ul)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/select-language'")
            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_ni_select_language_response.status, 302)
        redirected_url = post_ni_select_language_response.headers['location']
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

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_with_valid_adlocation_region_n_language_ul_display_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_n)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'eo'
            eq_payload['channel'] = 'ad'
            eq_payload['user_id'] = '1234567890'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_adlocation_valid_ni)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")
            self.assertLogEvent(cm, "assisted digital query parameter found")
            start_contents = str(await get_start_response.content.read())
            self.assertIn('type="submit"', start_contents)
            self.assertIn('type="hidden"', start_contents)
            self.assertIn('value="1234567890"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_ni,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid_with_adlocation)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.nisra_logo, confirm_address_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_ni,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/language-options'")

            self.assertEqual(200, post_confirm_address_response.status)
            confirm_language_options_content = str(await post_confirm_address_response.content.read())
            self.assertIn(self.nisra_logo, confirm_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_page_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_title, confirm_language_options_content)
            self.assertIn(self.content_start_ni_language_options_option_yes, confirm_language_options_content)

            post_ni_language_options_response = await self.client.request(
                'POST',
                self.post_start_language_options_ni,
                data=self.start_ni_language_option_data_no)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/select-language'")

            self.assertEqual(200, post_ni_language_options_response.status)
            select_language_options_content = str(await post_ni_language_options_response.content.read())
            self.assertIn(self.nisra_logo, select_language_options_content)
            self.assertIn(self.content_common_save_and_exit_link_en, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_page_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_title, select_language_options_content)
            self.assertIn(self.content_start_ni_select_language_option, select_language_options_content)

            post_ni_select_language_response = await self.client.request(
                'POST',
                self.post_start_select_language_ni,
                allow_redirects=False,
                data=self.start_ni_select_language_data_ul)

            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/select-language'")
            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_ni_select_language_response.status, 302)
        redirected_url = post_ni_select_language_response.headers['location']
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

    @unittest_run_loop
    async def test_start_code_in_northern_ireland_en(self):
        await self.assert_start_page_correct(self.get_start_en, 'en', ad_location=False)
        await self.assert_start_page_post_returns_address_in_northern_ireland(self.post_start_en, 'en')

    @unittest_run_loop
    async def test_start_code_in_northern_ireland_with_adlocation_en(self):
        await self.assert_start_page_correct(self.get_start_adlocation_valid_en, 'en', ad_location=True)
        await self.assert_start_page_post_returns_address_in_northern_ireland(self.post_start_en, 'en')

    @unittest_run_loop
    async def test_start_code_in_northern_ireland_cy(self):
        await self.assert_start_page_correct(self.get_start_cy, 'cy', ad_location=False)
        await self.assert_start_page_post_returns_address_in_northern_ireland(self.post_start_cy, 'cy')

    @unittest_run_loop
    async def test_start_code_in_northern_ireland_with_adlocation_cy(self):
        await self.assert_start_page_correct(self.get_start_adlocation_valid_cy, 'cy', ad_location=True)
        await self.assert_start_page_post_returns_address_in_northern_ireland(self.post_start_cy, 'cy')

    @unittest_run_loop
    async def test_start_code_in_england_ni(self):
        await self.assert_start_page_correct(self.get_start_ni, 'ni', ad_location=False)
        await self.assert_start_page_post_returns_address_in_england_and_wales(self.post_start_ni, 'ni', 'e')

    @unittest_run_loop
    async def test_start_code_in_england_with_adlocation_ni(self):
        await self.assert_start_page_correct(self.get_start_adlocation_valid_ni, 'ni', ad_location=True)
        await self.assert_start_page_post_returns_address_in_england_and_wales(self.post_start_ni, 'ni', 'e')

    @unittest_run_loop
    async def test_start_code_in_wales_ni(self):
        await self.assert_start_page_correct(self.get_start_ni, 'ni', ad_location=False)
        await self.assert_start_page_post_returns_address_in_england_and_wales(self.post_start_ni, 'ni', 'w')

    @unittest_run_loop
    async def test_start_code_in_wales_with_adlocation_ni(self):
        await self.assert_start_page_correct(self.get_start_adlocation_valid_ni, 'ni', ad_location=True)
        await self.assert_start_page_post_returns_address_in_england_and_wales(self.post_start_ni, 'ni', 'w')

    @unittest_run_loop
    async def test_start_code_ce4_en(self):
        await self.assert_start_page_correct(self.get_start_en, 'en', ad_location=False)
        await self.assert_start_page_post_ce4_code_test(self.post_start_en, 'en')

    @unittest_run_loop
    async def test_start_code_ce4_cy(self):
        await self.assert_start_page_correct(self.get_start_cy, 'cy', ad_location=False)
        await self.assert_start_page_post_ce4_code_test(self.post_start_cy, 'cy')

    @unittest_run_loop
    async def test_start_code_ce4_ni(self):
        await self.assert_start_page_correct(self.get_start_ni, 'ni', ad_location=False)
        await self.assert_start_page_post_ce4_code_test(self.post_start_ni, 'ni')

    @unittest_run_loop
    async def test_start_page_post_displays_welsh_warning(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)]) \
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            response = await self.client.request('POST', self.post_start_cy, data=self.start_data_valid)
            self.assertLogEvent(cm, self.build_url_log_entry(self.sub_user_journey, 'cy', 'POST',
                                                             include_sub_user_journey=False,
                                                             include_page=False))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', 'cy', 'GET',
                                                             include_sub_user_journey=False,
                                                             include_page=True))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo('cy'), contents)
            self.assertIn(self.content_start_confirm_address_page_title_cy, contents)
            self.assertIn(self.content_start_confirm_address_title_cy, contents)
            self.assertIn(self.content_start_confirm_address_region_warning_cy, contents)
