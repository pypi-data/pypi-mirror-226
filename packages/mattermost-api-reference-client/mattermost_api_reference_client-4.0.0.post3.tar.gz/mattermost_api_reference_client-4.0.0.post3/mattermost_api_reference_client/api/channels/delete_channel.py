from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.status_ok import StatusOK
from ...types import Response


def _get_kwargs(
    channel_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "delete",
        "url": "/api/v4/channels/{channel_id}".format(
            channel_id=channel_id,
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
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, StatusOK]]:
    """Delete a channel

     Archives a channel. This will set the `deleteAt` to the current timestamp in the database. Soft
    deleted channels may not be accessible in the user interface. They can be viewed and unarchived in
    the **System Console > User Management > Channels** based on your license. Direct and group message
    channels cannot be deleted.

    As of server version 5.28, optionally use the `permanent=true` query parameter to permanently delete
    the channel for compliance reasons. To use this feature `ServiceSettings.EnableAPIChannelDeletion`
    must be set to `true` in the server's configuration.  If you permanently delete a channel this
    action is not recoverable outside of a database backup.

    ##### Permissions
    `delete_public_channel` permission if the channel is public,
    `delete_private_channel` permission if the channel is private,
    or have `manage_system` permission.

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, StatusOK]]:
    """Delete a channel

     Archives a channel. This will set the `deleteAt` to the current timestamp in the database. Soft
    deleted channels may not be accessible in the user interface. They can be viewed and unarchived in
    the **System Console > User Management > Channels** based on your license. Direct and group message
    channels cannot be deleted.

    As of server version 5.28, optionally use the `permanent=true` query parameter to permanently delete
    the channel for compliance reasons. To use this feature `ServiceSettings.EnableAPIChannelDeletion`
    must be set to `true` in the server's configuration.  If you permanently delete a channel this
    action is not recoverable outside of a database backup.

    ##### Permissions
    `delete_public_channel` permission if the channel is public,
    `delete_private_channel` permission if the channel is private,
    or have `manage_system` permission.

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        channel_id=channel_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, StatusOK]]:
    """Delete a channel

     Archives a channel. This will set the `deleteAt` to the current timestamp in the database. Soft
    deleted channels may not be accessible in the user interface. They can be viewed and unarchived in
    the **System Console > User Management > Channels** based on your license. Direct and group message
    channels cannot be deleted.

    As of server version 5.28, optionally use the `permanent=true` query parameter to permanently delete
    the channel for compliance reasons. To use this feature `ServiceSettings.EnableAPIChannelDeletion`
    must be set to `true` in the server's configuration.  If you permanently delete a channel this
    action is not recoverable outside of a database backup.

    ##### Permissions
    `delete_public_channel` permission if the channel is public,
    `delete_private_channel` permission if the channel is private,
    or have `manage_system` permission.

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, StatusOK]]:
    """Delete a channel

     Archives a channel. This will set the `deleteAt` to the current timestamp in the database. Soft
    deleted channels may not be accessible in the user interface. They can be viewed and unarchived in
    the **System Console > User Management > Channels** based on your license. Direct and group message
    channels cannot be deleted.

    As of server version 5.28, optionally use the `permanent=true` query parameter to permanently delete
    the channel for compliance reasons. To use this feature `ServiceSettings.EnableAPIChannelDeletion`
    must be set to `true` in the server's configuration.  If you permanently delete a channel this
    action is not recoverable outside of a database backup.

    ##### Permissions
    `delete_public_channel` permission if the channel is public,
    `delete_private_channel` permission if the channel is private,
    or have `manage_system` permission.

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            channel_id=channel_id,
            client=client,
        )
    ).parsed
