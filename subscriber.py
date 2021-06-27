import datetime
import threading
import time
import typing

import requests
from requests.auth import HTTPBasicAuth

import constants
import exceptions


class Message:
    def __init__(
            self, message_id: int, body: str, created: typing.Union[str, datetime.datetime], subscriber: 'Subscriber'
    ):
        self.id = message_id
        self.body = body
        self.subscriber = subscriber

        if isinstance(created, str):
            self.created = datetime.datetime.strptime(created, "%Y-%m-%dT%H:%M:%S")
        else:
            self.created = self.created

        self.confirmed = False

    def confirm_message(self):
        if self.confirmed:
            return

        r = requests.get(
            constants.API_BASE + "/notification",
            auth=HTTPBasicAuth(self.subscriber.client_id, self.subscriber.client_secret)
        )

        if r.status_code == 200:
            self.confirmed = True

        elif r.status_code == 404:
            raise exceptions.InvalidCredentialsException(
                "The specified client ID and secret do not match a valid subscriber. Check your keys and try again. "
                "You can manage your publishers from the web interface at {}/notifi/subscribers/device".format(
                    constants.URL_BASE
                )
            )

        else:
            raise exceptions.FailedToConfirmMessageException(
                "Could not set confirmation status on message {}. Please try again later. HTTP: {}".format(
                    self.id, r.status_code
                )
            )

    def __repr__(self):
        return "<Message id={} body={}... created={}>".format(
            self.id, self.body[:20], self.created
        )


class Subscriber:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

        self.poll_thread = None

    def poll_messages(self) -> typing.List[Message]:
        r = requests.get(
            constants.API_BASE + "/notification",
            auth=HTTPBasicAuth(self.client_id, self.client_secret)
        )
        if r.status_code == 200:
            messages = []
            for m in r.json():
                messages.append(Message(m["id"], m["body"], m["created"], self))

            return messages

        if r.status_code == 404:
            raise exceptions.InvalidCredentialsException(
                "The specified client ID and secret do not match a valid subscriber. Check your keys and try again. "
                "You can manage your publishers from the web interface at {}/notifi/subscribers/device".format(
                    constants.URL_BASE
                )
            )

        else:
            raise exceptions.FailedToReceiveMessageException(
                "Could not receive messages from API. Please try again later. HTTP: {}".format(
                    r.status_code
                )
            )

    def poll_messages_blocking(self, callback: callable, poll_every: int = 10):
        while True:
            start = time.time()

            for message in self.poll_messages():
                callback(message)

            time.sleep(max([0, poll_every - (time.time() - start)]))

    def poll_messages_async(
            self, callback: callable, poll_every: int = 10, thread_name: str = "Notifi Poll Thread", daemon: bool = True
    ) -> threading.Thread:

        self.poll_thread = threading.Thread(target=self.poll_messages_blocking, args=[callback, poll_every])
        self.poll_thread.setName(thread_name)
        self.poll_thread.setDaemon(daemon)
        self.poll_thread.start()

        return self.poll_thread
