from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.channel import Channel
from ...models.update_channel_json_body import UpdateChannelJsonBody
from ...types import Response


def _get_kwargs(
    channel_id: str,
    *,
    json_body: UpdateChannelJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/api/v4/channels/{channel_id}".format(
            channel_id=channel_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Channel]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Channel.from_dict(response.json())

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
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateChannelJsonBody,
) -> Response[Union[Any, Channel]]:
    """Update a channel

     Update a channel. The fields that can be updated are listed as parameters. Omitted fields will be
    treated as blanks.
    ##### Permissions
    If updating a public channel, `manage_public_channel_members` permission is required. If updating a
    private channel, `manage_private_channel_members` permission is required.

    Args:
        channel_id (str):
        json_body (UpdateChannelJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Channel]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateChannelJsonBody,
) -> Optional[Union[Any, Channel]]:
    """Update a channel

     Update a channel. The fields that can be updated are listed as parameters. Omitted fields will be
    treated as blanks.
    ##### Permissions
    If updating a public channel, `manage_public_channel_members` permission is required. If updating a
    private channel, `manage_private_channel_members` permission is required.

    Args:
        channel_id (str):
        json_body (UpdateChannelJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Channel]
    """

    return sync_detailed(
        channel_id=channel_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateChannelJsonBody,
) -> Response[Union[Any, Channel]]:
    """Update a channel

     Update a channel. The fields that can be updated are listed as parameters. Omitted fields will be
    treated as blanks.
    ##### Permissions
    If updating a public channel, `manage_public_channel_members` permission is required. If updating a
    private channel, `manage_private_channel_members` permission is required.

    Args:
        channel_id (str):
        json_body (UpdateChannelJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Channel]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    channel_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateChannelJsonBody,
) -> Optional[Union[Any, Channel]]:
    """Update a channel

     Update a channel. The fields that can be updated are listed as parameters. Omitted fields will be
    treated as blanks.
    ##### Permissions
    If updating a public channel, `manage_public_channel_members` permission is required. If updating a
    private channel, `manage_private_channel_members` permission is required.

    Args:
        channel_id (str):
        json_body (UpdateChannelJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Channel]
    """

    return (
        await asyncio_detailed(
            channel_id=channel_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
