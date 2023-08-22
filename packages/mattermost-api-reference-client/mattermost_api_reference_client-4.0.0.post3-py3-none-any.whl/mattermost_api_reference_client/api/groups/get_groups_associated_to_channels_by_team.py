from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_groups_associated_to_channels_by_team_response_200 import (
    GetGroupsAssociatedToChannelsByTeamResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: str,
    *,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    filter_allow_reference: Union[Unset, None, bool] = False,
    paginate: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["per_page"] = per_page

    params["filter_allow_reference"] = filter_allow_reference

    params["paginate"] = paginate

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/teams/{team_id}/groups_by_channels".format(
            team_id=team_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetGroupsAssociatedToChannelsByTeamResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetGroupsAssociatedToChannelsByTeamResponse200.from_dict(response.json())

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
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, GetGroupsAssociatedToChannelsByTeamResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    filter_allow_reference: Union[Unset, None, bool] = False,
    paginate: Union[Unset, None, bool] = False,
) -> Response[Union[Any, GetGroupsAssociatedToChannelsByTeamResponse200]]:
    """Get team groups by channels

     Retrieve the set of groups associated with the channels in the given team grouped by channel.

    ##### Permissions
    Must have `manage_system` permission or can access only for current user

    __Minimum server version__: 5.11

    Args:
        team_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        filter_allow_reference (Union[Unset, None, bool]):
        paginate (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetGroupsAssociatedToChannelsByTeamResponse200]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        page=page,
        per_page=per_page,
        filter_allow_reference=filter_allow_reference,
        paginate=paginate,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    filter_allow_reference: Union[Unset, None, bool] = False,
    paginate: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, GetGroupsAssociatedToChannelsByTeamResponse200]]:
    """Get team groups by channels

     Retrieve the set of groups associated with the channels in the given team grouped by channel.

    ##### Permissions
    Must have `manage_system` permission or can access only for current user

    __Minimum server version__: 5.11

    Args:
        team_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        filter_allow_reference (Union[Unset, None, bool]):
        paginate (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetGroupsAssociatedToChannelsByTeamResponse200]
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        page=page,
        per_page=per_page,
        filter_allow_reference=filter_allow_reference,
        paginate=paginate,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    filter_allow_reference: Union[Unset, None, bool] = False,
    paginate: Union[Unset, None, bool] = False,
) -> Response[Union[Any, GetGroupsAssociatedToChannelsByTeamResponse200]]:
    """Get team groups by channels

     Retrieve the set of groups associated with the channels in the given team grouped by channel.

    ##### Permissions
    Must have `manage_system` permission or can access only for current user

    __Minimum server version__: 5.11

    Args:
        team_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        filter_allow_reference (Union[Unset, None, bool]):
        paginate (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetGroupsAssociatedToChannelsByTeamResponse200]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        page=page,
        per_page=per_page,
        filter_allow_reference=filter_allow_reference,
        paginate=paginate,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    filter_allow_reference: Union[Unset, None, bool] = False,
    paginate: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, GetGroupsAssociatedToChannelsByTeamResponse200]]:
    """Get team groups by channels

     Retrieve the set of groups associated with the channels in the given team grouped by channel.

    ##### Permissions
    Must have `manage_system` permission or can access only for current user

    __Minimum server version__: 5.11

    Args:
        team_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        filter_allow_reference (Union[Unset, None, bool]):
        paginate (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetGroupsAssociatedToChannelsByTeamResponse200]
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            page=page,
            per_page=per_page,
            filter_allow_reference=filter_allow_reference,
            paginate=paginate,
        )
    ).parsed
