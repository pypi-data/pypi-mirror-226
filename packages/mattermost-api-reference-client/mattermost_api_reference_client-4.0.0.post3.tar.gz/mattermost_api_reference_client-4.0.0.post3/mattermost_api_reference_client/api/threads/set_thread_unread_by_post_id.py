from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    user_id: str,
    team_id: str,
    thread_id: str,
    post_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "put",
        "url": "/api/v4/users/{user_id}/teams/{team_id}/threads/{thread_id}/set_unread/{post_id}".format(
            user_id=user_id,
            team_id=team_id,
            thread_id=thread_id,
            post_id=post_id,
        ),
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    team_id: str,
    thread_id: str,
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """Mark a thread that user is following as unread based on a post id

     Mark a thread that user is following as unread

    __Minimum server version__: 6.7

    ##### Permissions
    Must have `read_channel` permission for the channel the thread is in or if the channel is public,
    have the `read_public_channels` permission for the team.

    Must have `edit_other_users` permission if the user is not the one marking the thread for himself.

    Args:
        user_id (str):
        team_id (str):
        thread_id (str):
        post_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        team_id=team_id,
        thread_id=thread_id,
        post_id=post_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    user_id: str,
    team_id: str,
    thread_id: str,
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """Mark a thread that user is following as unread based on a post id

     Mark a thread that user is following as unread

    __Minimum server version__: 6.7

    ##### Permissions
    Must have `read_channel` permission for the channel the thread is in or if the channel is public,
    have the `read_public_channels` permission for the team.

    Must have `edit_other_users` permission if the user is not the one marking the thread for himself.

    Args:
        user_id (str):
        team_id (str):
        thread_id (str):
        post_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        team_id=team_id,
        thread_id=thread_id,
        post_id=post_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
