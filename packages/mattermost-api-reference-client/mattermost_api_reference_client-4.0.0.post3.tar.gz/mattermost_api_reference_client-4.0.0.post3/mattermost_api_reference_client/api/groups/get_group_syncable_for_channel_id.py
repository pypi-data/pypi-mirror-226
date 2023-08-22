from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_syncable_channel import GroupSyncableChannel
from ...types import Response


def _get_kwargs(
    group_id: str,
    channel_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/api/v4/groups/{group_id}/channels/{channel_id}".format(
            group_id=group_id,
            channel_id=channel_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GroupSyncableChannel]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GroupSyncableChannel.from_dict(response.json())

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
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, GroupSyncableChannel]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: str,
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, GroupSyncableChannel]]:
    """Get GroupSyncable from channel ID

     Get the GroupSyncable object with group_id and channel_id from params
    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GroupSyncableChannel]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        channel_id=channel_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: str,
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, GroupSyncableChannel]]:
    """Get GroupSyncable from channel ID

     Get the GroupSyncable object with group_id and channel_id from params
    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GroupSyncableChannel]
    """

    return sync_detailed(
        group_id=group_id,
        channel_id=channel_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_id: str,
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, GroupSyncableChannel]]:
    """Get GroupSyncable from channel ID

     Get the GroupSyncable object with group_id and channel_id from params
    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GroupSyncableChannel]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        channel_id=channel_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str,
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, GroupSyncableChannel]]:
    """Get GroupSyncable from channel ID

     Get the GroupSyncable object with group_id and channel_id from params
    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GroupSyncableChannel]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            channel_id=channel_id,
            client=client,
        )
    ).parsed
