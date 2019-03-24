from requests import Request
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth

from poetry.utils._compat import urlparse


class Auth(AuthBase):
    def __init__(self, url, username, password):  # type: (str, str, str) -> None
        self._netloc = urlparse.urlparse(url).netloc
        self._auth = HTTPBasicAuth(username, password)

    def __call__(self, r):  # type: (Request) -> Request
        if urlparse.urlparse(r.url).netloc != self._netloc:
            return r

        self._auth(r)

        return r
