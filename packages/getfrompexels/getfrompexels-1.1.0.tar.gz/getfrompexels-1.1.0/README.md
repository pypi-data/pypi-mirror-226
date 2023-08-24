# GetFromPexels
GetFromPexels is an elegant Pexels API wrapper that is available for everyone to use with the Python programming language.

## Examples
**Finding images**<br>
```py
# Finding 3 images of cats
from getfrompexels import PexelsSession
session = PexelsSession(API_KEY)
query = session.search_for_photos("cat", per_page=3)

for photo in query.contents:
    print(photo.pexels_url)
```

**Finding videos**<br>
```py
# Searching for dogs barking
from getfrompexels import PexelsSession
session = PexelsSession(API_KEY)

# Turning to page 2
query = session.search_for_videos("dog barking", page=2, per_page=3)

for video in query.contents:
    print(video.pexels_url)
```

**Saving to files**
```py
# Downloading the first image that pops up when you search "bird"
from getfrompexels import PexelsSession
session = PexelsSession(API_KEY)

# Searching for the first result for "bird"
results = session.search_for_photos("bird", per_page=1).contents
photo = results[0]

# Downloading the photo
photo.download(PATH, "large2x")  # Several sizes accepted
```

## Documentation
All classes and functions contain docstrings using the reST format as code documentation.

## Additional Information
**The library requires for the `requests` module to be installed.**<br>
If it isn't, running `pip install requests` in the terminal should install the library.<br>

The earliest Python version that can use this library is Python 3.11.<br>

To request an API key, you must make a Pexels account and get one from the official Pexels website.<br>
The official documentation for the Pexels APi is https://www.pexels.com/api/documentation/, which contains information about endpoints
and their results. GetFromPexels' main purpose is to provide anyone access to all the endpoints and provide an easy wrapper.
