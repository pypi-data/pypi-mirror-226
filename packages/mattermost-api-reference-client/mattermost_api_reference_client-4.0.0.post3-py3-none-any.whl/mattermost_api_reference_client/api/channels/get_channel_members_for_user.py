from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.channel_member import ChannelMember
from ...types import Response


def _get_kwargs(
    user_id: str,
    team_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/api/v4/users/{user_id}/teams/{team_id}/channels/members".format(
            user_id=user_id,
            team_id=team_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["ChannelMember"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ChannelMember.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[Any, List["ChannelMember"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, List["ChannelMember"]]]:
    """Get channel memberships and roles for a user

     Get all channel memberships and associated membership roles (i.e. `channel_user`, `channel_admin`)
    for a user on a specific team.
    ##### Permissions
    Logged in as the user and `view_team` permission for the team. Having `manage_system` permission
    voids the previous requirements.

    Args:
        user_id (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['ChannelMember']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        team_id=team_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, List["ChannelMember"]]]:
    """Get channel memberships and roles for a user

     Get all channel memberships and associated membership roles (i.e. `channel_user`, `channel_admin`)
    for a user on a specific team.
    ##### Permissions
    Logged in as the user and `view_team` permission for the team. Having `manage_system` permission
    voids the previous requirements.

    Args:
        user_id (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['ChannelMember']]
    """

    return sync_detailed(
        user_id=user_id,
        team_id=team_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, List["ChannelMember"]]]:
    """Get channel memberships and roles for a user

     Get all channel memberships and associated membership roles (i.e. `channel_user`, `channel_admin`)
    for a user on a specific team.
    ##### Permissions
    Logged in as the user and `view_team` permission for the team. Having `manage_system` permission
    voids the previous requirements.

    Args:
        user_id (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['ChannelMember']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        team_id=team_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, List["ChannelMember"]]]:
    """Get channel memberships and roles for a user

     Get all channel memberships and associated membership roles (i.e. `channel_user`, `channel_admin`)
    for a user on a specific team.
    ##### Permissions
    Logged in as the user and `view_team` permission for the team. Having `manage_system` permission
    voids the previous requirements.

    Args:
        user_id (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['ChannelMember']]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            team_id=team_id,
            client=client,
        )
    ).parsed
