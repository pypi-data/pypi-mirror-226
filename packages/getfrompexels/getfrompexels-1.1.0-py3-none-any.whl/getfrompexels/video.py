"""Module containing the PexelsVideo class that holds information about a video stored on Pexels."""

# Imports
from .user import PexelsUser
from .video_file import PexelsVideoFile
from .video_picture import PexelsVideoPicture
from .type_hints import RawVideoContent, Dimensions


# Video class
class PexelsVideo:
    """The class that contains information about a video on Pexels. PexelsVideo objects contain properties that are
    meant to be used, specifically to avoid modifying attributes which are not meant to be modified.

    :param json_content: The JSON response (represented as a dictionary) that the constructor will use to initialise
    attributes
    :type json_content: dict
    """

    def __init__(self, json_content: RawVideoContent):
        """Class constructor.
        """

        # Initialization of all read-only attributes
        self._pexels_id = json_content["id"]
        self._size = (json_content["width"], json_content["height"])
        self._pexels_url = json_content["url"]
        self._screenshot_url = json_content["image"]
        self._duration = json_content["duration"]
        self._owner = PexelsUser(
            json_content["user"]["name"],
            json_content["user"]["url"],
            json_content["user"]["id"]
        )

        # Initialization continued; creation of lists with child classes
        video_files = json_content["video_files"]
        video_pictures = json_content["video_pictures"]
        self._video_files = [PexelsVideoFile(x) for x in video_files]
        self._video_pictures = [PexelsVideoPicture(x["id"], x["picture"]) for x in video_pictures]
        self._content_type = "video"

    # Properties
    @property
    def pexels_id(self) -> int:
        """The ID of the video."""
        return self._pexels_id

    @property
    def size(self) -> Dimensions:
        """A list containing the width and height of the video in pixels."""
        return self._size

    @property
    def pexels_url(self) -> str:
        """The URL to the video on Pexels."""
        return self._pexels_url

    @property
    def screenshot_url(self) -> str:
        """The URL to the video on Pexels."""
        return self._screenshot_url

    @property
    def duration(self) -> int:
        """Duration of the video in seconds."""
        return self._duration

    @property
    def owner(self) -> PexelsUser:
        """PexelsUser object that contains information about the video owner."""
        return self._owner

    @property
    def video_files(self) -> list[PexelsVideoFile]:
        """A list of video files as PexelsVideoFile objects of the video."""
        return self._video_files

    @property
    def video_pictures(self) -> list[PexelsVideoPicture]:
        """A list of preview pictures as PexelsVideoPicture objects of the video."""
        return self._video_pictures

    @property
    def content_type(self) -> str:
        """Returns the type of media the object is, which is "video" for this class."""
        return self._content_type
