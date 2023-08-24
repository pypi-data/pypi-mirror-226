"""Module containing the PexelsUser dataclass."""

# Imports
from dataclasses import dataclass


# User class
@dataclass
class PexelsUser:
    """A dataclass containing information about a specific user. PexelsUser objects contain properties that are meant to
    be used, specifically to avoid modifying attributes which are not meant to be modified.

    :param _name: The name of the user
    :type _name: str
    :param _url: The URL of the user's profile
    :type _url: str
    :param _pexels_id: The Pexels ID of the user
    :type _pexels_id: int
    """

    _name: str
    _url: str
    _pexels_id: int

    # Properties
    @property
    def name(self) -> str:
        """The name of the user."""
        return self._name

    @property
    def url(self) -> str:
        """The URL of the user's profile."""
        return self._url

    @property
    def pexels_id(self) -> int:
        """The Pexels ID of the user."""
        return self._pexels_id

    @property
    def username(self) -> str:
        """The username of the user (with the @)."""
        return "@" + self.url.split("@")[1]
