import logging
import time
from collections import namedtuple
from uuid import uuid4
from aiohttp.web import Application
from structlog import wrap_logger

from .exceptions import InvalidEqPayLoad

logger = wrap_logger(logging.getLogger(__name__))

Request = namedtuple("Request", ["method", "path", "auth", "func"])


class EqPayloadConstructor(object):

    def __init__(self, case: dict, attributes: dict, app: Application, adlocation: str):
        """
        Creates the payload needed to communicate with EQ, built from the RH service
        """

        self._app = app

        self._tx_id = str(uuid4())

        if not attributes:
            raise InvalidEqPayLoad("Attributes is empty")

        self._sample_attributes = attributes

        # if not self._sample_attributes['display_region']:
        #
        #     self._account_service_url = \
        #         f'{app["ACCOUNT_SERVICE_URL"]}{app["URL_PATH_PREFIX"]}{self._app.router["SaveAndExitEN:get"].url_for}'
        #
        # else:
        #
        #     if self._sample_attributes['display_region'] == 'ni':
        #         self._account_service_url = \
        #             f'{app["ACCOUNT_SERVICE_URL"]}{app["URL_PATH_PREFIX"]}{self._app.router["SaveAndExitNI:get"].url_for}'
        #     elif self._sample_attributes['display_region'] == 'cy':
        #         self._account_service_url = \
        #             f'{app["ACCOUNT_SERVICE_URL"]}{app["URL_PATH_PREFIX"]}{self._app.router["SaveAndExitCY:get"].url_for}'
        #     else:
        #         self._account_service_url = \
        #             f'{app["ACCOUNT_SERVICE_URL"]}{app["URL_PATH_PREFIX"]}{self._app.router["SaveAndExitEN:get"].url_for}'

        if adlocation:
            self._channel = 'ad'
            self._user_id = adlocation
        else:
            self._channel = 'rh'
            self._user_id = ''

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
            self._questionnaire_id = case["questionnaireId"]
        except KeyError:
            raise InvalidEqPayLoad("No questionnaireId in supplied case JSON")

        try:
            self._uprn = case["address"]["uprn"]
        except KeyError:
            raise InvalidEqPayLoad(f"Could not retrieve address uprn from case JSON ")

        try:
            self._region = case["region"]
        except KeyError:
            raise InvalidEqPayLoad(f"Could not retrieve region from case JSON ")

    async def build(self):
        """__init__ is not a coroutine function, so I/O needs to go here"""

        logger.debug("Creating payload for JWT", case_id=self._case_id, tx_id=self._tx_id)

        self._language_code = self._sample_attributes['language']

        self._payload = {
            "jti": str(uuid4()),  # required by eQ for creating a new claim
            "tx_id": self._tx_id,  # not required by eQ (will generate if does not exist)
            "iat": int(time.time()),
            "exp": int(time.time() + (5 * 60)),  # required by eQ for creating a new claim
            "case_type": self._case_type,
            "collection_exercise_sid": self._collex_id,  # required by eQ
            "region_code": self.convert_region_code(self._region),
            "ru_ref": self._uprn,  # new payload requires uprn to be ru_ref
            "case_id": self._case_id,  # not required by eQ but useful for downstream
            "language_code": self._language_code,
            "display_address": self.build_display_address(self._sample_attributes),
            "response_id": self._response_id,
            "account_service_url": self._account_service_url,  # required for save/continue
            "channel": self._channel,
            "user_id": self._user_id,
            "questionnaire_id": self._questionnaire_id,
            "eq_id": "census",  # for 19.9 hardcoded as will not be needed for new payload but still needed for original
            "period_id": "1",  # for 19.9 hardcoded as will not be needed for new payload but still needed for original
            "form_type": "individual_gb_eng",  # for 19.9 hardcoded as will not be needed for new payload but still needed for original
            "survey": "CENSUS"  # hardcoded for census
        }

        return self._payload

    @staticmethod
    def build_display_address(sample_attributes):
        """
        Build `display_address` value by appending not-None (in order) values of sample attributes

        :param sample_attributes: dictionary of address attributes
        :return: string of a single address attribute or a combination of two
        """
        display_address = ''
        for key in ['addressLine1', 'addressLine2', 'addressLine3', 'townName', 'postcode']:  # retain order of address attributes
            val = sample_attributes.get(key)
            if val:
                prev_display = display_address
                display_address = f'{prev_display}, {val}' if prev_display else val
                if prev_display:
                    break  # break once two address attributes have been added
        if not display_address:
            raise InvalidEqPayLoad("Displayable address not in sample attributes")
        return display_address

    @staticmethod
    def convert_region_code(case_region):
        region_value = ''
        if case_region == 'N':
            region_value = 'GB-NIR'
        elif case_region == 'W':
            region_value = 'GB-WLS'
        else:
            region_value = 'GB-ENG'
        return region_value
