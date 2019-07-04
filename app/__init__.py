VERSION = '0.0.1'


BAD_CODE_MSG = {'text': 'Enter your access code.', "clickable": True, "level": "ERROR", "type": "BAD_CODE", "field": "uac"}  # NOQA
BAD_CODE_TYPE_MSG = {'text': 'Please re-enter your access code and try again.', "clickable": True, "level": "ERROR", "type": "NOT_HOUSEHOLD_CODE", "field": "uac"}  # NOQA
BAD_RESPONSE_MSG = {'text': 'There was an error, please enter your access code and try again.', "clickable": True, "level": "ERROR", "type": "SYSTEM_RESPONSE_ERROR", "field": "uac"}  # NOQA
INVALID_CODE_MSG = {'text': 'Please re-enter your access code and try again.', "clickable": True, "level": "ERROR", "type": "INVALID_CODE", "field": "uac"}  # NOQA
NOT_AUTHORIZED_MSG = {'text': 'There was a problem connecting to this study. Please try again later.', "level": "ERROR", "type": "SYSTEM_AUTH_ERROR", "field": "uac"}  # NOQA
SESSION_TIMEOUT_MSG = {'text': 'Apologies, your session has timed out. Please re-enter your access code.', "level": "ERROR", "type": "SYSTEM_AUTH_ERROR", "field": "uac"}  # NOQA
ADDRESS_CHECK_MSG = {'text': 'Please check and confirm address.', "level": "ERROR", "type": "ADDRESS_CONFIRMATION_ERROR", "field": "address"}  # NOQA
ADDRESS_EDIT_MSG = {'text': 'Enter address to continue', "level": "ERROR", "type": "ADDRESS_EDIT_ERROR", "field": "address"}  # NOQA
WEBCHAT_MISSING_NAME_MSG = {'text': 'Enter your name', "clickable": True, "level": "ERROR", "type": "BAD_CODE", "field": "screen_name"}  # NOQA
WEBCHAT_MISSING_LANGUAGE_MSG = {'text': 'Select your language', "clickable": True, "level": "ERROR", "type": "BAD_CODE", "field": "language"}  # NOQA
WEBCHAT_MISSING_QUERY_MSG = {'text': 'What type of query do you have', "clickable": True, "level": "ERROR", "type": "BAD_CODE", "field": "query"}  # NOQA
MOBILE_ENTER_MSG = {'text': 'Enter a valid UK mobile number to continue', "level": "ERROR", "type": "MOBILE_ENTER_ERROR", "field": "mobile"}  # NOQA
