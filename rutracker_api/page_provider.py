from .enums import Url
from .exceptions import (
    AuthorizationException,
    NotAuthorizedException,
    RedirectException,
)
import json


class PageProvider:
    def __init__(self, session):
        self.session = session
        self.authorized = False
        self.cookie = None

    def login(self, username, password):
        body = {"login_username": username, "login_password": password, "login": "Вход"}
        response = self.session.post(
            Url.LOGIN_URL.value,
            data=body,
            allow_redirects=False,
        )
        if response.status_code == 307:
            raise RedirectException(response.headers["Location"])
        if response.status_code != 302:
            raise AuthorizationException

        self.cookie = response.headers["set-cookie"]
        self.authorized = True

    def search(self, query, sort, order, page):
        if not self.authorized:
            raise NotAuthorizedException

        if page < 1:
            page = 1

        params = {"nm": query, "start": (page - 1) * 50}
        body = {
            "s": sort,
            "o": order,
        }
        headers = {"Cookie": self.cookie}
        response = self.session.post(
            Url.SEARCH_URL.value,
            params=params,
            data=body,
            headers=headers,
        )
        return response.content

    def torrent_file(self, topic_id):
        if not self.authorized:
            raise NotAuthorizedException

        params = {"t": topic_id}
        headers = {"Cookie": self.cookie}
        response = self.session.get(
            Url.DOWNLOAD_URL.value,
            params=params,
            headers=headers,
        )
        return response.content
