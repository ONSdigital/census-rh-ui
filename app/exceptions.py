class InactiveCaseError(Exception):
    """Raised when a user enters a used IAC code"""
    def __init__(self, case_type):
        super().__init__()
        self.case_type = case_type


class InvalidEqPayLoad(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class InvalidIACError(Exception):
    """Raised when the IAC Service returns a 404"""


class SessionTimeout(Exception):
    """Raised when users session expires in journeys requiring sessions"""
    def __init__(self, user_journey, sub_user_journey=None):
        super().__init__()
        self.user_journey = user_journey
        self.sub_user_journey = sub_user_journey


class TooManyRequests(Exception):
    """Raised when users session expires in journeys requiring sessions"""
    def __init__(self, sub_user_journey):
        super().__init__()
        self.sub_user_journey = sub_user_journey


class ExerciseClosedError(Exception):
    """Raised when a user attempts to access an already ended CE"""
    def __init__(self, collection_exercise_id):
        super().__init__()
        self.collection_exercise_id = collection_exercise_id


class InvalidDataError(Exception):
    """ Raised when user supplies invalid data in form fields (on english language page) """
    def __init__(self, message=None):
        super().__init__(message or 'The supplied value is invalid')


class InvalidDataErrorWelsh(Exception):
    """ Raised when user supplies invalid data in form fields (on welsh language page) """
    def __init__(self, message=None):
        # TODO: Add Welsh Translation
        super().__init__(message or 'WELSH The supplied value is invalid')
