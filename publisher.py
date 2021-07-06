import typing

import requests
from requests.auth import HTTPBasicAuth

import Notipy.constants as constants
import Notipy.exceptions as exceptions


class PublicationResponse:
    def __init__(self, passed, failed, total):
        self.passed = passed
        self.failed = failed
        self.total = total

    def passed_percent(self) -> float:
        if self.total == 0:
            return 0

        return self.passed / self.total

    def failed_percent(self) -> float:
        if self.total == 0:
            return 0

        return self.failed / self.total

    def __repr__(self):
        return "<PublicationResponse passed={} failed={} total={}>".format(self.passed, self.failed, self.total)


class Publisher:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def publish(self, message: str, categories: typing.Union[typing.List[str], str] = "*") -> PublicationResponse:
        r = requests.post(
            constants.API_BASE + "/notification", json=dict(
                message=message,
                category=categories
            ),
            auth=HTTPBasicAuth(self.client_id, self.client_secret)
        )

        if r.status_code == 200:
            resp = r.json()
            return PublicationResponse(
                resp["success"],
                resp["fail"],
                resp["total"]
            )

        if r.status_code == 404:
            raise exceptions.InvalidCredentialsException(
                "The specified client ID and secret do not match a valid publisher. Check your keys and try again. "
                "You can manage your publishers from the web interface at {}/notifi/publishers".format(
                    constants.URL_BASE
                )
            )

        else:
            raise exceptions.FailedToSendMessageException(
                "Could not send message to categories '{}'. Please try again later. HTTP: {}".format(
                    categories, r.status_code
                )
            )
