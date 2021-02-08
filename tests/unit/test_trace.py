from app.trace import get_trace
from .helpers import TestHelpers
from aiohttp.test_utils import unittest_run_loop
from uuid import UUID


def test_get_trace():
    header = {"X-Cloud-Trace-Context": "0123456789/0123456789012345678901;o=1"}
    trace = get_trace(header)
    assert trace == "0123456789"


def test_get_trace_no_xcloud_header():
    header = {}
    trace = get_trace(header)
    assert trace is None


def test_get_trace_malformed_xcloud_header():
    header = {"X-Cloud-Trace-Context": "not a real trace context"}
    trace = get_trace(header)
    assert trace is None


class TestTraceHandling(TestHelpers):

    def clear_session(self):
        """
        Ensure session cleared from previous requests
        """
        jar = self.client._session.cookie_jar
        jar.clear()

    def validate_uuid4(self, uuid_string):
        """
        Validate that a UUID string is in fact a valid uuid4
        """
        try:
            UUID(uuid_string, version=4)
            return True
        except ValueError:
            # If it's a value error, then the string
            # is not a valid hex code for a UUID.
            return False

    @unittest_run_loop
    async def test_client_id_in_session(self):
        self.clear_session()
        cookie = {'RH_SESSION': '{ "session": {"client_id": "36be6b97-b4de-4718-8a74-8b27fb03ca8c"}}'}
        header = {"X-Cloud-Trace-Context": "0123456789/0123456789012345678901;o=1"}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            await self.client.request('GET', '/en/start/',
                                      allow_redirects=False, cookies=cookie, headers=header)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'",
                                client_id='36be6b97-b4de-4718-8a74-8b27fb03ca8c',
                                trace='0123456789')

    @unittest_run_loop
    async def test_client_id_not_in_session(self):
        self.clear_session()
        header = {"X-Cloud-Trace-Context": "0123456789/0123456789012345678901;o=1"}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            await self.client.request('GET', '/en/start/',
                                      allow_redirects=False, headers=header)
            log_record = self.assertLogEvent(cm, "received GET on endpoint 'en/start'", trace='0123456789')
            self.assertTrue(self.validate_uuid4(log_record.__dict__['client_id']))
