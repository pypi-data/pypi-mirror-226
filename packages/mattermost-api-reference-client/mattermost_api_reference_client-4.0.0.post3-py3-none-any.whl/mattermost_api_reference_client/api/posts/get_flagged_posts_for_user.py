from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_list import PostList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    *,
    team_id: Union[Unset, None, str] = UNSET,
    channel_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["team_id"] = team_id

    params["channel_id"] = channel_id

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/users/{user_id}/posts/flagged".format(
            user_id=user_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["PostList"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PostList.from_dict(response_200_item_data)

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
) -> Response[Union[Any, List["PostList"]]]:
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
    team_id: Union[Unset, None, str] = UNSET,
    channel_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
) -> Response[Union[Any, List["PostList"]]]:
    """Get a list of flagged posts

     Get a page of flagged posts of a user provided user id string. Selects from a channel, team, or all
    flagged posts by a user. Will only return posts from channels in which the user is member.
    ##### Permissions
    Must be user or have `manage_system` permission.

    Args:
        user_id (str):
        team_id (Union[Unset, None, str]):
        channel_id (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['PostList']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    team_id: Union[Unset, None, str] = UNSET,
    channel_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
) -> Optional[Union[Any, List["PostList"]]]:
    """Get a list of flagged posts

     Get a page of flagged posts of a user provided user id string. Selects from a channel, team, or all
    flagged posts by a user. Will only return posts from channels in which the user is member.
    ##### Permissions
    Must be user or have `manage_system` permission.

    Args:
        user_id (str):
        team_id (Union[Unset, None, str]):
        channel_id (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['PostList']]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        team_id=team_id,
        channel_id=channel_id,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    team_id: Union[Unset, None, str] = UNSET,
    channel_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
) -> Response[Union[Any, List["PostList"]]]:
    """Get a list of flagged posts

     Get a page of flagged posts of a user provided user id string. Selects from a channel, team, or all
    flagged posts by a user. Will only return posts from channels in which the user is member.
    ##### Permissions
    Must be user or have `manage_system` permission.

    Args:
        user_id (str):
        team_id (Union[Unset, None, str]):
        channel_id (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['PostList']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    team_id: Union[Unset, None, str] = UNSET,
    channel_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
) -> Optional[Union[Any, List["PostList"]]]:
    """Get a list of flagged posts

     Get a page of flagged posts of a user provided user id string. Selects from a channel, team, or all
    flagged posts by a user. Will only return posts from channels in which the user is member.
    ##### Permissions
    Must be user or have `manage_system` permission.

    Args:
        user_id (str):
        team_id (Union[Unset, None, str]):
        channel_id (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['PostList']]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            team_id=team_id,
            channel_id=channel_id,
            page=page,
            per_page=per_page,
        )
    ).parsed
