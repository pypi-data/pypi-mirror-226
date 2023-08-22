from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.team_unread import TeamUnread
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    *,
    exclude_team: str,
    include_collapsed_threads: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["exclude_team"] = exclude_team

    params["include_collapsed_threads"] = include_collapsed_threads

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/users/{user_id}/teams/unread".format(
            user_id=user_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["TeamUnread"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TeamUnread.from_dict(response_200_item_data)

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
) -> Response[Union[Any, List["TeamUnread"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    exclude_team: str,
    include_collapsed_threads: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List["TeamUnread"]]]:
    """Get team unreads for a user

     Get the count for unread messages and mentions in the teams the user is a member of.
    ##### Permissions
    Must be logged in.

    Args:
        user_id (str):
        exclude_team (str):
        include_collapsed_threads (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['TeamUnread']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        exclude_team=exclude_team,
        include_collapsed_threads=include_collapsed_threads,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    exclude_team: str,
    include_collapsed_threads: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List["TeamUnread"]]]:
    """Get team unreads for a user

     Get the count for unread messages and mentions in the teams the user is a member of.
    ##### Permissions
    Must be logged in.

    Args:
        user_id (str):
        exclude_team (str):
        include_collapsed_threads (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['TeamUnread']]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        exclude_team=exclude_team,
        include_collapsed_threads=include_collapsed_threads,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    exclude_team: str,
    include_collapsed_threads: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List["TeamUnread"]]]:
    """Get team unreads for a user

     Get the count for unread messages and mentions in the teams the user is a member of.
    ##### Permissions
    Must be logged in.

    Args:
        user_id (str):
        exclude_team (str):
        include_collapsed_threads (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['TeamUnread']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        exclude_team=exclude_team,
        include_collapsed_threads=include_collapsed_threads,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    exclude_team: str,
    include_collapsed_threads: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List["TeamUnread"]]]:
    """Get team unreads for a user

     Get the count for unread messages and mentions in the teams the user is a member of.
    ##### Permissions
    Must be logged in.

    Args:
        user_id (str):
        exclude_team (str):
        include_collapsed_threads (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['TeamUnread']]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            exclude_team=exclude_team,
            include_collapsed_threads=include_collapsed_threads,
        )
    ).parsed
