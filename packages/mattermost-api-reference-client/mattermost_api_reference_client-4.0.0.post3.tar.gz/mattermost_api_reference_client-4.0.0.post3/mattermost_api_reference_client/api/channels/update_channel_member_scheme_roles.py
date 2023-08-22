from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.status_ok import StatusOK
from ...models.update_channel_member_scheme_roles_json_body import UpdateChannelMemberSchemeRolesJsonBody
from ...types import Response


def _get_kwargs(
    channel_id: str,
    user_id: str,
    *,
    json_body: UpdateChannelMemberSchemeRolesJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/api/v4/channels/{channel_id}/members/{user_id}/schemeRoles".format(
            channel_id=channel_id,
            user_id=user_id,
        ),
        "json": json_json_body,
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
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
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
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateChannelMemberSchemeRolesJsonBody,
) -> Response[Union[Any, StatusOK]]:
    """Update the scheme-derived roles of a channel member.

     Update a channel member's scheme_admin/scheme_user properties. Typically this should either be
    `scheme_admin=false, scheme_user=true` for ordinary channel member, or `scheme_admin=true,
    scheme_user=true` for a channel admin.
    __Minimum server version__: 5.0
    ##### Permissions
    Must be authenticated and have the `manage_channel_roles` permission.

    Args:
        channel_id (str):
        user_id (str):
        json_body (UpdateChannelMemberSchemeRolesJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        user_id=user_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    channel_id: str,
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateChannelMemberSchemeRolesJsonBody,
) -> Optional[Union[Any, StatusOK]]:
    """Update the scheme-derived roles of a channel member.

     Update a channel member's scheme_admin/scheme_user properties. Typically this should either be
    `scheme_admin=false, scheme_user=true` for ordinary channel member, or `scheme_admin=true,
    scheme_user=true` for a channel admin.
    __Minimum server version__: 5.0
    ##### Permissions
    Must be authenticated and have the `manage_channel_roles` permission.

    Args:
        channel_id (str):
        user_id (str):
        json_body (UpdateChannelMemberSchemeRolesJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        channel_id=channel_id,
        user_id=user_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    channel_id: str,
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateChannelMemberSchemeRolesJsonBody,
) -> Response[Union[Any, StatusOK]]:
    """Update the scheme-derived roles of a channel member.

     Update a channel member's scheme_admin/scheme_user properties. Typically this should either be
    `scheme_admin=false, scheme_user=true` for ordinary channel member, or `scheme_admin=true,
    scheme_user=true` for a channel admin.
    __Minimum server version__: 5.0
    ##### Permissions
    Must be authenticated and have the `manage_channel_roles` permission.

    Args:
        channel_id (str):
        user_id (str):
        json_body (UpdateChannelMemberSchemeRolesJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        user_id=user_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    channel_id: str,
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateChannelMemberSchemeRolesJsonBody,
) -> Optional[Union[Any, StatusOK]]:
    """Update the scheme-derived roles of a channel member.

     Update a channel member's scheme_admin/scheme_user properties. Typically this should either be
    `scheme_admin=false, scheme_user=true` for ordinary channel member, or `scheme_admin=true,
    scheme_user=true` for a channel admin.
    __Minimum server version__: 5.0
    ##### Permissions
    Must be authenticated and have the `manage_channel_roles` permission.

    Args:
        channel_id (str):
        user_id (str):
        json_body (UpdateChannelMemberSchemeRolesJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            channel_id=channel_id,
            user_id=user_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
