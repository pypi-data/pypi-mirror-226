from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.channel import Channel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    team_id: str,
    *,
    include_deleted: Union[Unset, None, bool] = False,
    last_delete_at: Union[Unset, None, int] = 0,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["include_deleted"] = include_deleted

    params["last_delete_at"] = last_delete_at

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/users/{user_id}/teams/{team_id}/channels".format(
            user_id=user_id,
            team_id=team_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["Channel"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Channel.from_dict(response_200_item_data)

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
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, List["Channel"]]]:
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
    include_deleted: Union[Unset, None, bool] = False,
    last_delete_at: Union[Unset, None, int] = 0,
) -> Response[Union[Any, List["Channel"]]]:
    """Get channels for user

     Get all the channels on a team for a user.
    ##### Permissions
    Logged in as the user, or have `edit_other_users` permission, and `view_team` permission for the
    team.

    Args:
        user_id (str):
        team_id (str):
        include_deleted (Union[Unset, None, bool]):
        last_delete_at (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Channel']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        team_id=team_id,
        include_deleted=include_deleted,
        last_delete_at=last_delete_at,
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
    include_deleted: Union[Unset, None, bool] = False,
    last_delete_at: Union[Unset, None, int] = 0,
) -> Optional[Union[Any, List["Channel"]]]:
    """Get channels for user

     Get all the channels on a team for a user.
    ##### Permissions
    Logged in as the user, or have `edit_other_users` permission, and `view_team` permission for the
    team.

    Args:
        user_id (str):
        team_id (str):
        include_deleted (Union[Unset, None, bool]):
        last_delete_at (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Channel']]
    """

    return sync_detailed(
        user_id=user_id,
        team_id=team_id,
        client=client,
        include_deleted=include_deleted,
        last_delete_at=last_delete_at,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = False,
    last_delete_at: Union[Unset, None, int] = 0,
) -> Response[Union[Any, List["Channel"]]]:
    """Get channels for user

     Get all the channels on a team for a user.
    ##### Permissions
    Logged in as the user, or have `edit_other_users` permission, and `view_team` permission for the
    team.

    Args:
        user_id (str):
        team_id (str):
        include_deleted (Union[Unset, None, bool]):
        last_delete_at (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Channel']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        team_id=team_id,
        include_deleted=include_deleted,
        last_delete_at=last_delete_at,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = False,
    last_delete_at: Union[Unset, None, int] = 0,
) -> Optional[Union[Any, List["Channel"]]]:
    """Get channels for user

     Get all the channels on a team for a user.
    ##### Permissions
    Logged in as the user, or have `edit_other_users` permission, and `view_team` permission for the
    team.

    Args:
        user_id (str):
        team_id (str):
        include_deleted (Union[Unset, None, bool]):
        last_delete_at (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Channel']]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            team_id=team_id,
            client=client,
            include_deleted=include_deleted,
            last_delete_at=last_delete_at,
        )
    ).parsed
