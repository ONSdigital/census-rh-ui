from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app import (WEBFORM_MISSING_COUNTRY_MSG,
                 WEBFORM_MISSING_CATEGORY_MSG,
                 WEBFORM_MISSING_DESCRIPTION_MSG,
                 WEBFORM_MISSING_NAME_MSG,
                 WEBFORM_MISSING_EMAIL_EMPTY_MSG,
                 WEBFORM_MISSING_EMAIL_INVALID_MSG,
                 WEBFORM_MISSING_COUNTRY_MSG_CY,
                 WEBFORM_MISSING_CATEGORY_MSG_CY,
                 WEBFORM_MISSING_DESCRIPTION_MSG_CY,
                 WEBFORM_MISSING_NAME_MSG_CY,
                 WEBFORM_MISSING_EMAIL_EMPTY_MSG_CY,
                 WEBFORM_MISSING_EMAIL_INVALID_MSG_CY)

from .helpers import TestHelpers


# noinspection PyTypeChecker
class TestWebFormHandlers(TestHelpers):
    user_journey = 'web-form'

    def check_text_web_form(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if check_error:
                self.assertIn(self.content_web_form_page_title_error_cy, contents)
            else:
                self.assertIn(self.content_web_form_page_title_cy, contents)
            self.assertIn(self.content_web_form_title_cy, contents)
            self.assertIn(self.content_web_form_warning_cy, contents)
        else:
            if check_error:
                self.assertIn(self.content_web_form_page_title_error_en, contents)
            else:
                self.assertIn(self.content_web_form_page_title_en, contents)
            self.assertIn(self.content_web_form_title_en, contents)
            self.assertIn(self.content_web_form_warning_en, contents)

    def check_text_web_form_success(self, display_region, contents):
        if display_region == 'cy':
            self.assertIn(self.content_web_form_success_page_title_cy, contents)
            self.assertIn(self.content_web_form_success_title_cy, contents)
            self.assertIn(self.content_web_form_success_confirmation_cy, contents)
            self.assertIn(self.content_web_form_success_secondary_cy, contents)
        else:
            self.assertIn(self.content_web_form_success_page_title_en, contents)
            self.assertIn(self.content_web_form_success_title_en, contents)
            self.assertIn(self.content_web_form_success_confirmation_en, contents)
            self.assertIn(self.content_web_form_success_secondary_en, contents)

    async def form_submission_success(self, get_url, post_url, display_region):
        form_data = self.webform_form_data.copy()

        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.post(self.rhsvc_url_web_form, status=200)

            get_response = await self.client.request('GET', get_url)
            self.assertLogEvent(cm, self.build_url_log_entry('web-form', display_region, 'GET',
                                                             include_sub_user_journey=False, include_page=False))
            self.assertEqual(get_response.status, 200)
            contents = str(await get_response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('web-form', display_region, include_sub_user_journey=False,
                                                          include_page=False), contents)
            self.check_text_web_form(display_region, contents)

            post_response = await self.client.request('POST', post_url, data=form_data)
            self.assertLogEvent(cm, self.build_url_log_entry('web-form', display_region, 'POST',
                                                             include_sub_user_journey=False, include_page=False))
            self.assertLogEvent(cm, self.build_url_log_entry('web-form-success', display_region, 'GET',
                                                             include_sub_user_journey=False, include_page=False))

            self.assertEqual(post_response.status, 200)
            contents = str(await post_response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('success', display_region,
                                                          include_sub_user_journey=False,
                                                          include_page=True), contents)
            self.check_text_web_form_success(display_region, contents)

    async def form_submission_error(self, url, display_region, status):
        form_data = self.webform_form_data.copy()

        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.post(self.rhsvc_url_web_form, status=status)

            response = await self.client.request('POST', url, data=form_data)
            self.assertLogEvent(cm, self.build_url_log_entry('web-form', display_region, 'POST',
                                                             include_sub_user_journey=False, include_page=False))
            self.assertLogEvent(cm, 'error in response', status_code=status)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def form_submission_error_429(self, url, display_region):
        form_data = self.webform_form_data.copy()

        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.post(self.rhsvc_url_web_form, status=429)

            response = await self.client.request('POST', url, data=form_data)
            self.assertLogEvent(cm, self.build_url_log_entry('web-form', display_region, 'POST',
                                                             include_sub_user_journey=False, include_page=False))
            self.assertLogEvent(cm, 'too many requests', status_code=429)

            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_web_form_error_429_title_cy, contents)
            else:
                self.assertIn(self.content_web_form_error_429_title_en, contents)

    async def form_submission_incomplete(self, url, display_region, missing_value):
        form_data = self.webform_form_data.copy()
        del form_data[missing_value]

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=form_data)

            self.assertLogEvent(cm, self.build_url_log_entry('web-form', display_region, 'POST',
                                                             include_sub_user_journey=False, include_page=False))
            self.assertLogEvent(cm, 'web form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('web-form', display_region, include_sub_user_journey=False,
                                                          include_page=False), contents)
            self.check_text_web_form(display_region, contents, check_error=True)
            if missing_value == 'country':
                if display_region == 'cy':
                    self.assertMessagePanel(WEBFORM_MISSING_COUNTRY_MSG_CY, contents)
                else:
                    self.assertMessagePanel(WEBFORM_MISSING_COUNTRY_MSG, contents)
            elif missing_value == 'category':
                if display_region == 'cy':
                    self.assertMessagePanel(WEBFORM_MISSING_CATEGORY_MSG_CY, contents)
                else:
                    self.assertMessagePanel(WEBFORM_MISSING_CATEGORY_MSG, contents)
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

    async def form_submission_email_invalid(self, url, display_region, email_value):
        form_data = self.webform_form_data.copy()
        form_data['email'] = email_value

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST', url, data=form_data)
            self.assertLogEvent(cm, self.build_url_log_entry('web-form', display_region, 'POST',
                                                             include_sub_user_journey=False, include_page=False))
            self.assertLogEvent(cm, 'web form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if not display_region == 'ni':
                self.assertIn(self.build_translation_link('web-form', display_region, include_sub_user_journey=False,
                                                          include_page=False), contents)
            self.check_text_web_form(display_region, contents, check_error=True)
            if display_region == 'cy':
                self.assertMessagePanel(WEBFORM_MISSING_EMAIL_INVALID_MSG_CY, contents)
            else:
                self.assertMessagePanel(WEBFORM_MISSING_EMAIL_INVALID_MSG, contents)

    @unittest_run_loop
    async def test_form_submission_success(self):
        await self.form_submission_success(self.get_webform_en, self.post_webform_en, 'en')
        await self.form_submission_success(self.get_webform_cy, self.post_webform_cy, 'cy')
        await self.form_submission_success(self.get_webform_ni, self.post_webform_ni, 'ni')

    @unittest_run_loop
    async def test_form_submission_error(self):
        await self.form_submission_error(self.post_webform_en, 'en', 400)
        await self.form_submission_error(self.post_webform_cy, 'cy', 400)
        await self.form_submission_error(self.post_webform_ni, 'ni', 400)

    @unittest_run_loop
    async def test_form_submission_error_429(self):
        await self.form_submission_error_429(self.post_webform_en, 'en')
        await self.form_submission_error_429(self.post_webform_cy, 'cy')
        await self.form_submission_error_429(self.post_webform_ni, 'ni')

    @unittest_run_loop
    async def test_form_submission_incomplete(self):
        await self.form_submission_incomplete(self.post_webform_en, 'en', 'country')
        await self.form_submission_incomplete(self.post_webform_cy, 'cy', 'country')
        await self.form_submission_incomplete(self.post_webform_ni, 'ni', 'country')
        await self.form_submission_incomplete(self.post_webform_en, 'en', 'category')
        await self.form_submission_incomplete(self.post_webform_cy, 'cy', 'category')
        await self.form_submission_incomplete(self.post_webform_ni, 'ni', 'category')
        await self.form_submission_incomplete(self.post_webform_en, 'en', 'description')
        await self.form_submission_incomplete(self.post_webform_cy, 'cy', 'description')
        await self.form_submission_incomplete(self.post_webform_ni, 'ni', 'description')
        await self.form_submission_incomplete(self.post_webform_en, 'en', 'name')
        await self.form_submission_incomplete(self.post_webform_cy, 'cy', 'name')
        await self.form_submission_incomplete(self.post_webform_ni, 'ni', 'name')
        await self.form_submission_incomplete(self.post_webform_en, 'en', 'email')
        await self.form_submission_incomplete(self.post_webform_cy, 'cy', 'email')
        await self.form_submission_incomplete(self.post_webform_ni, 'ni', 'email')

    @unittest_run_loop
    async def test_form_submission_email_invalid(self):
        await self.form_submission_email_invalid(self.post_webform_en, 'en', 'cheese scone')
        await self.form_submission_email_invalid(self.post_webform_cy, 'cy', 'cheese scone')
        await self.form_submission_email_invalid(self.post_webform_ni, 'ni', 'cheese scone')
        await self.form_submission_email_invalid(self.post_webform_en, 'en', 'cheese@scone')
        await self.form_submission_email_invalid(self.post_webform_cy, 'cy', 'cheese@scone')
        await self.form_submission_email_invalid(self.post_webform_ni, 'ni', 'cheese@scone')
