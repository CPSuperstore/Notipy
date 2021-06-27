# Notipy
The SDK for Python applications

- [Publishing a Message](#publishing-a-message)
    - [PublicationResponse](#publicationresponse)
- [Subscribing a Message](#subscribing-a-message)
    - [Single Message Poll](#single-message-poll)
    - [Indefinite Message Poll](#indefinite-message-poll)
    - [Asynchronous Indefinite Message Poll](#asynchronous-indefinite-message-poll)
    - [Message](#message)

## Publishing a Message
Use the following code to publish a message:

```python
from Notipy.publisher import Publisher

pub = Publisher("client_id", "client_secret")

# you can optionally specify a single category, or list of categories.
# use the reference when working with categories. Default is '*' (all categories)
resp = pub.publish("message")
```

You can get your Client ID and Secret from the [Publisher Management Page](https://notifi.pythonanywhere.com/notifi/publishers)

Calling `pub.publush` can produce the following exceptions:
- `InvalidCredentialsException` - The `client_id` and `client_secret` specified do not match a valid account. Note that creating the `Publisher` object does not validate credentials, so the exception will not be thrown until you attempt to publish 
- `FailedToSendMessageException` - The API endpoint returned a status code other than 200, and the failure was not caused by bad credentials.

### PublicationResponse
Calling `resp = pub.publish("Test")` will return a `PublicationResponse` object. 

This object contains the following attributes:
- `passed` - The number of subscribers the message has been successfully sent to
- `failed` - The number of subscribers the message has failed to send to
- `total` - The total number of subscribers a message has attempted to send to (`passed` + `failed`)

This object also contains the following methods:
- `passed_percent` - The percent of messages which were successfully sent (or 0 if no messages were sent)
- `failed_percent` - The percent of messages which failed to send (or 0 if no messages were sent)

## Subscribing a Message
Use the following code to publish a message. In every case, the variable `messages` is a list of the `Message` object.

The following exceptions may be thrown with subscribing.
- `InvalidCredentialsException` - The `client_id` and `client_secret` specified do not match a valid account. Note that creating the `Publisher` object does not validate credentials, so the exception will not be thrown until you attempt to publish 
- `FailedToConfirmMessageException` - Something went wrong while attempting to confirm the message as sent. Try again later.
- `FailedToReceiveMessageException` - Something went wrong while receiving messages from the server. Try again later.

#### Single Message Poll
The following code polls the server for pending messages once. 

```python
from Notipy.subscriber import Subscriber

sub = Subscriber("client_id", "client_secret")

messages = sub.poll_messages()
```

#### Indefinite Message Poll
The following code polls the server for pending messages indefinitely

```python
from Notipy.subscriber import Subscriber

sub = Subscriber("client_id", "client_secret")


def on_message(messages):
    print(messages)

# You can also specify "poll_every" which is the number of seconds to poll the API. 
# Please do not set this value any lower than 10s
resp = sub.poll_messages_blocking(callback=on_message)
```

#### Asynchronous Indefinite Message Poll
The following code polls the server for pending messages indefinitely in the background as a thread

```python
from Notipy.subscriber import Subscriber

sub = Subscriber("client_id", "client_secret")


def on_message(messages):
    print(messages)

# You can also specify "poll_every" which is the number of seconds to poll the API. 
# Please do not set this value any lower than 10s
# In addition, you can also set "thread_name" to override the name of the thread (default is "Notifi Poll Thread")
# "daemon" is used to set if the thread is a daemon or not. Default is "True"
resp = sub.poll_messages_async(callback=on_message)
```

### Message
Regardless of the poll type, `messages` is a list of this `Message` object.

This object contains the following attributes:
- `id` - The ID of the message
- `body` - The body of the message
- `created` - The date and time the message was published
- `confirmed` - If the message has been confirmed as sent (This will be set to `True` automatically when you are finished with the message)

This object also contains the following methods:
- `confirm_message` - Marks the message as successfully sent. This indicates the message was sent by your application with no errors, so call this AFTER you are finished handling the message.
