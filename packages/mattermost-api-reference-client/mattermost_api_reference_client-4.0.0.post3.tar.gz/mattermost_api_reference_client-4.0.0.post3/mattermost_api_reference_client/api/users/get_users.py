from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.user import User
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    in_team: Union[Unset, None, str] = UNSET,
    not_in_team: Union[Unset, None, str] = UNSET,
    in_channel: Union[Unset, None, str] = UNSET,
    not_in_channel: Union[Unset, None, str] = UNSET,
    in_group: Union[Unset, None, str] = UNSET,
    group_constrained: Union[Unset, None, bool] = UNSET,
    without_team: Union[Unset, None, bool] = UNSET,
    active: Union[Unset, None, bool] = UNSET,
    inactive: Union[Unset, None, bool] = UNSET,
    role: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    roles: Union[Unset, None, str] = UNSET,
    channel_roles: Union[Unset, None, str] = UNSET,
    team_roles: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["per_page"] = per_page

    params["in_team"] = in_team

    params["not_in_team"] = not_in_team

    params["in_channel"] = in_channel

    params["not_in_channel"] = not_in_channel

    params["in_group"] = in_group

    params["group_constrained"] = group_constrained

    params["without_team"] = without_team

    params["active"] = active

    params["inactive"] = inactive

    params["role"] = role

    params["sort"] = sort

    params["roles"] = roles

    params["channel_roles"] = channel_roles

    params["team_roles"] = team_roles

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/users",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["User"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = User.from_dict(response_200_item_data)

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
) -> Response[Union[Any, List["User"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    in_team: Union[Unset, None, str] = UNSET,
    not_in_team: Union[Unset, None, str] = UNSET,
    in_channel: Union[Unset, None, str] = UNSET,
    not_in_channel: Union[Unset, None, str] = UNSET,
    in_group: Union[Unset, None, str] = UNSET,
    group_constrained: Union[Unset, None, bool] = UNSET,
    without_team: Union[Unset, None, bool] = UNSET,
    active: Union[Unset, None, bool] = UNSET,
    inactive: Union[Unset, None, bool] = UNSET,
    role: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    roles: Union[Unset, None, str] = UNSET,
    channel_roles: Union[Unset, None, str] = UNSET,
    team_roles: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, List["User"]]]:
    """Get users

     Get a page of a list of users. Based on query string parameters, select users from a team, channel,
    or select users not in a specific channel.

    Since server version 4.0, some basic sorting is available using the `sort` query parameter. Sorting
    is currently only supported when selecting users on a team.
    ##### Permissions
    Requires an active session and (if specified) membership to the channel or team being selected from.

    Args:
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        in_team (Union[Unset, None, str]):
        not_in_team (Union[Unset, None, str]):
        in_channel (Union[Unset, None, str]):
        not_in_channel (Union[Unset, None, str]):
        in_group (Union[Unset, None, str]):
        group_constrained (Union[Unset, None, bool]):
        without_team (Union[Unset, None, bool]):
        active (Union[Unset, None, bool]):
        inactive (Union[Unset, None, bool]):
        role (Union[Unset, None, str]):
        sort (Union[Unset, None, str]):
        roles (Union[Unset, None, str]):
        channel_roles (Union[Unset, None, str]):
        team_roles (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['User']]]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        in_team=in_team,
        not_in_team=not_in_team,
        in_channel=in_channel,
        not_in_channel=not_in_channel,
        in_group=in_group,
        group_constrained=group_constrained,
        without_team=without_team,
        active=active,
        inactive=inactive,
        role=role,
        sort=sort,
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
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    in_team: Union[Unset, None, str] = UNSET,
    not_in_team: Union[Unset, None, str] = UNSET,
    in_channel: Union[Unset, None, str] = UNSET,
    not_in_channel: Union[Unset, None, str] = UNSET,
    in_group: Union[Unset, None, str] = UNSET,
    group_constrained: Union[Unset, None, bool] = UNSET,
    without_team: Union[Unset, None, bool] = UNSET,
    active: Union[Unset, None, bool] = UNSET,
    inactive: Union[Unset, None, bool] = UNSET,
    role: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    roles: Union[Unset, None, str] = UNSET,
    channel_roles: Union[Unset, None, str] = UNSET,
    team_roles: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, List["User"]]]:
    """Get users

     Get a page of a list of users. Based on query string parameters, select users from a team, channel,
    or select users not in a specific channel.

    Since server version 4.0, some basic sorting is available using the `sort` query parameter. Sorting
    is currently only supported when selecting users on a team.
    ##### Permissions
    Requires an active session and (if specified) membership to the channel or team being selected from.

    Args:
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        in_team (Union[Unset, None, str]):
        not_in_team (Union[Unset, None, str]):
        in_channel (Union[Unset, None, str]):
        not_in_channel (Union[Unset, None, str]):
        in_group (Union[Unset, None, str]):
        group_constrained (Union[Unset, None, bool]):
        without_team (Union[Unset, None, bool]):
        active (Union[Unset, None, bool]):
        inactive (Union[Unset, None, bool]):
        role (Union[Unset, None, str]):
        sort (Union[Unset, None, str]):
        roles (Union[Unset, None, str]):
        channel_roles (Union[Unset, None, str]):
        team_roles (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['User']]
    """

    return sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        in_team=in_team,
        not_in_team=not_in_team,
        in_channel=in_channel,
        not_in_channel=not_in_channel,
        in_group=in_group,
        group_constrained=group_constrained,
        without_team=without_team,
        active=active,
        inactive=inactive,
        role=role,
        sort=sort,
        roles=roles,
        channel_roles=channel_roles,
        team_roles=team_roles,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    in_team: Union[Unset, None, str] = UNSET,
    not_in_team: Union[Unset, None, str] = UNSET,
    in_channel: Union[Unset, None, str] = UNSET,
    not_in_channel: Union[Unset, None, str] = UNSET,
    in_group: Union[Unset, None, str] = UNSET,
    group_constrained: Union[Unset, None, bool] = UNSET,
    without_team: Union[Unset, None, bool] = UNSET,
    active: Union[Unset, None, bool] = UNSET,
    inactive: Union[Unset, None, bool] = UNSET,
    role: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    roles: Union[Unset, None, str] = UNSET,
    channel_roles: Union[Unset, None, str] = UNSET,
    team_roles: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, List["User"]]]:
    """Get users

     Get a page of a list of users. Based on query string parameters, select users from a team, channel,
    or select users not in a specific channel.

    Since server version 4.0, some basic sorting is available using the `sort` query parameter. Sorting
    is currently only supported when selecting users on a team.
    ##### Permissions
    Requires an active session and (if specified) membership to the channel or team being selected from.

    Args:
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        in_team (Union[Unset, None, str]):
        not_in_team (Union[Unset, None, str]):
        in_channel (Union[Unset, None, str]):
        not_in_channel (Union[Unset, None, str]):
        in_group (Union[Unset, None, str]):
        group_constrained (Union[Unset, None, bool]):
        without_team (Union[Unset, None, bool]):
        active (Union[Unset, None, bool]):
        inactive (Union[Unset, None, bool]):
        role (Union[Unset, None, str]):
        sort (Union[Unset, None, str]):
        roles (Union[Unset, None, str]):
        channel_roles (Union[Unset, None, str]):
        team_roles (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['User']]]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        in_team=in_team,
        not_in_team=not_in_team,
        in_channel=in_channel,
        not_in_channel=not_in_channel,
        in_group=in_group,
        group_constrained=group_constrained,
        without_team=without_team,
        active=active,
        inactive=inactive,
        role=role,
        sort=sort,
        roles=roles,
        channel_roles=channel_roles,
        team_roles=team_roles,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    in_team: Union[Unset, None, str] = UNSET,
    not_in_team: Union[Unset, None, str] = UNSET,
    in_channel: Union[Unset, None, str] = UNSET,
    not_in_channel: Union[Unset, None, str] = UNSET,
    in_group: Union[Unset, None, str] = UNSET,
    group_constrained: Union[Unset, None, bool] = UNSET,
    without_team: Union[Unset, None, bool] = UNSET,
    active: Union[Unset, None, bool] = UNSET,
    inactive: Union[Unset, None, bool] = UNSET,
    role: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    roles: Union[Unset, None, str] = UNSET,
    channel_roles: Union[Unset, None, str] = UNSET,
    team_roles: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, List["User"]]]:
    """Get users

     Get a page of a list of users. Based on query string parameters, select users from a team, channel,
    or select users not in a specific channel.

    Since server version 4.0, some basic sorting is available using the `sort` query parameter. Sorting
    is currently only supported when selecting users on a team.
    ##### Permissions
    Requires an active session and (if specified) membership to the channel or team being selected from.

    Args:
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        in_team (Union[Unset, None, str]):
        not_in_team (Union[Unset, None, str]):
        in_channel (Union[Unset, None, str]):
        not_in_channel (Union[Unset, None, str]):
        in_group (Union[Unset, None, str]):
        group_constrained (Union[Unset, None, bool]):
        without_team (Union[Unset, None, bool]):
        active (Union[Unset, None, bool]):
        inactive (Union[Unset, None, bool]):
        role (Union[Unset, None, str]):
        sort (Union[Unset, None, str]):
        roles (Union[Unset, None, str]):
        channel_roles (Union[Unset, None, str]):
        team_roles (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['User']]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            per_page=per_page,
            in_team=in_team,
            not_in_team=not_in_team,
            in_channel=in_channel,
            not_in_channel=not_in_channel,
            in_group=in_group,
            group_constrained=group_constrained,
            without_team=without_team,
            active=active,
            inactive=inactive,
            role=role,
            sort=sort,
            roles=roles,
            channel_roles=channel_roles,
            team_roles=team_roles,
        )
    ).parsed
