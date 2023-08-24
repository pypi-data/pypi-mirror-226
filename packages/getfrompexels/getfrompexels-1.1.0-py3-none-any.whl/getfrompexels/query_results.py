"""Module containing the PexelsQueryResults dataclass."""

# Imports
from dataclasses import dataclass
from .photo import PexelsPhoto
from .video import PexelsVideo
from .collection import PexelsCollection
from .type_hints import CollectionMediaType, PhotoSize
from typing import Optional
import os


# Type aliases
PexelsContent = list[PexelsPhoto | PexelsVideo | PexelsCollection]


# Class
@dataclass
class PexelsQueryResults:
    """Dataclass that contains the results of a query made by a PexelsSession object.

    :param _content: A list that contains PexelsPhoto, PexelsVideo, or PexelsCollection objects. Can be mixed
    :type _content: list
    :param _url: The URl of the query
    :type _url: str
    :param _total_results: The total amount of media that was returned from the query
    :type _total_results: int
    :param _page: The page number of the query
    :type _page: int
    :param _per_page: The number of content returned per page
    :type _per_page: int
    """

    _content: list
    _url: str
    _total_results: int
    _page: int
    _per_page: int

    # Methods
    def download_content(self, path: str, media_type: Optional[CollectionMediaType] = None,
                         name_prefix: Optional[str] = None, name_suffix: Optional[str] = None,
                         desired_size_for_photo: PhotoSize = "original"):
        """Downloads all content in the PexelsQueryResults object to a folder. Filtering and slight filename changes are
        possible.

        :param path: The path to the directory where each file will be downloaded to
        :type path: str
        :param media_type: The type of content from the query that is requested for download. Can be "photos" or "videos"
        :type media_type: str, optional
        :param name_prefix: If set, all content will be given a specific prefix in its filename before being followed by
        its position in the content list. Otherwise, the filename of each file will just be its ID
        :type name_prefix: str, optional
        :param name_suffix: If set, all content will be given a specific suffix in its filename, which also depends on
        file_prefix.
        :type name_suffix: str, optional
        :param desired_size_for_photo: The desired size to download of the photos in the content. Defaults to "original"
        :type desired_size_for_photo: str
        """
        for index, media in enumerate(self.content):
            match media.content_type:
                case "photo":
                    if media_type is None or media_type == "photos":
                        if (name_prefix is None) and (name_suffix is None):
                            filename = str(media.pexels_id)
                        else:
                            filename = f"{name_prefix if name_prefix is not None else ''}{index}{name_suffix if name_suffix is not None else ''}"
                        media.download(os.path.join(path, filename), desired_size_for_photo)

                case "video":
                    # TODO: create param that allows user to choose what type of video file to save in later versions
                    if media_type is None or media_type == "videos":
                        if (name_prefix is None) and (name_suffix is None):
                            filename = str(media.pexels_id)
                        else:
                            filename = f"{name_prefix if name_prefix is not None else ''}{index}{name_suffix if name_suffix is not None else ''}"
                        media.video_files[0].download(os.path.join(path, filename))

    # Properties
    @property
    def content(self) -> PexelsContent:
        """A list that contains PexelsPhoto, PexelsVideo, or PexelsCollection objects. Can be mixed."""
        return self._content

    @property
    def url(self) -> str:
        """The URL of the query."""
        return self._url

    @property
    def total_results(self) -> int:
        """The total amount of results received from the query."""
        return self._total_results

    @property
    def page(self) -> int:
        """The page number of the query."""
        return self._page

    @property
    def per_page(self) -> int:
        """The amount of content returned per page."""
        return self._per_page
