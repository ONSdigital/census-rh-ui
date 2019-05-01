import datetime
import logging
import time
# import hashlib
# import base64
from collections import namedtuple
from uuid import uuid4

import iso8601
from aiohttp import ClientError
from aiohttp.web import Application
from structlog import wrap_logger

from .exceptions import ExerciseClosedError, InvalidEqPayLoad


logger = wrap_logger(logging.getLogger(__name__))

Request = namedtuple("Request", ["method", "path", "auth", "func"])


def handle_response(response):
    try:
        response.raise_for_status()
    except ClientError as ex:
        logger.error("Error in response", url=str(response.url), status_code=response.status)
        raise ex
    else:
        logger.debug("Successfully connected to service", url=str(response.url))


def parse_date(string_date):
    """
    Parses a date string from ISO 8601 format to be converted elsewhere.
    :param string_date: a date string in ISO 8601 format
    :return: datetime object
    """
    try:
        return iso8601.parse_date(string_date)
    except (ValueError, iso8601.iso8601.ParseError):
        raise InvalidEqPayLoad(f"Unable to parse {string_date}")


def format_date(datetime_object):
    """
    Formats the date from a datetime object to %Y-%m-%d eg 2018-01-20
    :param datetime_object: datetime object
    :return formatted date
    """
    try:
        return datetime_object.strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        raise InvalidEqPayLoad(f"Unable to format {datetime_object}")


class EqPayloadConstructor(object):

    def __init__(self, case: dict, attributes: dict, app: Application, iac: str):
        """
        Creates the payload needed to communicate with EQ, built from the RH service
        """

        self._app = app

        self._tx_id = str(uuid4())
        self._account_service_url = f'{app["ACCOUNT_SERVICE_URL"]}{app["URL_PATH_PREFIX"]}'

        if not iac:
            raise InvalidEqPayLoad("IAC is empty")

        self._iac = iac

        if not attributes:
            raise InvalidEqPayLoad("Attributes is empty")

        self._sample_attributes = attributes

        try:
            self._case_id = case["caseId"]
        except KeyError:
            raise InvalidEqPayLoad("No case id in supplied case JSON")

        try:
            self._case_type = case["caseType"]
        except KeyError:
            raise InvalidEqPayLoad("No case type in supplied case JSON")

        try:
            self._collex_id = case["collectionExerciseId"]
        except KeyError:
            raise InvalidEqPayLoad("No collection id in supplied case JSON")

        try:
            self._response_id = case["questionnaireId"]
        except KeyError:
            raise InvalidEqPayLoad("No questionnaireId in supplied case JSON")

        try:
            self._uprn = case["address"]["uprn"]
        except KeyError:
            raise InvalidEqPayLoad(f"Could not retrieve address uprn from case JSON ")

    async def build(self):
        """__init__ is not a coroutine function, so I/O needs to go here"""

        logger.debug("Creating payload for JWT", case_id=self._case_id, tx_id=self._tx_id)

        self._language_code = 'en'  # hardcoded for 19.9 until we know how to derive

        self._payload = {
            "jti": str(uuid4()),  # required by eQ for creating a new claim
            "tx_id": self._tx_id,  # not required by eQ (will generate if does not exist)
            "iat": int(time.time()),
            "exp": int(time.time() + (5 * 60)),  # required by eQ for creating a new claim
            "case_type": self._case_type,
            "collection_exercise_sid": self._collex_id,  # required by eQ
            "region_code": "GB-ENG",  # hardcoded for sprint 19.9
            "ru_ref": self._uprn,  # new payload reuires uprn to be ru_ref
            "case_id": self._case_id,  # not required by eQ but useful for downstream
            "language_code": self._language_code,  # set as 'en' for 19.9 until we know how to set
            "display_address": self.build_display_address(self._sample_attributes),
            "response_id": self._response_id,
            "account_service_url": self._account_service_url,  # required for save/continue
            "channel": "rh",  # from claims sent from RH channel will always by rh,
            "user_id": "1234567890",  # for 19.9 will be hardcoded. This will be set to empty when eq reasdy to accept as empty
            "eq_id": "census",  # for 19.9 hardcoded as will not be needed for new payload but still needed for original
            "period_id": "1",  # for 19.9 hardcoded as will not be needed for new payload but still needed for original
            "form_type": "household"  # for 19.9 hardcoded as will not be needed for new payload but still needed for original

        }

        return self._payload

    @staticmethod
    def caps_to_snake(s):
        return s.lower().lstrip('_')

    @staticmethod
    def build_display_address(sample_attributes):
        """
        Build `display_address` value by appending not-None (in order) values of sample attributes

        :param sample_attributes: dictionary of address attributes
        :return: string of a single address attribute or a combination of two
        """
        display_address = ''
        for key in ['address_line1', 'address_line2', 'address_line3', 'town_name', 'postcode']:  # retain order of address attributes
            val = sample_attributes.get(key)
            if val:
                prev_display = display_address
                display_address = f'{prev_display}, {val}' if prev_display else val
                if prev_display:
                    break  # break once two address attributes have been added
        if not display_address:
            raise InvalidEqPayLoad("Displayable address not in sample attributes")
        return display_address

    async def _make_request(self, request: Request):
        method, url, auth, func = request
        logger.debug(f"Making {method} request to {url} and handling with {func.__name__}")
        async with self._app.http_session_pool.request(method, url, auth=auth) as resp:
            func(resp)
            return await resp.json()

    async def _get_sample_attributes_by_id(self):
        url = self._sample_url + self._sample_unit_id + "/attributes"
        return await self._make_request(Request("GET", url, self._app['SAMPLE_AUTH'], handle_response))

    async def _get_collection_instrument(self):
        url = self._ci_url + self._ci_id
        return await self._make_request(Request("GET", url, self._app['COLLECTION_INSTRUMENT_AUTH'], handle_response))

    async def _get_collection_exercise(self):
        url = self._collex_url + self._collex_id
        return await self._make_request(Request("GET", url, self._app['COLLECTION_EXERCISE_AUTH'], handle_response))

    async def _get_collection_exercise_events(self):
        url = self._collex_url + self._collex_id + "/events"
        return await self._make_request(Request("GET", url, self._app['COLLECTION_EXERCISE_AUTH'], handle_response))

    def _get_collex_event_dates(self):
        return {
            "exercise_end": self._find_event_date_by_tag("exercise_end", True, cmp_func=self._check_ce_has_ended),
            "ref_p_start_date": self._find_event_date_by_tag("ref_period_start", False),
            "ref_p_end_date": self._find_event_date_by_tag("ref_period_end", False),
            "return_by": self._find_event_date_by_tag("return_by", False),
        }

    def _check_ce_has_ended(self, datetime_object):
        try:
            if datetime.datetime.now(tz=datetime_object.tzinfo) > datetime_object:
                raise ExerciseClosedError(collection_exercise_id=self._collex_id)
        except (AttributeError, ValueError):
            raise InvalidEqPayLoad("Unable to compare date objects")

    def _find_event_date_by_tag(self, search_param: str, mandatory: bool, cmp_func=None):
        for event in self._collex_events:
            if event["tag"] == search_param and event.get("timestamp"):
                parsed_datetime = parse_date(event["timestamp"])
                if callable(cmp_func):
                    cmp_func(parsed_datetime)
                return format_date(parsed_datetime)

        if mandatory:
            raise InvalidEqPayLoad(
                f"Mandatory event not found for collection {self._collex_id} for search param {search_param}"
            )
