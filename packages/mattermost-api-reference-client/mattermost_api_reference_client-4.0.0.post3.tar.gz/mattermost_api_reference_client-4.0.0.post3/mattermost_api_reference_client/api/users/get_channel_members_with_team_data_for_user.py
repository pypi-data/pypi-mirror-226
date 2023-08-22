from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.channel_member_with_team_data import ChannelMemberWithTeamData
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    *,
    page: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["pageSize"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/users/{user_id}/channel_members".format(
            user_id=user_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["ChannelMemberWithTeamData"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ChannelMemberWithTeamData.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, List["ChannelMemberWithTeamData"]]]:
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
    page: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, List["ChannelMemberWithTeamData"]]]:
    """Get all channel members from all teams for a user

     Get all channel members from all teams for a user.

    __Minimum server version__: 6.2.0

    ##### Permissions
    Logged in as the user, or have `edit_other_users` permission.

    Args:
        user_id (str):
        page (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['ChannelMemberWithTeamData']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        page=page,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, List["ChannelMemberWithTeamData"]]]:
    """Get all channel members from all teams for a user

     Get all channel members from all teams for a user.

    __Minimum server version__: 6.2.0

    ##### Permissions
    Logged in as the user, or have `edit_other_users` permission.

    Args:
        user_id (str):
        page (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['ChannelMemberWithTeamData']]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, List["ChannelMemberWithTeamData"]]]:
    """Get all channel members from all teams for a user

     Get all channel members from all teams for a user.

    __Minimum server version__: 6.2.0

    ##### Permissions
    Logged in as the user, or have `edit_other_users` permission.

    Args:
        user_id (str):
        page (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['ChannelMemberWithTeamData']]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, List["ChannelMemberWithTeamData"]]]:
    """Get all channel members from all teams for a user

     Get all channel members from all teams for a user.

    __Minimum server version__: 6.2.0

    ##### Permissions
    Logged in as the user, or have `edit_other_users` permission.

    Args:
        user_id (str):
        page (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['ChannelMemberWithTeamData']]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            page=page,
            page_size=page_size,
        )
    ).parsed
