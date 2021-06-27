# Notipy
The SDK for Python applications

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
