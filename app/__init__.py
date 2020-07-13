VERSION = '0.0.1'


BAD_CODE_MSG = {'text': 'Enter your access code.', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE', 'field': 'uac'}
BAD_CODE_TYPE_MSG = {'text': 'Please re-enter your access code and try again.', 'clickable': True, 'level': 'ERROR', 'type': 'NOT_HOUSEHOLD_CODE', 'field': 'uac'}  # NOQA
BAD_RESPONSE_MSG = {'text': 'There was an error, please enter your access code and try again.', 'clickable': True, 'level': 'ERROR', 'type': 'SYSTEM_RESPONSE_ERROR', 'field': 'uac'}  # NOQA
INVALID_CODE_MSG = {'text': 'Please re-enter your access code and try again.', 'clickable': True, 'level': 'ERROR', 'type': 'INVALID_CODE', 'field': 'uac'}
NOT_AUTHORIZED_MSG = {'text': 'There was a problem connecting to this study. Please try again later.', 'level': 'ERROR', 'type': 'SYSTEM_AUTH_ERROR', 'field': 'uac'}  # NOQA
SESSION_TIMEOUT_MSG = {'text': 'Apologies, your session has timed out. Please re-enter your access code.', 'level': 'ERROR', 'type': 'SYSTEM_AUTH_ERROR', 'field': 'uac'}  # NOQA
SESSION_TIMEOUT_CODE_MSG = {'text': 'Apologies, your session has timed out. You will need to start again.', 'level': 'ERROR', 'type': 'SYSTEM_AUTH_ERROR', 'field': 'code'}  # NOQA
ADDRESS_CHECK_MSG = {'text': 'Please check and confirm address.', 'level': 'ERROR', 'type': 'ADDRESS_CONFIRMATION_ERROR', 'field': 'address'}
ADDRESS_EDIT_MSG = {'text': 'Enter address to continue', 'level': 'ERROR', 'type': 'ADDRESS_EDIT_ERROR', 'field': 'address'}
WEBCHAT_MISSING_NAME_MSG = {'text': 'Enter your name', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE', 'field': 'screen_name'}
WEBCHAT_MISSING_COUNTRY_MSG = {'text': 'Select your country', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE', 'field': 'country'}
WEBCHAT_MISSING_QUERY_MSG = {'text': 'What type of query do you have', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE', 'field': 'query'}
MOBILE_CHECK_MSG = {'text': 'Please check and confirm your mobile phone number.', 'level': 'ERROR', 'type': 'MOBILE_CONFIRMATION_ERROR', 'field': 'mobile'}
ADDRESS_SELECT_CHECK_MSG = {'text': 'Select an address', 'level': 'ERROR', 'type': 'ADDRESS_SELECT_CHECK_MSG', 'field': 'address-select'}
VALIDATION_FAILURE_MSG = {'text': 'Session timed out or permission denied', 'level': 'ERROR', 'type': 'VALIDATION_FAILURE_MSG', 'field': 'uac'}
START_LANGUAGE_OPTION_MSG = {'text': 'Select a language option', 'level': 'ERROR', 'type': 'START_LANGUAGE_OPTION_MSG', 'field': 'language-option'}
NO_SELECTION_CHECK_MSG = {'text': 'Please select an option.', 'level': 'ERROR', 'type': 'NO_SELECTION_ERROR', 'field': 'no-selection'}  # NOQA

BAD_CODE_MSG_CY = {'text': 'Rhowch eich cod mynediad.', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE', 'field': 'uac'}
BAD_CODE_TYPE_MSG_CY = {'text': 'Rhowch eich cod mynediad eto a rhowch gynnig arall arni.', 'clickable': True, 'level': 'ERROR', 'type': 'NOT_HOUSEHOLD_CODE', 'field': 'uac'}  # NOQA
BAD_RESPONSE_MSG_CY = {'text': 'Digwyddodd gwall – rhowch eich cod mynediad a rhowch gynnig arall arni.', 'clickable': True, 'level': 'ERROR', 'type': 'SYSTEM_RESPONSE_ERROR', 'field': 'uac'}  # NOQA
INVALID_CODE_MSG_CY = {'text': 'Rhowch eich cod mynediad eto a rhowch gynnig arall arni.', 'clickable': True, 'level': 'ERROR', 'type': 'INVALID_CODE', 'field': 'uac'}  # NOQA
NOT_AUTHORIZED_MSG_CY = {'text': "Roedd problem wrth gysylltu â'r astudiaeth hon. Rhowch gynnig arall arni yn nes ymlaen.", 'level': 'ERROR', 'type': 'SYSTEM_AUTH_ERROR', 'field': 'uac'}  # NOQA
SESSION_TIMEOUT_MSG_CY = {'text': "Mae'n flin gennym, ond mae eich sesiwn wedi cyrraedd y terfyn amser. Rhowch eich cod mynediad eto.", 'level': 'ERROR', 'type': 'SYSTEM_AUTH_ERROR', 'field': 'uac'}  # NOQA
SESSION_TIMEOUT_CODE_MSG_CY = {'text': "Mae'n flin gennym, ond mae eich sesiwn wedi cyrraedd y terfyn amser. Bydd angen i chi ddechrau eto.", 'level': 'ERROR', 'type': 'SYSTEM_AUTH_ERROR', 'field': 'code'}  # NOQA
ADDRESS_CHECK_MSG_CY = {'text': "Edrychwch eto ar y cyfeiriad a'i gadarnhau.", 'level': 'ERROR', 'type': 'ADDRESS_CONFIRMATION_ERROR', 'field': 'address'}
ADDRESS_EDIT_MSG_CY = {'text': 'Nodwch gyfeiriad i barhau', 'level': 'ERROR', 'type': 'ADDRESS_EDIT_ERROR', 'field': 'address'}
WEBCHAT_MISSING_NAME_MSG_CY = {'text': 'Nodwch eich enw', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE', 'field': 'screen_name'}
WEBCHAT_MISSING_COUNTRY_MSG_CY = {'text': 'Dewiswch eich gwlad', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE', 'field': 'country'}
WEBCHAT_MISSING_QUERY_MSG_CY = {'text': 'Pa fath o ymholiad sydd gennych chi?', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE', 'field': 'query'}
MOBILE_CHECK_MSG_CY = {'text': "Edrychwch eto ar eich rhif ffôn symudol a'i gadarnhau.", 'level': 'ERROR', 'type': 'MOBILE_CONFIRMATION_ERROR', 'field': 'mobile'}  # NOQA
ADDRESS_SELECT_CHECK_MSG_CY = {'text': 'Dewiswch gyfeiriad', 'level': 'ERROR', 'type': 'ADDRESS_SELECT_CHECK_MSG', 'field': 'address-select'}
VALIDATION_FAILURE_MSG_CY = {'text': "Mae'r sesiwn wedi cyrraedd y terfyn amser neu nid oes caniatâd wedi cael ei roi", 'level': 'ERROR', 'type': 'VALIDATION_FAILURE_MSG', 'field': 'uac'}  # NOQA
START_LANGUAGE_OPTION_MSG_CY = {'text': 'Dewiswch opsiwn iaith', 'level': 'ERROR', 'type': 'START_LANGUAGE_OPTION_MSG', 'field': 'language-option'}
# TODO ADD WELSH TRANSLATION
NO_SELECTION_CHECK_MSG_CY = {'text': 'Please select an option.', 'level': 'ERROR', 'type': 'NO_SELECTION_ERROR', 'field': 'no-selection'}  # NOQA
