"""Python module containing the PexelsPhoto class that holds information about a photo stored on Pexels."""

# Imports
from .user import PexelsUser
from .type_hints import RawPhotoContent, Dimensions
import requests


# Photo class
class PexelsPhoto:
    """Class that contains information about a photo hosted on Pexels. PexelsPhoto objects contain properties that are
    meant to be used, specifically to avoid modifying attributes which are not meant to be modified.

    :param json_content: The JSON response (represented as a dictionary) that the constructor will use to initialise
    attributes
    :type json_content: dict
    :param hide_liked: Boolean that determines whether the PexelsPhoto object has a liked_by_user property, as it
    may not be accurate depending on the PexelsSession method that returned the PexelsPhoto, setting the attribute (and
    property) to None, defaults to False
    :type hide_liked: bool
    """

    def __init__(self, json_content: RawPhotoContent, hide_liked: bool = False):
        """Class constructor.
        """

        # Initialization of read-only attributes
        self._pexels_id = json_content["id"]
        self._size = (json_content["width"], json_content["height"])
        self._pexels_url = json_content["url"]
        self._average_color = json_content["avg_color"]
        self._photographer = PexelsUser(
            json_content["photographer"],
            json_content["photographer_url"],
            json_content["photographer_id"]
        )
        self._links = {
            "original": json_content["src"]["original"],
            "large": json_content["src"]["large"],
            "large2x": json_content["src"]["large2x"],
            "medium": json_content["src"]["medium"],
            "small": json_content["src"]["small"],
            "portrait": json_content["src"]["portrait"],
            "landscape": json_content["src"]["landscape"],
            "tiny": json_content["src"]["tiny"]
        }
        self._liked_by_user = json_content["liked"] if not hide_liked else None
        self._alt_text = json_content["alt"]
        self._content_type = "photo"

    # Methods
    def download(self, path: str, size: str = "original"):
        """Downloads a JPG file of the image to a given path, allowing the user to pick a specific photo size if they
        wish.

        :param path: The path to the file that the photo will be saved as. Must include the filename, but not the file
        extension
        :type path: str
        :param size: The size of the photo, which must be a key from the "links" property, defaults to "original"
        :type size: str
        """

        image_content = requests.get(self.links[size])
        with open(f"{path}.jpg", "wb") as file:
            file.write(image_content.content)

    # Properties
    @property
    def pexels_id(self) -> int:
        """The ID of the photo."""
        return self._pexels_id

    @property
    def size(self) -> Dimensions:
        """A list containing the width and height of the photo in pixels."""
        return self._size

    @property
    def pexels_url(self) -> str:
        """The URL to the photo on Pexels."""
        return self._pexels_url

    @property
    def average_color(self) -> str:
        """The hex code of the average color of the photo."""
        return self._average_color

    @property
    def photographer(self) -> PexelsUser:
        """PexelsUser object that contains information about the photographer."""
        return self._photographer

    @property
    def links(self) -> dict[str, str]:
        """A dictionary containing direct links to the image in varying sizes."""
        return self._links

    @property
    def liked_by_user(self) -> bool | None:
        """A boolean variable that states whether the photo is liked by the user whose API is being used for the
        Session object. If the photo was returned from find_collection_contents() it is None as it doesn't appear
        to be returned properly when that method is called."""
        return self._liked_by_user

    @property
    def alt_text(self) -> str:
        """Alt text for the image."""
        return self._alt_text


    @property
    def content_type(self) -> str:
        """Returns the type of media the object is, which is "photo" for this class."""
        return self._content_type
