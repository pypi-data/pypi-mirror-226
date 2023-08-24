"""Module containing the PexelsCollection dataclass."""

# Imports
from dataclasses import dataclass
from .photo import PexelsPhoto
from .video import PexelsVideo
from .type_hints import CollectionMediaType, PhotoSize
from .exceptions import PexelsLimitError
from typing import Optional
from math import ceil
import os


# Type aliases
PexelsContent = list[PexelsPhoto | PexelsVideo]


# Collection class
@dataclass
class PexelsCollection:
    """The dataclass that stores information of a collection on Pexels. PexelsCollection objects contain properties that
    are meant to be used, specifically to avoid modifying attributes which are not meant to be modified.

    :param _pexels_id: The ID of the collection
    :type _pexels_id: str
    :param _title: The name of the collection
    :type _title: str
    :param _description: The description of the collection
    :type _description: str
    :param _is_private: Boolean value that shows whether the collection is marked as private or not
    :type _is_private: bool
    :param _media_count: Total amount of media in the collection
    :type _media_count: int
    :param _photos_count: Total amount of photos in the collection
    :type _photos_count: int
    :param _videos_count: Total amount of videos in the collection
    :type _videos_count: int
    """

    _pexels_id: str
    _title: str
    _description: str
    _is_private: bool
    _media_count: int
    _photos_count: int
    _videos_count: int

    # Methods
    def get_collection_content(self, pexels_session, media_type: Optional[CollectionMediaType] = None) -> PexelsContent:
        """Returns a list that contains PexelsPhoto or PexelsVideo objects (or both) which contain information about all
        media in the collection. This method uses up a request from a Pexels user.

        :param pexels_session: A PexelsSession object which will be used to return all content form the collection
        :type pexels_session: PexelsSession
        :param media_type: A filter variable which determines if only photos or videos are going to be returned. If not
        given, the filter will not apply and both media types will be included
        :type media_type: str, optional

        :raises PexelsLimitError: When the amount of requests needed to be made is greater than the amount of requests
        the user is able to make

        :return: A list containing PexelsPhoto PexelsVideo objects (or both)
        :rtype: list
        """
        if (requests_needed := ceil(self.photos_count if media_type == "photos" else self.videos_count if media_type == "videos" else self.media_count / 80)) > pexels_session.requests_left:
            raise PexelsLimitError(f"{requests_needed} requests required but only {pexels_session.requests_left} left")

        collection_content = []
        for request_number in range(requests_needed):
            query_results = pexels_session.find_collection_contents(
                collection_id=self._pexels_id,
                media_type=media_type,
                page=request_number + 1,
                per_page=80
            ).content
            for media in query_results:
                collection_content.append(media)
        return collection_content

    def download_content(self, path: str, pexels_session, media_type: Optional[CollectionMediaType] = None,
                         name_prefix: Optional[str] = None, name_suffix: Optional[str] = None,
                         desired_size_for_photo: Optional[PhotoSize] = None):
        """Downloads all content from the Pexels collection that the object contains information of. Filtering and
        slight filename changes are possible.

        :param path: The path to the directory where each file will be downloaded to
        :type path: str
        :param pexels_session: A PexelsSession object which will be used to download all content form the collection
        :type pexels_session: PexelsSession
        :param media_type: A filter variable which determines if only photos or videos are going to be saved. If not
        given, the filter will not apply and both media types will be downloaded
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
        content = self.get_collection_content(pexels_session, media_type=media_type)
        for index, media in enumerate(content):
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
    def pexels_id(self) -> str:
        """The ID of the collection."""
        return self._pexels_id

    @property
    def title(self) -> str:
        """The name of the collection."""
        return self._title

    @property
    def description(self) -> str:
        """The description of the collection."""
        return self._description

    @property
    def is_private(self) -> bool:
        """Boolean value that shows whether the collection is marked as private or not."""
        return self._is_private

    @property
    def media_count(self) -> int:
        """Total amount of media in the collection."""
        return self._media_count

    @property
    def photos_count(self) -> int:
        """Total amount of photos in the collection."""
        return self._photos_count

    @property
    def videos_count(self) -> int:
        """Total amount of videos in the collection."""
        return self._videos_count

    @property
    def content_type(self) -> str:
        """Returns "collection", useful for checking the type of content of an object the class of which is unknown."""
        return "collection"
