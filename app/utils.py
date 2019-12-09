import string
import re

OBSCURE_WHITESPACE = (
    '\u180E'  # Mongolian vowel separator
    '\u200B'  # zero width space
    '\u200C'  # zero width non-joiner
    '\u200D'  # zero width joiner
    '\u2060'  # word joiner
    '\uFEFF'  # zero width non-breaking space
)

uk_prefix = '44'


class InvalidDataError(Exception):

    def __init__(self, message=None):
        super().__init__(message or 'The supplied value is invalid')


class InvalidDataErrorWelsh(Exception):

    def __init__(self, message=None):
        super().__init__(message or 'WELSH The supplied value is invalid')


class ProcessPostcode:

    postcode_validation_pattern = re.compile(
        r'^((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|BX|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}))|BFPO[ ]?\d{1,4}$'  # NOQA
    )

    @staticmethod
    def validate_postcode(postcode, locale):

        for character in string.whitespace + OBSCURE_WHITESPACE:
            postcode = postcode.replace(character, '')

        postcode = postcode.upper()

        if not postcode.isalnum():
            if locale == 'cy':
                raise InvalidDataErrorWelsh('WELSH The postcode must not contain symbols')
            else:
                raise InvalidDataError('The postcode must not contain symbols')

        if len(postcode) < 5:
            if locale == 'cy':
                raise InvalidDataErrorWelsh('WELSH The postcode does not contain enough characters')
            else:
                raise InvalidDataError('The postcode does not contain enough characters')

        if len(postcode) > 7:
            if locale == 'cy':
                raise InvalidDataErrorWelsh('WELSH The postcode contain too many characters')
            else:
                raise InvalidDataError('The postcode contain too many characters')

        if not ProcessPostcode.postcode_validation_pattern.fullmatch(postcode):
            if locale == 'cy':
                raise InvalidDataErrorWelsh('WELSH The postcode is not a valid UK postcode')
            else:
                raise InvalidDataError('The postcode is not a valid UK postcode')

        return postcode


class ProcessMobileNumber:

    @staticmethod
    def normalise_phone_number(number, locale):

        for character in string.whitespace + OBSCURE_WHITESPACE + '()-+':
            number = number.replace(character, '')

        try:
            list(map(int, number))
        except ValueError:
            if locale == 'cy':
                raise InvalidDataErrorWelsh('WELSH The mobile phone number must not contain letters or symbols')
            else:
                raise InvalidDataError('The mobile phone number must not contain letters or symbols')

        return number.lstrip('0')

    @staticmethod
    def validate_uk_mobile_phone_number(number, locale):

        number = ProcessMobileNumber.normalise_phone_number(number, locale).lstrip(uk_prefix).lstrip('0')

        if not number.startswith('7'):
            if locale == 'cy':
                raise InvalidDataErrorWelsh('WELSH The mobile phone number is not a UK mobile number')
            else:
                raise InvalidDataError('The mobile phone number is not a UK mobile number')

        if len(number) > 10:
            if locale == 'cy':
                raise InvalidDataErrorWelsh('WELSH The mobile phone number contains too many digits')
            else:
                raise InvalidDataError('The mobile phone number contains too many digits')

        if len(number) < 10:
            if locale == 'cy':
                raise InvalidDataErrorWelsh('WELSH The mobile phone number does not contain enough digits')
            else:
                raise InvalidDataError('The mobile phone number does not contain enough digits')

        return '{}{}'.format(uk_prefix, number)


class FlashMessage:

    @staticmethod
    def generate_flash_message(text, level, message_type, field):
        json_return = {'text': text, 'level': level, 'type': message_type, 'field': field}
        return json_return
