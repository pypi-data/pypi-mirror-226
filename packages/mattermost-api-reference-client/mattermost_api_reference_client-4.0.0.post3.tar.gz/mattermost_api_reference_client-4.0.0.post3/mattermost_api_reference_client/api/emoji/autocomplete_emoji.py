from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.emoji import Emoji
from ...types import UNSET, Response


def _get_kwargs(
    *,
    name: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["name"] = name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/emoji/autocomplete",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Emoji]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Emoji.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Emoji]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
) -> Response[Union[Any, Emoji]]:
    """Autocomplete custom emoji

     Get a list of custom emoji with names starting with or matching the provided name. Returns a maximum
    of 100 results.
    ##### Permissions
    Must be authenticated.

    __Minimum server version__: 4.7

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Emoji]]
    """

    kwargs = _get_kwargs(
        name=name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
) -> Optional[Union[Any, Emoji]]:
    """Autocomplete custom emoji

     Get a list of custom emoji with names starting with or matching the provided name. Returns a maximum
    of 100 results.
    ##### Permissions
    Must be authenticated.

    __Minimum server version__: 4.7

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Emoji]
    """

    return sync_detailed(
        client=client,
        name=name,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
) -> Response[Union[Any, Emoji]]:
    """Autocomplete custom emoji

     Get a list of custom emoji with names starting with or matching the provided name. Returns a maximum
    of 100 results.
    ##### Permissions
    Must be authenticated.

    __Minimum server version__: 4.7

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Emoji]]
    """

    kwargs = _get_kwargs(
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
) -> Optional[Union[Any, Emoji]]:
    """Autocomplete custom emoji

     Get a list of custom emoji with names starting with or matching the provided name. Returns a maximum
    of 100 results.
    ##### Permissions
    Must be authenticated.

    __Minimum server version__: 4.7

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Emoji]
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
        )
    ).parsed
