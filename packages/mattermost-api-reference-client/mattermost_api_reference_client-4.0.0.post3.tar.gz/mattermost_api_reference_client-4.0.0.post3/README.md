# mattermost-api-reference-client
A client library for accessing Mattermost API Reference

[![pypi](https://badge.fury.io/py/mattermost-api-reference-client.svg)](https://pypi.org/project/mattermost-api-reference-client/)
[![builds.sr.ht status](https://builds.sr.ht/~nicoco/mattermost-api-reference-client/commits/master/.build.yml.svg)](https://builds.sr.ht/~nicoco/mattermost-api-reference-client/commits/master/.build.yml?)

Generated using the awesome [openapi-python-client](https://pypi.org/project/openapi-python-client/) using
the schema provided on the [mattermost api docs](https://api.mattermost.com).

Should provide correct signatures for endpoint calls and correct type hinting for all response models.
Auto-completion works like a charm in pycharm (pun intended), and probably other editors.

## Usage
First, create a client:

```python
from mattermost_api_reference_client import Client

client = Client(base_url="https://mattermost.example.com/api/v4")
```

If the endpoints you're going to hit require authentication, use `AuthenticatedClient` instead.
Get your token either by using the `users.login` endpoint or by grabbing the `MMAUTHTOKEN` from
a web session, using the "storage" tab of developer console to inspect cookies.

```python
from mattermost_api_reference_client import AuthenticatedClient

client = AuthenticatedClient(base_url="https://mattermost.example.com/api/v4", token="MMAUTHTOKEN_VALUE")
```

Now call your endpoint and use your models:

```python
from mattermost_api_reference_client.models import User
from mattermost_api_reference_client.api.users import get_user
from mattermost_api_reference_client.types import Response

my_data: User = get_user.sync("me", client=client)
# or if you need more info (e.g. status_code)
response: Response[User] = get_user.sync_detailed("me", client=client)
```

Or do the same thing with an async version:

```python
my_data: User = await get_user.asyncio(client=client)
response: Response[User] = await get_user.asyncio_detailed(client=client)
```

By default, when you're calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="MMAUTHTOKEN_VALUE",
    verify_ssl="/path/to/certificate_bundle.pem",
)
```

You can also disable certificate validation altogether, but beware that **this is a security risk**.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="MMAUTHTOKEN_VALUE", 
    verify_ssl=False
)
```

Things to know:
1. Every path/method combo becomes a Python module with four functions:
    1. `sync`: Blocking request that returns parsed data (if successful) or `None`
    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.
    1. `asyncio`: Like `sync` but async instead of blocking
    1. `asyncio_detailed`: Like `sync_detailed` but async instead of blocking

1. All path/query params, and bodies become method arguments.
1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)
1. Any endpoint which did not have a tag will be in `mattermost_api_reference_client.api.default`

## Similar to

- https://github.com/Vaelor/python-mattermost-driver
- https://pypi.org/project/mattermost/
