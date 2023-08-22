from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.users_stats import UsersStats
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    in_team: Union[Unset, None, str] = UNSET,
    in_channel: Union[Unset, None, str] = UNSET,
    include_deleted: Union[Unset, None, bool] = UNSET,
    include_bots: Union[Unset, None, bool] = UNSET,
    roles: Union[Unset, None, str] = UNSET,
    channel_roles: Union[Unset, None, str] = UNSET,
    team_roles: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["in_team"] = in_team

    params["in_channel"] = in_channel

    params["include_deleted"] = include_deleted

    params["include_bots"] = include_bots

    params["roles"] = roles

    params["channel_roles"] = channel_roles

    params["team_roles"] = team_roles

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/users/stats/filtered",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, UsersStats]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UsersStats.from_dict(response.json())

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
) -> Response[Union[Any, UsersStats]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    in_team: Union[Unset, None, str] = UNSET,
    in_channel: Union[Unset, None, str] = UNSET,
    include_deleted: Union[Unset, None, bool] = UNSET,
    include_bots: Union[Unset, None, bool] = UNSET,
    roles: Union[Unset, None, str] = UNSET,
    channel_roles: Union[Unset, None, str] = UNSET,
    team_roles: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, UsersStats]]:
    """Get total count of users in the system matching the specified filters

     Get a count of users in the system matching the specified filters.

    __Minimum server version__: 5.26

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        in_team (Union[Unset, None, str]):
        in_channel (Union[Unset, None, str]):
        include_deleted (Union[Unset, None, bool]):
        include_bots (Union[Unset, None, bool]):
        roles (Union[Unset, None, str]):
        channel_roles (Union[Unset, None, str]):
        team_roles (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UsersStats]]
    """

    kwargs = _get_kwargs(
        in_team=in_team,
        in_channel=in_channel,
        include_deleted=include_deleted,
        include_bots=include_bots,
        roles=roles,
        channel_roles=channel_roles,
        team_roles=team_roles,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    in_team: Union[Unset, None, str] = UNSET,
    in_channel: Union[Unset, None, str] = UNSET,
    include_deleted: Union[Unset, None, bool] = UNSET,
    include_bots: Union[Unset, None, bool] = UNSET,
    roles: Union[Unset, None, str] = UNSET,
    channel_roles: Union[Unset, None, str] = UNSET,
    team_roles: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, UsersStats]]:
    """Get total count of users in the system matching the specified filters

     Get a count of users in the system matching the specified filters.

    __Minimum server version__: 5.26

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        in_team (Union[Unset, None, str]):
        in_channel (Union[Unset, None, str]):
        include_deleted (Union[Unset, None, bool]):
        include_bots (Union[Unset, None, bool]):
        roles (Union[Unset, None, str]):
        channel_roles (Union[Unset, None, str]):
        team_roles (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UsersStats]
    """

    return sync_detailed(
        client=client,
        in_team=in_team,
        in_channel=in_channel,
        include_deleted=include_deleted,
        include_bots=include_bots,
        roles=roles,
        channel_roles=channel_roles,
        team_roles=team_roles,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    in_team: Union[Unset, None, str] = UNSET,
    in_channel: Union[Unset, None, str] = UNSET,
    include_deleted: Union[Unset, None, bool] = UNSET,
    include_bots: Union[Unset, None, bool] = UNSET,
    roles: Union[Unset, None, str] = UNSET,
    channel_roles: Union[Unset, None, str] = UNSET,
    team_roles: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, UsersStats]]:
    """Get total count of users in the system matching the specified filters

     Get a count of users in the system matching the specified filters.

    __Minimum server version__: 5.26

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        in_team (Union[Unset, None, str]):
        in_channel (Union[Unset, None, str]):
        include_deleted (Union[Unset, None, bool]):
        include_bots (Union[Unset, None, bool]):
        roles (Union[Unset, None, str]):
        channel_roles (Union[Unset, None, str]):
        team_roles (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UsersStats]]
    """

    kwargs = _get_kwargs(
        in_team=in_team,
        in_channel=in_channel,
        include_deleted=include_deleted,
        include_bots=include_bots,
        roles=roles,
        channel_roles=channel_roles,
        team_roles=team_roles,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    in_team: Union[Unset, None, str] = UNSET,
    in_channel: Union[Unset, None, str] = UNSET,
    include_deleted: Union[Unset, None, bool] = UNSET,
    include_bots: Union[Unset, None, bool] = UNSET,
    roles: Union[Unset, None, str] = UNSET,
    channel_roles: Union[Unset, None, str] = UNSET,
    team_roles: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, UsersStats]]:
    """Get total count of users in the system matching the specified filters

     Get a count of users in the system matching the specified filters.

    __Minimum server version__: 5.26

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        in_team (Union[Unset, None, str]):
        in_channel (Union[Unset, None, str]):
        include_deleted (Union[Unset, None, bool]):
        include_bots (Union[Unset, None, bool]):
        roles (Union[Unset, None, str]):
        channel_roles (Union[Unset, None, str]):
        team_roles (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UsersStats]
    """

    return (
        await asyncio_detailed(
            client=client,
            in_team=in_team,
            in_channel=in_channel,
            include_deleted=include_deleted,
            include_bots=include_bots,
            roles=roles,
            channel_roles=channel_roles,
            team_roles=team_roles,
        )
    ).parsed
