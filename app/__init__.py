VERSION = '0.0.1'


BAD_CODE_MSG = {'text': 'Please enter your access code.', "clickable": True, "level": "ERROR", "type": "BAD_CODE"}  # NOQA
BAD_CODE_TYPE_MSG = {'text': 'Please re-enter your access code and try again.', "clickable": True, "level": "ERROR", "type": "NOT_HOUSEHOLD_CODE"}  # NOQA
BAD_RESPONSE_MSG = {'text': 'There was an error, please enter your access code and try again.', "clickable": True, "level": "ERROR", "type": "SYSTEM_RESPONSE_ERROR"}  # NOQA
INVALID_CODE_MSG = {'text': 'Please re-enter your access code and try again.', "clickable": True, "level": "ERROR", "type": "INVALID_CODE"}  # NOQA
NOT_AUTHORIZED_MSG = {'text': 'There was a problem connecting to this study. Please try again later.', "level": "ERROR", "type": "SYSTEM_AUTH_ERROR"}  # NOQA
SESSION_TIMEOUT_MSG = {'text': 'Apologies, your session has timed out. Please re-enter your access code.', "level": "ERROR", "type": "SYSTEM_AUTH_ERROR"}
ADDRESS_CHECK_MSG = {'text': 'Please check and confirm address.', "level": "ERROR", "type": "ADDRESS_CONFIRMATION_ERROR"}
ADDRESS_EDIT_MSG = {'text': 'Enter address to continue', "level": "ERROR", "type": "ADDRESS_EDIT_ERROR"}
