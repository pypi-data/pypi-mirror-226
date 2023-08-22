from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.channel import Channel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: str,
    channel_name: str,
    *,
    include_deleted: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["include_deleted"] = include_deleted

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/teams/{team_id}/channels/name/{channel_name}".format(
            team_id=team_id,
            channel_name=channel_name,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Channel]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Channel.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Channel]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: str,
    channel_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = False,
) -> Response[Union[Any, Channel]]:
    """Get a channel by name

     Gets channel from the provided team id and channel name strings.
    ##### Permissions
    `read_channel` permission for the channel.

    Args:
        team_id (str):
        channel_name (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Channel]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        channel_name=channel_name,
        include_deleted=include_deleted,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: str,
    channel_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, Channel]]:
    """Get a channel by name

     Gets channel from the provided team id and channel name strings.
    ##### Permissions
    `read_channel` permission for the channel.

    Args:
        team_id (str):
        channel_name (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Channel]
    """

    return sync_detailed(
        team_id=team_id,
        channel_name=channel_name,
        client=client,
        include_deleted=include_deleted,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    channel_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = False,
) -> Response[Union[Any, Channel]]:
    """Get a channel by name

     Gets channel from the provided team id and channel name strings.
    ##### Permissions
    `read_channel` permission for the channel.

    Args:
        team_id (str):
        channel_name (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Channel]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        channel_name=channel_name,
        include_deleted=include_deleted,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    channel_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, Channel]]:
    """Get a channel by name

     Gets channel from the provided team id and channel name strings.
    ##### Permissions
    `read_channel` permission for the channel.

    Args:
        team_id (str):
        channel_name (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Channel]
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            channel_name=channel_name,
            client=client,
            include_deleted=include_deleted,
        )
    ).parsed
