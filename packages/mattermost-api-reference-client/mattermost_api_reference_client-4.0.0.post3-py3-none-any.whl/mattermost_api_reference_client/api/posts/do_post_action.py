from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.status_ok import StatusOK
from ...types import Response


def _get_kwargs(
    post_id: str,
    action_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "post",
        "url": "/api/v4/posts/{post_id}/actions/{action_id}".format(
            post_id=post_id,
            action_id=action_id,
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
    post_id: str,
    action_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, StatusOK]]:
    """Perform a post action

     Perform a post action, which allows users to interact with integrations through posts.
    ##### Permissions
    Must be authenticated and have the `read_channel` permission to the channel the post is in.

    Args:
        post_id (str):
        action_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        post_id=post_id,
        action_id=action_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    post_id: str,
    action_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, StatusOK]]:
    """Perform a post action

     Perform a post action, which allows users to interact with integrations through posts.
    ##### Permissions
    Must be authenticated and have the `read_channel` permission to the channel the post is in.

    Args:
        post_id (str):
        action_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        post_id=post_id,
        action_id=action_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    post_id: str,
    action_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, StatusOK]]:
    """Perform a post action

     Perform a post action, which allows users to interact with integrations through posts.
    ##### Permissions
    Must be authenticated and have the `read_channel` permission to the channel the post is in.

    Args:
        post_id (str):
        action_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        post_id=post_id,
        action_id=action_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    post_id: str,
    action_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, StatusOK]]:
    """Perform a post action

     Perform a post action, which allows users to interact with integrations through posts.
    ##### Permissions
    Must be authenticated and have the `read_channel` permission to the channel the post is in.

    Args:
        post_id (str):
        action_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            post_id=post_id,
            action_id=action_id,
            client=client,
        )
    ).parsed
