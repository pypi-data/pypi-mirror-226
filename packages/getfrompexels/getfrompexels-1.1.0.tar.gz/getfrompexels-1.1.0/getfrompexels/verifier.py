"""Module containing a function to verify a response object, separated from other modules."""

# Getting exceptions
from .exceptions import PexelsAuthorizationError, PexelsLookupError, PexelsAPIRequestError
from .type_hints import QueryMethod
from typing import Optional
import requests


# Response verifier (called by PexelsSession before it returns anything)
def verify_response(response: requests.Response, origin_function_type: Optional[QueryMethod]):
    """Runs through a response to see if it has returned a valid status code, raising an exception if it didn't.

    :param response: The requests.Response object that is to be run through
    :type response: requests.Response
    :param origin_function_type: The type of the method that called this function
    :type origin_function_type: str, optional

    :raises PexelsAuthorizationError: On HTTP Error 401 if the request returns an Unauthorized error, meaning there is
    no given API key
    :raises PexelsLookupError: If no valid media is found after a "find" function calls this method
    :raises PexelsAPIRequestError: If any other HTTP error is given due to a non-200 status code
    """
    status_code = response.status_code

    # Making sure the response is valid first
    if status_code == 200:
        return

    # Generating message for every request
    message = f"response returned HTTP {status_code} status code"
    match status_code:
        case 401:
            raise PexelsAuthorizationError("a valid API key must be provided for function call")

        case 403:
            message = "response returned HTTP 403 \"Forbidden\" status code"

        case 404:
            if origin_function_type == "find":
                raise PexelsLookupError("no media found; invalid ID")
            message = "response returned HTTP 404 \"Not Found\" status code"

        case 429:
            message = "response returned HTTP 429 \"Too Many Requests\" status code, please wait longer"

    # Accounting for possible server errors
    if 500 <= response.status_code <= 599:
        raise PexelsAPIRequestError(f"response returned HTTP {status_code}, this is a server error")
    raise PexelsAPIRequestError(message)
