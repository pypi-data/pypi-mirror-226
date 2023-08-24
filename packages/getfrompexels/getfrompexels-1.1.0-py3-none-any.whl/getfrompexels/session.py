"""Module containing the PexelsSession class with associated variables and functions outside the class."""

# Imports
from .exceptions import *
from .photo import PexelsPhoto
from .video import PexelsVideo
from .collection import PexelsCollection
from .query_results import PexelsQueryResults
from .endpoints import ENDPOINTS
from .verifier import verify_response
from .type_hints import QueryMethod, CollectionMediaType, Orientation, Size
from typing import Optional
import requests
import re


# Constants
SUPPORTED_PHOTO_COLORS = (
    "red",
    "orange",
    "yellow",
    "green",
    "turquoise",
    "blue",
    "violet",
    "pink",
    "brown",
    "black",
    "gray",
    "white"
)

SUPPORTED_LOCATIONS = (
    "en-us",
    "pt-br",
    "es-es",
    "it-it",
    "fr-fr",
    "sv-se",
    "id-id",
    "pl-pl",
    "ja-jp",
    "zh-tw",
    "zh-cn",
    "ko-kr",
    "th-th",
    "nl-nl",
    "hu-hu",
    "vi-vn",
    "cs-cz",
    "da-dk",
    "fi-fi",
    "uk-ua",
    "el-gr",
    "ro-ro",
    "nb-no",
    "sk-sk",
    "tr-tr",
    "ru-ru"
)


# Non-class functions
def ensure_lower(*values):
    """Returns a modified list of given values (*values) where all string members are in lowercase."""
    return list(map(lambda x: x.lower() if isinstance(x, str) else x, values))


def check_query_arguments(query: str, orientation: Optional[str], size: Optional[str], color: Optional[str],
                          locale: Optional[str]):
    """Checks and raises exceptions when arguments passed in a "search" function do not fit required criteria. This
    function is called inside another method. More information on the arguments can be seen in those functions.

    :param query: The search query that was passed from the function that called this method
    :rtype query: str
    :param orientation: The orientation of the photo or video that was passed from the function that called this method
    :rtype orientation: str, optional
    :param size: The size of the photo or video that was passed from the function that called this method
    :rtype size: str, optional
    :param color: The color of the photo or video that was passed from the function that called this method
    :rtype color: str, optional
    :param locale: The locale of the search
    :rtype locale: str, optional

    :raises PexelsSearchError: When a given argument does not fit its required criteria
    """
    # Type annotations above are not needed, for the if-statements below do not use their class' methods.
    orientation, size, color, locale = ensure_lower(orientation, size, color, locale)

    if not query:
        # query is a mandatory string argument that must not be empty
        raise PexelsSearchError("query parameter must be entered")

    if (orientation is not None) and (orientation not in ["landscape", "portrait", "square"]):
        # orientation can either be "landscape", "portrait", "square", or left unspecified
        raise PexelsSearchError("unsupported or invalid orientation parameter, must either not be set or "
                                "landscape, portrait or square")

    if (size is not None) and (size not in ["small", "medium", "large"]):
        # size can either be "small", "medium", "large", or left unspecified
        raise PexelsSearchError("unsupported or invalid size parameter, must either not be set or small, "
                                "medium or large")

    if (color is not None) and (color not in SUPPORTED_PHOTO_COLORS) and \
            (not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                           color)):  # Thanks to teoreda StackOverflow for hex col detection
        # color can either be part of SUPPORTED_PHOTO_COLORS, a hex code [#abcdef], or left unspecified
        raise PexelsSearchError("unsupported or invalid color parameter")

    if (locale is not None) and (locale not in SUPPORTED_LOCATIONS):
        # locale can either be part of SUPPORTED_LOCATIONS or left unspecified
        raise PexelsSearchError("unsupported or invalid locale parameter")


def get_query_parameters(**parameters):
    """Returns an incomplete part of a URL for an endpoint with parameters for making requests with specific values."""
    if parameters:
        return "?" + "&".join([f"{key}={value}" for key, value in parameters.items() if value is not None])
    return ""


