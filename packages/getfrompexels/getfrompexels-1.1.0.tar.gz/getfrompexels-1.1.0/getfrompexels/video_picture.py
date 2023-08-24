"""Module containing the PexelsVideoPicture dataclass."""

# Imports
from dataclasses import dataclass


# Class
@dataclass
class PexelsVideoPicture:
    """The dataclass that contains information about a preview picture of a Pexels video. PexelsVideoPicture objects
    contain properties that are meant to be used, specifically to avoid modifying attributes which are not meant to be
    modified.

    :param _pexels_id: The ID of the preview picture
    :type _pexels_id: int
    :param _picture_url: The URL of the preview picture
    :type _picture_url: str
    """

    _pexels_id: int
    _picture_url: str

    # Properties
    @property
    def pexels_id(self) -> int:
        """The ID of the preview picture."""
        return self._pexels_id

    @property
    def picture_url(self) -> str:
        """The URL of the preview picture."""
        return self._picture_url
