from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.status_ok import StatusOK
from ...types import Response


def _get_kwargs(
    user_id: str,
    post_id: str,
    emoji_name: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "delete",
        "url": "/api/v4/users/{user_id}/posts/{post_id}/reactions/{emoji_name}".format(
            user_id=user_id,
            post_id=post_id,
            emoji_name=emoji_name,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, StatusOK]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = StatusOK.from_dict(response.json())

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
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, StatusOK]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    post_id: str,
    emoji_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, StatusOK]]:
    """Remove a reaction from a post

     Deletes a reaction made by a user from the given post.
    ##### Permissions
    Must be user or have `manage_system` permission.

    Args:
        user_id (str):
        post_id (str):
        emoji_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        post_id=post_id,
        emoji_name=emoji_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    post_id: str,
    emoji_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, StatusOK]]:
    """Remove a reaction from a post

     Deletes a reaction made by a user from the given post.
    ##### Permissions
    Must be user or have `manage_system` permission.

    Args:
        user_id (str):
        post_id (str):
        emoji_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        user_id=user_id,
        post_id=post_id,
        emoji_name=emoji_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    post_id: str,
    emoji_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, StatusOK]]:
    """Remove a reaction from a post

     Deletes a reaction made by a user from the given post.
    ##### Permissions
    Must be user or have `manage_system` permission.

    Args:
        user_id (str):
        post_id (str):
        emoji_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        post_id=post_id,
        emoji_name=emoji_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    post_id: str,
    emoji_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, StatusOK]]:
    """Remove a reaction from a post

     Deletes a reaction made by a user from the given post.
    ##### Permissions
    Must be user or have `manage_system` permission.

    Args:
        user_id (str):
        post_id (str):
        emoji_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            post_id=post_id,
            emoji_name=emoji_name,
            client=client,
        )
    ).parsed
