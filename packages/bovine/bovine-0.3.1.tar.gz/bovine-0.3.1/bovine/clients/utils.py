from importlib.metadata import version
from urllib.parse import urlparse

BOVINE_CLIENT_NAME = "bovine/" + version("bovine")


def host_target_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc, parsed_url.path
