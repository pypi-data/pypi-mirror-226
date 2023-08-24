"""Module containing custom exceptions that are raised in the case of an error."""


# Exceptions
class PexelsAuthorizationError(Exception):
    """Error that is raised when an API key is not given or is invalid but a request is called."""
    pass


class PexelsSearchError(Exception):
    """Error that is raised when a "search" function encounters an error."""
    pass


class PexelsLookupError(Exception):
    """Error that is raised when a "find" function encounters an error."""
    pass


class PexelsAPIRequestError(Exception):
    """More in-detail error that is raised when an HTTP response has an invalid status code after a request goes
    through the verify_response function."""
    pass


class PexelsLimitError(Exception):
    """Error that is raised when a method will demand to make more requests than a session object has left."""
    pass
