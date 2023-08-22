from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.emoji import Emoji
from ...types import Response


def _get_kwargs(
    emoji_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "delete",
        "url": "/api/v4/emoji/{emoji_id}".format(
            emoji_id=emoji_id,
        ),
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
    emoji_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Emoji]]:
    """Delete a custom emoji

     Delete a custom emoji.
    ##### Permissions
    Must have the `manage_team` or `manage_system` permissions or be the user who created the emoji.

    Args:
        emoji_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Emoji]]
    """

    kwargs = _get_kwargs(
        emoji_id=emoji_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    emoji_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Emoji]]:
    """Delete a custom emoji

     Delete a custom emoji.
    ##### Permissions
    Must have the `manage_team` or `manage_system` permissions or be the user who created the emoji.

    Args:
        emoji_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Emoji]
    """

    return sync_detailed(
        emoji_id=emoji_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    emoji_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Emoji]]:
    """Delete a custom emoji

     Delete a custom emoji.
    ##### Permissions
    Must have the `manage_team` or `manage_system` permissions or be the user who created the emoji.

    Args:
        emoji_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Emoji]]
    """

    kwargs = _get_kwargs(
        emoji_id=emoji_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    emoji_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Emoji]]:
    """Delete a custom emoji

     Delete a custom emoji.
    ##### Permissions
    Must have the `manage_team` or `manage_system` permissions or be the user who created the emoji.

    Args:
        emoji_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Emoji]
    """

    return (
        await asyncio_detailed(
            emoji_id=emoji_id,
            client=client,
        )
    ).parsed
