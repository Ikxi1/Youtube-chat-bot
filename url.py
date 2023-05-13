import re


def get_youtube_id(url):
    # Regular expression pattern to match YouTube video ID
    pattern = r"(?:(?<=v=)|(?<=video\/)|(?<=\/live\/)|(?<=live_chat\?v=))([\w-]+)"

    # Search for the pattern in the URL
    match = re.search(pattern, url)

    # Check whether a match was found
    if match is not None:
        stream_id = match.group(0)

        if len(stream_id) == 11:
            valid = True
        else:
            valid = False

        # If a match is found and the video ID is valid, return the video ID
        if valid:
            return True, stream_id

    # If no match was found, return False and an empty string
    return False, ''
