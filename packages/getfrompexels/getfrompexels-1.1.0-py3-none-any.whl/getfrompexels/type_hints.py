"""Module containing type hints to be imported by other modules in the package for more clear typing."""

# Imports
from typing import Literal, TypedDict

# Type aliases go below (can get imported by other modules)
QueryMethod = Literal["search", "find"]
Orientation = Literal["landscape", "portrait", "square"]
CollectionMediaType = Literal["photos", "videos"]
Size = Literal["small", "medium", "large"]
Dimensions = tuple[int, int]  # (width, height) both in px

# Photo-specific type hints
PhotoSize = Literal["original", "portrait", "landscape", "large", "large2x", "medium", "small", "tiny"]
PhotoLinks = TypedDict("PhotoLinks", {
    "original": str,
    "portrait": str,
    "landscape": str,
    "large": str,
    "large2x": str,
    "medium": str,
    "small": str,
    "tiny": str
})
RawPhotoContent = TypedDict("RawPhotoContent", {
    "id": int,
    "width": int,
    "height": int,
    "url": str,
    "avg_color": str,
    "photographer": str,
    "photographer_url": str,
    "photographer_id": int,
    "src": PhotoLinks,
    "liked": bool,
    "alt": str
})

VideoQuality = Literal["sd", "hd"]
VideoOwner = TypedDict("VideoOwner", {
    "id": int,
    "name": str,
    "url": str
})
VideoFile = TypedDict("VideoFile", {
    "id": int,
    "quality": VideoQuality,
    "file_type": str,
    "width": int,
    "height": int,
    "fps": float,
    "link": str
})
VideoPicture = TypedDict("VideoPicture", {
    "id": int,
    "picture": str,
    "nr": int
})
RawVideoContent = TypedDict("RawVideoContent", {
    "id": int,
    "width": int,
    "height": int,
    "url": str,
    "image": str,
    "duration": int,
    "user": VideoOwner,
    "video_files": list[VideoFile],
    "video_pictures": list[VideoPicture]
})
