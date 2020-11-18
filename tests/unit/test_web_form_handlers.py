from unittest import mock

from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app import (WEBFORM_MISSING_COUNTRY_MSG,
                 WEBFORM_MISSING_QUERY_MSG,
                 WEBFORM_MISSING_DESCRIPTION_MSG,
                 WEBFORM_MISSING_NAME_MSG,
                 WEBFORM_MISSING_EMAIL_EMPTY_MSG,
                 WEBFORM_MISSING_EMAIL_INVALID_MSG,
                 WEBFORM_MISSING_COUNTRY_MSG_CY,
                 WEBFORM_MISSING_QUERY_MSG_CY,
                 WEBFORM_MISSING_DESCRIPTION_MSG_CY,
                 WEBFORM_MISSING_NAME_MSG_CY,
                 WEBFORM_MISSING_EMAIL_EMPTY_MSG_CY,
                 WEBFORM_MISSING_EMAIL_INVALID_MSG)

from app.web_form_handlers import WebForm

from .helpers import TestHelpers


# noinspection PyTypeChecker
class TestWebFormHandlers(TestHelpers):

    async def form_submission_incomplete(self, url, display_region, missing_value):
        form_data = self.webform_form_data.copy()
        del form_data[missing_value]

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=form_data)
        self.assertLogEvent(cm, 'web form submission error')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.get_logo(display_region), contents)
        if missing_value == 'country':
            if display_region == 'cy':
                self.assertMessagePanel(WEBFORM_MISSING_COUNTRY_MSG_CY, contents)
            else:
                self.assertMessagePanel(WEBFORM_MISSING_COUNTRY_MSG, contents)
        elif missing_value == 'query':
            if display_region == 'cy':
                self.assertMessagePanel(WEBFORM_MISSING_QUERY_MSG_CY, contents)
            else:
                self.assertMessagePanel(WEBFORM_MISSING_QUERY_MSG, contents)
        elif missing_value == 'description':
            if display_region == 'cy':
                self.assertMessagePanel(WEBFORM_MISSING_DESCRIPTION_MSG_CY, contents)
            else:
                self.assertMessagePanel(WEBFORM_MISSING_DESCRIPTION_MSG, contents)
        elif missing_value == 'name':
            if display_region == 'cy':
                self.assertMessagePanel(WEBFORM_MISSING_NAME_MSG_CY, contents)
            else:
                self.assertMessagePanel(WEBFORM_MISSING_NAME_MSG, contents)
        elif missing_value == 'email':
            if display_region == 'cy':
                self.assertMessagePanel(WEBFORM_MISSING_EMAIL_EMPTY_MSG_CY, contents)
            else:
                self.assertMessagePanel(WEBFORM_MISSING_EMAIL_EMPTY_MSG, contents)

    @unittest_run_loop
    async def test_form_submission_incomplete(self):
        await self.form_submission_incomplete(self.post_webform_en, 'en', 'country')
        await self.form_submission_incomplete(self.post_webform_cy, 'cy', 'country')
        await self.form_submission_incomplete(self.post_webform_ni, 'ni', 'country')
        await self.form_submission_incomplete(self.post_webform_en, 'en', 'query')
        await self.form_submission_incomplete(self.post_webform_cy, 'cy', 'query')
        await self.form_submission_incomplete(self.post_webform_ni, 'ni', 'query')
        await self.form_submission_incomplete(self.post_webform_en, 'en', 'description')
        await self.form_submission_incomplete(self.post_webform_cy, 'cy', 'description')
        await self.form_submission_incomplete(self.post_webform_ni, 'ni', 'description')
        await self.form_submission_incomplete(self.post_webform_en, 'en', 'name')
        await self.form_submission_incomplete(self.post_webform_cy, 'cy', 'name')
        await self.form_submission_incomplete(self.post_webform_ni, 'ni', 'name')
        await self.form_submission_incomplete(self.post_webform_en, 'en', 'email')
        await self.form_submission_incomplete(self.post_webform_cy, 'cy', 'email')
        await self.form_submission_incomplete(self.post_webform_ni, 'ni', 'email')
