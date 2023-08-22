from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_channels_direction import GetChannelsDirection
from ...models.get_channels_sort import GetChannelsSort
from ...models.get_channels_status import GetChannelsStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    team_id: str,
    sort: Union[Unset, None, GetChannelsSort] = GetChannelsSort.CREATE_AT,
    direction: Union[Unset, None, GetChannelsDirection] = GetChannelsDirection.DESC,
    status: Union[Unset, None, GetChannelsStatus] = GetChannelsStatus.ALL,
    owner_user_id: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    participant_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["team_id"] = team_id

    json_sort: Union[Unset, None, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value if sort else None

    params["sort"] = json_sort

    json_direction: Union[Unset, None, str] = UNSET
    if not isinstance(direction, Unset):
        json_direction = direction.value if direction else None

    params["direction"] = json_direction

    json_status: Union[Unset, None, str] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value if status else None

    params["status"] = json_status

    params["owner_user_id"] = owner_user_id

    params["search_term"] = search_term

    params["participant_id"] = participant_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/plugins/playbooks/api/v0/runs/channels",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List[str]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(List[str], response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, List[str]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    team_id: str,
    sort: Union[Unset, None, GetChannelsSort] = GetChannelsSort.CREATE_AT,
    direction: Union[Unset, None, GetChannelsDirection] = GetChannelsDirection.DESC,
    status: Union[Unset, None, GetChannelsStatus] = GetChannelsStatus.ALL,
    owner_user_id: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    participant_id: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, List[str]]]:
    """Get playbook run channels

     Get all channels associated with a playbook run, filtered by team, status, owner, name and/or
    members, and sorted by ID, name, status, creation date, end date, team, or owner ID.

    Args:
        team_id (str):
        sort (Union[Unset, None, GetChannelsSort]):  Default: GetChannelsSort.CREATE_AT.
        direction (Union[Unset, None, GetChannelsDirection]):  Default: GetChannelsDirection.DESC.
        status (Union[Unset, None, GetChannelsStatus]):  Default: GetChannelsStatus.ALL.
        owner_user_id (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):
        participant_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List[str]]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        sort=sort,
        direction=direction,
        status=status,
        owner_user_id=owner_user_id,
        search_term=search_term,
        participant_id=participant_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    team_id: str,
    sort: Union[Unset, None, GetChannelsSort] = GetChannelsSort.CREATE_AT,
    direction: Union[Unset, None, GetChannelsDirection] = GetChannelsDirection.DESC,
    status: Union[Unset, None, GetChannelsStatus] = GetChannelsStatus.ALL,
    owner_user_id: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    participant_id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, List[str]]]:
    """Get playbook run channels

     Get all channels associated with a playbook run, filtered by team, status, owner, name and/or
    members, and sorted by ID, name, status, creation date, end date, team, or owner ID.

    Args:
        team_id (str):
        sort (Union[Unset, None, GetChannelsSort]):  Default: GetChannelsSort.CREATE_AT.
        direction (Union[Unset, None, GetChannelsDirection]):  Default: GetChannelsDirection.DESC.
        status (Union[Unset, None, GetChannelsStatus]):  Default: GetChannelsStatus.ALL.
        owner_user_id (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):
        participant_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List[str]]
    """

    return sync_detailed(
        client=client,
        team_id=team_id,
        sort=sort,
        direction=direction,
        status=status,
        owner_user_id=owner_user_id,
        search_term=search_term,
        participant_id=participant_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    team_id: str,
    sort: Union[Unset, None, GetChannelsSort] = GetChannelsSort.CREATE_AT,
    direction: Union[Unset, None, GetChannelsDirection] = GetChannelsDirection.DESC,
    status: Union[Unset, None, GetChannelsStatus] = GetChannelsStatus.ALL,
    owner_user_id: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    participant_id: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, List[str]]]:
    """Get playbook run channels

     Get all channels associated with a playbook run, filtered by team, status, owner, name and/or
    members, and sorted by ID, name, status, creation date, end date, team, or owner ID.

    Args:
        team_id (str):
        sort (Union[Unset, None, GetChannelsSort]):  Default: GetChannelsSort.CREATE_AT.
        direction (Union[Unset, None, GetChannelsDirection]):  Default: GetChannelsDirection.DESC.
        status (Union[Unset, None, GetChannelsStatus]):  Default: GetChannelsStatus.ALL.
        owner_user_id (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):
        participant_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List[str]]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        sort=sort,
        direction=direction,
        status=status,
        owner_user_id=owner_user_id,
        search_term=search_term,
        participant_id=participant_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    team_id: str,
    sort: Union[Unset, None, GetChannelsSort] = GetChannelsSort.CREATE_AT,
    direction: Union[Unset, None, GetChannelsDirection] = GetChannelsDirection.DESC,
    status: Union[Unset, None, GetChannelsStatus] = GetChannelsStatus.ALL,
    owner_user_id: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    participant_id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, List[str]]]:
    """Get playbook run channels

     Get all channels associated with a playbook run, filtered by team, status, owner, name and/or
    members, and sorted by ID, name, status, creation date, end date, team, or owner ID.

    Args:
        team_id (str):
        sort (Union[Unset, None, GetChannelsSort]):  Default: GetChannelsSort.CREATE_AT.
        direction (Union[Unset, None, GetChannelsDirection]):  Default: GetChannelsDirection.DESC.
        status (Union[Unset, None, GetChannelsStatus]):  Default: GetChannelsStatus.ALL.
        owner_user_id (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):
        participant_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List[str]]
    """

    return (
        await asyncio_detailed(
            client=client,
            team_id=team_id,
            sort=sort,
            direction=direction,
            status=status,
            owner_user_id=owner_user_id,
            search_term=search_term,
            participant_id=participant_id,
        )
    ).parsed
