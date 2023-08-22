from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_syncable_team import GroupSyncableTeam
from ...types import Response


def _get_kwargs(
    group_id: str,
    team_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "post",
        "url": "/api/v4/groups/{group_id}/teams/{team_id}/link".format(
            group_id=group_id,
            team_id=team_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GroupSyncableTeam]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = GroupSyncableTeam.from_dict(response.json())

        return response_201
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
) -> Response[Union[Any, GroupSyncableTeam]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, GroupSyncableTeam]]:
    """Link a team to a group

     Link a team to a group
    ##### Permissions
    Must have `manage_team` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GroupSyncableTeam]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        team_id=team_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, GroupSyncableTeam]]:
    """Link a team to a group

     Link a team to a group
    ##### Permissions
    Must have `manage_team` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GroupSyncableTeam]
    """

    return sync_detailed(
        group_id=group_id,
        team_id=team_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, GroupSyncableTeam]]:
    """Link a team to a group

     Link a team to a group
    ##### Permissions
    Must have `manage_team` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GroupSyncableTeam]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        team_id=team_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, GroupSyncableTeam]]:
    """Link a team to a group

     Link a team to a group
    ##### Permissions
    Must have `manage_team` permission.

    __Minimum server version__: 5.11

    Args:
        group_id (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GroupSyncableTeam]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            team_id=team_id,
            client=client,
        )
    ).parsed
