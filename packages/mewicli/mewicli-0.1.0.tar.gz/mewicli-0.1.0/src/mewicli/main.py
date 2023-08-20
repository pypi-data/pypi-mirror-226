# src/mewicli/main.py

from __future__ import annotations  # for Python 3.7-3.9

from collections.abc import Callable

import requests

# https://www.mediawiki.org/wiki/API:Edit
# POST requests containing large amounts of text content (8000+ characters)
# should be sent with Content-Type: multipart/form-data
# https://gist.github.com/kazqvaizer/4cebebe5db654a414132809f9f88067b


def multipartify(
    data,
    parent_key=None,
    formatter: Callable | None = None,
) -> dict:
    if formatter is None:
        formatter = lambda v: (None, v)  # noqa E731

    if not isinstance(data, dict):
        return {parent_key: formatter(data)}

    converted: list = []

    for key, value in data.items():
        current_key = key if parent_key is None else f"{parent_key}[{key}]"
        if isinstance(value, dict):
            converted.extend(
                multipartify(value, current_key, formatter).items()
            )
        elif isinstance(value, list):
            for ind, list_value in enumerate(value):
                iter_key = f"{current_key}[{ind}]"
                converted.extend(
                    multipartify(list_value, iter_key, formatter).items()
                )
        else:
            converted.append((current_key, formatter(value)))

    return dict(converted)


class LoginError(RuntimeError):
    def __init__(self, arg):
        self.args = arg


class MediaWiki:
    def __init__(self, url: str) -> None:
        self.url = url

    def login(
        self,
        username: str,
        password: str,
    ) -> None:
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login_response = "fail to login"
        self._get_login_token()
        self._get_login_result()
        if self.login_response == "Success":
            self._get_csrf_token()
        else:
            self.session.close()
            raise LoginError(self.login_response)

    def logout(self) -> None:
        params = {
            "action": "edit",
            "token": self.csrf_token,
            "format": "json",
        }
        response = self.session.post(url=self.url, params=params)
        self.logout_response = response.json()
        self.session.close()

    def _get_login_token(self) -> None:
        params_token = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json",
        }
        response = self.session.get(url=self.url, params=params_token)
        data = response.json()
        self.login_token = data["query"]["tokens"]["logintoken"]

    def _get_login_result(self) -> None:
        params_login = {
            "action": "login",
            "lgname": self.username,
            "lgpassword": self.password,
            "lgtoken": self.login_token,
            "format": "json",
        }
        response = self.session.post(url=self.url, data=params_login)
        data = response.json()
        self.login_response = data.get("login", {}).get(
            "result", "fail to login"
        )

    def _get_csrf_token(self) -> None:
        params_csrf = {
            "action": "query",
            "meta": "tokens",
            "format": "json",
        }
        response = self.session.get(url=self.url, params=params_csrf)
        data = response.json()
        self.csrf_token = data["query"]["tokens"]["csrftoken"]

    def edit(self, title: str, text: str) -> None:
        page_edit = {
            "action": "edit",
            "title": title,
            "token": self.csrf_token,
            "format": "json",
            "text": text,
        }
        response = self.session.post(
            url=self.url, files=multipartify(page_edit)
        )
        self.post_response = response.json()
