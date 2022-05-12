class SentrywireException(Exception):
    """
    The base Sentrywire Exception that all other exception classes extend.
    """


class InvalidParameters(SentrywireException):
    """
    Parameters are invalid or missing
    """


class InvalidAuthentication(SentrywireException):
    """
    The authentication token is not valid for this system
    """


class NotFound(SentrywireException):
    """
    A 404 error
    """


class TooManyRequests(SentrywireException):
    """
    Server is likely full or busy
    """


class ServerError(SentrywireException):
    """
    A 500 error
    """


ErrorLookupTable = {
    400: InvalidParameters,
    401: InvalidAuthentication,
    403: InvalidAuthentication,
    404: NotFound,
    429: TooManyRequests,
    500: ServerError
}
