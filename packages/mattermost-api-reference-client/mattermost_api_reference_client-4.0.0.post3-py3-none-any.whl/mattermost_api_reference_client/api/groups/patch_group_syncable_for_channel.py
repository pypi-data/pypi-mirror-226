from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_syncable_channel import GroupSyncableChannel
from ...models.patch_group_syncable_for_channel_json_body import PatchGroupSyncableForChannelJsonBody
from ...types import Response


def _get_kwargs(
    group_id: str,
    channel_id: str,
    *,
    json_body: PatchGroupSyncableForChannelJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/api/v4/groups/{group_id}/channels/{channel_id}/patch".format(
            group_id=group_id,
            channel_id=channel_id,
        ),
        "json": json_json_body,
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
    json_body: PatchGroupSyncableForChannelJsonBody,
) -> Response[Union[Any, GroupSyncableChannel]]:
    """Patch a GroupSyncable associated to Channel

     Partially update a GroupSyncable by providing only the fields you want to update. Omitted fields
    will not be updated. The fields that can be updated are defined in the request body, all other
    provided fields will be ignored.

    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        channel_id (str):
        json_body (PatchGroupSyncableForChannelJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GroupSyncableChannel]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        channel_id=channel_id,
        json_body=json_body,
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
    json_body: PatchGroupSyncableForChannelJsonBody,
) -> Optional[Union[Any, GroupSyncableChannel]]:
    """Patch a GroupSyncable associated to Channel

     Partially update a GroupSyncable by providing only the fields you want to update. Omitted fields
    will not be updated. The fields that can be updated are defined in the request body, all other
    provided fields will be ignored.

    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        channel_id (str):
        json_body (PatchGroupSyncableForChannelJsonBody):

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
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    group_id: str,
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PatchGroupSyncableForChannelJsonBody,
) -> Response[Union[Any, GroupSyncableChannel]]:
    """Patch a GroupSyncable associated to Channel

     Partially update a GroupSyncable by providing only the fields you want to update. Omitted fields
    will not be updated. The fields that can be updated are defined in the request body, all other
    provided fields will be ignored.

    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        channel_id (str):
        json_body (PatchGroupSyncableForChannelJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GroupSyncableChannel]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        channel_id=channel_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str,
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PatchGroupSyncableForChannelJsonBody,
) -> Optional[Union[Any, GroupSyncableChannel]]:
    """Patch a GroupSyncable associated to Channel

     Partially update a GroupSyncable by providing only the fields you want to update. Omitted fields
    will not be updated. The fields that can be updated are defined in the request body, all other
    provided fields will be ignored.

    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        channel_id (str):
        json_body (PatchGroupSyncableForChannelJsonBody):

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
            json_body=json_body,
        )
    ).parsed