# Session class
class PexelsSession:
    """The main class that is used to call methods which deal with making requests to the Pexels API. Contains request
    statistics as properties of a PexelsSession object, all of which are set to None before a first request due to the
    way the Pexels API works.

    :param key: The API key used every time a request is made. While specifying the API key is not forced (optional),
    must be specified before request methods get used, however, either by the set_key() method or with the constructor
    :type key: str, optional
    """

    def __init__(self, key: str = None):
        """Class constructor.
        """
        # Initialisation
        if not (isinstance(key, str) or key is None):
            raise TypeError("key must either be not given/None or a str object")
        self._key = key

        # The values below can only be seen after the first successful request is made. At first, they are set to None.
        self._request_limit = None
        self._requests_left = None
        self._requests_rollback_timestamp = None

    # Functions to shorten code
    def get_https_response(self, endpoint: str, origin_function_type: Optional[QueryMethod] = None) -> requests.Response:
        """Serves as the main function that makes an HTTPS request to the Pexels API. Returns a requests.Response
        object.

        :param: endpoint: HTTPS endpoint to be called, must be part of the ENDPOINTS dictionary in endpoints.py
        :type endpoint: str
        :param: origin_function_type: The type of function that calls the method to phrase errors differently
        :type origin_function_type: QueryMethod, optional

        :raises: PexelsAuthorizationError: When an API key was not provided for the PexelsSession instance

        :return: A Response object that was returned from the request made in the method call
        :rtype: requests.Response
        """
        if self._key is None:
            raise PexelsAuthorizationError("an API key must be provided for function call")

        response = requests.get(endpoint, headers={"Authorization": self._key})
        verify_response(response, origin_function_type)
        return response

    # API wrapper functions
    def find_photo(self, photo_id: int) -> PexelsPhoto:
        """Returns a PexelsPhoto object given the photo ID.

        :param: photo_id: The ID of the photo
        :type: photo_id: int

        :return: A PexelsPhoto object containing information about the photo given the ID
        :rtype: PexelsPhoto
        """
        # Making request
        targeted_endpoint = ENDPOINTS["FIND_PHOTO"]
        request_url = f"{targeted_endpoint}/{photo_id}"
        response = self.get_https_response(request_url, "find")

        # Returning data and updating rate limit values
        self.update_rate_limit_attributes(response)
        return PexelsPhoto(response.json())

    def find_video(self, video_id: int) -> PexelsVideo:
        """Returns a PexelsVideo object given the video ID.

        :param video_id: The ID of the video
        :type video_id: int

        :return: A PexelsVideo object containing information about the video given the ID
        :rtype: PexelsVideo
        """
        # Making request
        targeted_endpoint = ENDPOINTS["FIND_VIDEO"]
        request_url = f"{targeted_endpoint}/{video_id}"
        response = self.get_https_response(request_url, "find")

        # Returning data and updating rate limit values
        self.update_rate_limit_attributes(response)
        return PexelsVideo(response.json())

    # Search for curated photos/popular videos
    def search_curated_photos(self, page: int = 1, per_page: int = 15) -> PexelsQueryResults:
        """Returns a PexelsQueryResults object containing photos curated by the Pexels team.

        :param page: The results page number that is being requested, defaults to 1
        :type page: int
        :param per_page: The number of photos that is being requested for the page. Maximum is 80, defaults to 15
        :type per_page: int

        :raises PexelsSearchError: When page is less than 1 or per_page is less than 1 or over 80

        :return: A PexelsQueryResults object containing all curated photos as PexelsPhoto objects
        :rtype: PexelsQueryResults
        """
        # Checking specific argument validity
        if per_page > 80 or per_page < 1:
            raise PexelsSearchError("per_page parameter must be in between 1 and 80 inclusive")

        if page < 1:
            PexelsSearchError("page parameter must be at least 1")

        # Making request
        targeted_endpoint = ENDPOINTS["CURATED_PHOTOS"]
        request_url = targeted_endpoint + get_query_parameters(page=page, per_page=per_page)
        response = self.get_https_response(request_url)
        results = response.json()

        # Returning data and updating rate limit values
        self.update_rate_limit_attributes(response)
        return PexelsQueryResults(
            _content=[PexelsPhoto(x) for x in results["photos"]],
            _url=request_url,
            _total_results=results["total_results"],
            _page=results["page"],
            _per_page=results["per_page"]
        )

    def search_popular_videos(
            self,
            min_width: Optional[int] = None,
            min_height: Optional[int] = None,
            min_duration: Optional[int] = None,
            max_duration: Optional[int] = None,
            page: int = 1,
            per_page: int = 15
    ) -> PexelsQueryResults:
        """Returns a PexelsQueryResults object containing popular Pexels videos with optional parameters.

        :param min_width: The minimum width in pixels of the returned videos
        :type min_width: int, optional
        :param min_height: The minimum height in pixels of the returned videos
        :type min_height: int, optional
        :param min_duration: The minimum duration of the returned videos in seconds
        :type min_duration: int, optional
        :param max_duration: The maximum duration of the returned videos in seconds
        :type max_duration: int, optional
        :param page: The results page number that is being requested
        :type page: int The results page number that is being requested, defaults to 1
        :param per_page: The number of videos that is being requested for the page. Maximum is 80, defaults to 15
        :type per_page: int

        :raises PexelsSearchError: When specific criteria aren't met, like max_duration being less than min_duration,
        or negative values being present for the first 5 arguments, or per_page being less than 1 or over 80

        :return: A PexelsQueryResults object containing popular videos on the website as PexelsVideo objects
        :rtype: PexelsQueryResults
        """
        # Checking specific argument validity
        if (max_duration is not None) and (min_duration is not None):
            if isinstance(max_duration, int) and isinstance(min_duration, int):
                if max_duration < min_duration:
                    raise PexelsSearchError("max_duration cannot be less than min_duration")
            else:
                raise PexelsSearchError("duration parameters must be integers")
        if min_height is not None:
            if not isinstance(min_height, int):
                raise PexelsSearchError("min_height parameter must be integers")

        if any(map(lambda x: x <= 0 if x is not None else False, [min_width, min_height, min_duration, max_duration])):
            raise PexelsSearchError("negative and zero minimums/maximums are invalid")

        if per_page > 80 or per_page < 1:
            raise PexelsSearchError("per_page parameter must be in between 1 and 80 inclusive")

        if page < 1:
            PexelsSearchError("page parameter must be at least 1")

        # Making request
        targeted_endpoint = ENDPOINTS["POPULAR_VIDEOS"]
        request_url = targeted_endpoint + get_query_parameters(
            min_width=min_width,
            min_height=min_height,
            min_duration=min_duration,
            max_duration=max_duration,
            page=page,
            per_page=per_page
        )
        response = self.get_https_response(request_url)
        results = response.json()

        # Returning data and updating rate limit values
        self.update_rate_limit_attributes(response)
        return PexelsQueryResults(
            _content=[PexelsVideo(x) for x in results["videos"]],
            _url=request_url,
            _total_results=results["total_results"],
            _page=results["page"],
            _per_page=results["per_page"]
        )

    def search_featured_collections(self, page: int = 1, per_page: int = 15) -> PexelsQueryResults:
        """Returns a PexelsQueryResults object containing featured Pexels collections.

        :param page: The results page number that is being requested, defaults to 1
        :type page: int The results page number that is being requested
        :param per_page: The number of collections that is being requested for the page. Maximum is 80, defaults to 15
        :type per_page: int

        :return: A PexelsQueryResults object containing collections featured on Pexels as PexelsCollection objects
        :rtype: PexelsQueryResults
        """
        # Checking specific argument validity
        if per_page > 80 or per_page < 1:
            raise PexelsSearchError("per_page parameter must be in between 1 and 80 inclusive")

        if page < 1:
            raise PexelsSearchError("page parameter must be at least 1")

        # Making request
        request_url = ENDPOINTS["FEATURED_COLLECTIONS"] + get_query_parameters(
            page=page,
            per_page=per_page
        )
        response = self.get_https_response(request_url)
        results = response.json()

        # Returning data and updating rate limit values
        self.update_rate_limit_attributes(response)
        return PexelsQueryResults(
            _content=[PexelsCollection(
                _pexels_id=x["id"],
                _title=x["title"],
                _description=x["description"],
                _is_private=x["private"],
                _media_count=x["media_count"],
                _photos_count=x["photos_count"],
                _videos_count=x["videos_count"]

            ) for x in results["collections"]],
            _url=request_url,
            _total_results=results["total_results"],
            _page=results["page"],
            _per_page=results["per_page"]
        )

    # Search owned collection function
    def find_user_collections(self, page: int = 1, per_page: int = 15) -> PexelsQueryResults:
        """Returns a PexelsQueryResults object containing the collections saved by the user.

        :param page: The results page number that is being requested, defaults to 1
        :type page: int The results page number that is being requested
        :param per_page: The number of collections that is being requested for the page. Maximum is 80, defaults to 15
        :type per_page: int

        :raises PexelsSearchError: When page is less than 1 or per_page is less than 1 or over 80

        :return: A PexelsQueryResults object that contains PexelsCollection objects for each collection that the user
        (the key of which is being used) owns
        :rtype: PexelsQueryResults
        """
        # Checking specific argument validity
        if per_page > 80 or per_page < 1:
            raise PexelsSearchError("per_page parameter must be in between 1 and 80 inclusive")

        if page < 1:
            raise PexelsSearchError("page parameter must be at least 1")

        # Making request
        request_url = ENDPOINTS["USER_COLLECTIONS"] + get_query_parameters(
            page=page,
            per_page=per_page
        )
        response = self.get_https_response(request_url)
        results = response.json()

        # Returning data and updating rate limit values
        self.update_rate_limit_attributes(response)
        return PexelsQueryResults(
            _content=[PexelsCollection(
                _pexels_id=x["id"],
                _title=x["title"],
                _description=x["description"],
                _is_private=x["private"],
                _media_count=x["media_count"],
                _photos_count=x["photos_count"],
                _videos_count=x["videos_count"]

            ) for x in results["collections"]],
            _url=request_url,
            _total_results=results["total_results"],
            _page=results["page"],
            _per_page=results["per_page"]
        )

    # Search media in collection
    def find_collection_contents(
            self,
            collection_id: str,
            media_type: Optional[CollectionMediaType] = None,
            page: int = 1,
            per_page: int = 15
    ) -> PexelsQueryResults:
        """Returns a PexelsQueryResults object that contains media that is part of a given collection. The
        media type can be filtered out.

        :param collection_id: The ID of the collection the contents of which are being requested
        :type collection_id: str
        :param media_type: A filter variable which determines if only photos or videos are going to be returned. If not
        given, the filter will not apply and both media types will be included
        :type media_type: str, optional
        :param page: The results page number that is being requested, defaults to 1
        :type page: int The results page number that is being requested
        :param per_page: The number of media that is being requested for the page. Maximum is 80, defaults to 15
        :type per_page: int

        :raises PexelsSearchError: When page is less than 1 or per_page is less than 1 or over 80

        :return: A PexelsQueryResults object that contains PexelsPhoto or PexelsVideo (or both) objects which give
        information about media that are in the collection given by its ID
        :rtype: PexelsQueryResults
        """
        # Checking specific argument validity
        if media_type not in ["photos", "videos"]:
            media_type = None  # Done to remove from parameters section in request URL

        if per_page > 80 or per_page < 1:
            raise PexelsSearchError("per_page parameter must be in between 1 and 80 inclusive")

        if page < 1:
            raise PexelsSearchError("page parameter must be at least 1")

        # Making request
        request_url = f"{ENDPOINTS['COLLECTION_MEDIA']}/{collection_id}" + get_query_parameters(
            page=page,
            per_page=per_page,
            type=media_type
        )
        response = self.get_https_response(request_url, "find")  # 404 counts as PexelsLookupError in verify_response()
        results = response.json()

        # Returning data and updating rate limit values
        self.update_rate_limit_attributes(response)
        return PexelsQueryResults(
            _content=[PexelsPhoto(x, True) if x["type"] == "Photo" else PexelsVideo(x) for x in results["media"]],
            _url=request_url,
            _total_results=results["total_results"],
            _page=results["page"],
            _per_page=results["per_page"]
        )

    # Search by keyword functions
    def search_for_photos(
            self,
            query: str,
            orientation: Optional[Orientation] = None,
            size: Optional[Size] = None,
            color: Optional[str] = None,
            locale: Optional[str] = None,
            page: int = 1,
            per_page: int = 15
    ) -> PexelsQueryResults:
        """Searches for photos given a specific query and some optional parameters and returns a PexelsQueryResults
        object with the photos that are returned.

        :param query: The query that is being searched
        :type query: str
        :param orientation: The selected orientation of the photos. Can be "landscape", "portrait", or "square"
        :type orientation: str, optional
        :param size: The chosen size of the photos. Can be "large" (24MP), "medium" (12MP), or "small" (4MP)
        :type size: str, optional
        :param color: Desired color of the photo. Can either be a hex value or part of SUPPORTED_PHOTO_COLORS
        :type color: str, optional
        :param locale: The locale of the performed search. Can be any option in SUPPORTED_LOCATIONS
        :type locale: str, optional
        :param page: The results page number that is being requested, defaults to 1
        :type page: int The results page number that is being requested
        :param per_page: The number of photos that is being requested for the page. Maximum is 80, defaults to 15
        :type per_page: int

        :raises PexelsSearchError: When page is less than 1 or per_page is less than 1 or over 80

        :return: A PexelsQueryResults object containing PexelsPhoto objects containing information about the photos that
        were returned from the query
        :rtype: PexelsQueryResults
        """
        # Checking argument validity
        query = query.strip()
        check_query_arguments(query, orientation, size, color, locale)
        if per_page > 80 or per_page < 1:
            raise PexelsSearchError("per_page parameter must be in between 1 and 80 inclusive")

        if page < 1:
            raise PexelsSearchError("page parameter must be at least 1")

        if color is not None:
            color = color[1:]  # Slice done to remove the # from the hex code! (no following arguments become ignored)

        # Making request
        request_url = ENDPOINTS["SEARCH_PHOTOS"] + get_query_parameters(
            query=query,
            orientation=orientation,
            size=size,
            color=color,
            locale=locale,
            page=page,
            per_page=per_page
        )
        response = self.get_https_response(request_url)
        results = response.json()

        # Returning data and updating rate limit values
        self.update_rate_limit_attributes(response)
        return PexelsQueryResults(
            _content=[PexelsPhoto(x) for x in results["photos"]],
            _url=request_url,
            _total_results=results["total_results"],
            _page=results["page"],
            _per_page=results["per_page"]
        )

    def search_for_videos(
            self,
            query: str,
            orientation: Optional[str] = None,
            size: Optional[Size] = None,
            locale: Optional[str] = None,
            page=1,
            per_page=15
    ) -> PexelsQueryResults:
        """Searches for videos given a specific query and some optional parameters and returns a PexelsQueryResults
        object with the videos that are returned.

         :param query: The query that is being searched
         :type query: str
         :param orientation: The selected orientation of the videos. Can be "landscape", "portrait", or "square"
         :type orientation: str, optional
         :param size: The chosen size of the videos. Can be "large" (4K), "medium" (Full HD), or "small" (HD)
         :rtype size: str, optional
         :param locale: The locale of the performed search. Can be any option in SUPPORTED_LOCATIONS
         :size locale: str, optional
         :param page: The results page number that is being requested. Maximum is 80, defaults to 1
         :type page: int
         :param per_page: Amount of videos that will be returned in the page. Maximum is 80, defaults to 15
         :type per_page: int

        :raises PexelsSearchError: When the page number is lest han 1, or per_page is less than 1 or over 80

        :return: A PexelsQueryResults object containing PexelsVideo objects containing information about the videos that
        were returned from the query
        :rtype: PexelsQueryResults
        """
        # Checking argument validity
        query = query.strip()
        check_query_arguments(query, orientation, size, None, locale)  # No such parameter as color for video
        if per_page > 80 or per_page < 1:
            raise PexelsSearchError("per_page parameter must be in between 1 and 80 inclusive")

        if page < 1:
            raise PexelsSearchError("page parameter must be at least 1")

        # Making request
        request_url = ENDPOINTS["SEARCH_VIDEOS"] + get_query_parameters(
            query=query,
            orientation=orientation,
            size=size,
            locale=locale,
            page=page,
            per_page=per_page
        )
        response = self.get_https_response(request_url)
        results = response.json()

        # Returning data and updating rate limit values
        self.update_rate_limit_attributes(response)
        return PexelsQueryResults(
            _content=[PexelsVideo(x) for x in results["videos"]],
            _url=request_url,
            _total_results=results["total_results"],
            _page=results["page"],
            _per_page=results["per_page"]
        )

    # Key setting function
    def set_key(self, key: str):
        """Sets the key of the PexelsSession object or changes it if an old one is present.

        :param key: The new key that the PexelsSession instance will use when making requests with methods.
        :type key: str

        :raises TypeError: When the key argument is not a string
        """
        if not isinstance(key, str):
            raise TypeError("key is not of type str")
        self._key = key

    # Updating saved rate limit values
    def update_rate_limit_attributes(self, response: requests.Response):
        """Updates the request limit attributes given by the latest response's headers. This function gets called by
        another method.

        :param response: The response object the headers of which will contain the latest request statistics
        :type response: requests.Response
        """
        self._request_limit = response.headers["X-Ratelimit-Limit"]
        self._requests_left = response.headers["X-Ratelimit-Remaining"]
        self._requests_rollback_timestamp = response.headers["X-Ratelimit-Reset"]

    # Properties
    @property
    def key(self) -> str:
        """The API key for the PexelsSession object."""
        return self._key

    @property
    def request_limit(self) -> int:
        """The maximum amount of requests the user can make for the month."""
        return self._request_limit

    @property
    def requests_left(self) -> int:
        """The amount of requests the user can make for until the limit resets."""
        return self._requests_left

    @property
    def requests_rollback_timestamp(self) -> int:
        """The UNIX timestamp of the date when the monthly period rolls over."""
        return self._requests_rollback_timestamp
