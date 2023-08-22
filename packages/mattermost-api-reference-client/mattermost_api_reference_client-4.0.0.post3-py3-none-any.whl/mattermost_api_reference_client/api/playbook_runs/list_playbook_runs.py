from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_playbook_runs_direction import ListPlaybookRunsDirection
from ...models.list_playbook_runs_sort import ListPlaybookRunsSort
from ...models.list_playbook_runs_statuses_item import ListPlaybookRunsStatusesItem
from ...models.playbook_run_list import PlaybookRunList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    team_id: str,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 1000,
    sort: Union[Unset, None, ListPlaybookRunsSort] = ListPlaybookRunsSort.CREATE_AT,
    direction: Union[Unset, None, ListPlaybookRunsDirection] = ListPlaybookRunsDirection.DESC,
    statuses: Union[Unset, None, List[ListPlaybookRunsStatusesItem]] = UNSET,
    owner_user_id: Union[Unset, None, str] = UNSET,
    participant_id: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["team_id"] = team_id

    params["page"] = page

    params["per_page"] = per_page

    json_sort: Union[Unset, None, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value if sort else None

    params["sort"] = json_sort

    json_direction: Union[Unset, None, str] = UNSET
    if not isinstance(direction, Unset):
        json_direction = direction.value if direction else None

    params["direction"] = json_direction

    json_statuses: Union[Unset, None, List[str]] = UNSET
    if not isinstance(statuses, Unset):
        if statuses is None:
            json_statuses = None
        else:
            json_statuses = []
            for statuses_item_data in statuses:
                statuses_item = statuses_item_data.value

                json_statuses.append(statuses_item)

    params["statuses"] = json_statuses

    params["owner_user_id"] = owner_user_id

    params["participant_id"] = participant_id

    params["search_term"] = search_term

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/plugins/playbooks/api/v0/runs",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PlaybookRunList]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PlaybookRunList.from_dict(response.json())

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
) -> Response[Union[Any, PlaybookRunList]]:
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
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 1000,
    sort: Union[Unset, None, ListPlaybookRunsSort] = ListPlaybookRunsSort.CREATE_AT,
    direction: Union[Unset, None, ListPlaybookRunsDirection] = ListPlaybookRunsDirection.DESC,
    statuses: Union[Unset, None, List[ListPlaybookRunsStatusesItem]] = UNSET,
    owner_user_id: Union[Unset, None, str] = UNSET,
    participant_id: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, PlaybookRunList]]:
    """List all playbook runs

     Retrieve a paged list of playbook runs, filtered by team, status, owner, name and/or members, and
    sorted by ID, name, status, creation date, end date, team or owner ID.

    Args:
        team_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 1000.
        sort (Union[Unset, None, ListPlaybookRunsSort]):  Default: ListPlaybookRunsSort.CREATE_AT.
        direction (Union[Unset, None, ListPlaybookRunsDirection]):  Default:
            ListPlaybookRunsDirection.DESC.
        statuses (Union[Unset, None, List[ListPlaybookRunsStatusesItem]]):
        owner_user_id (Union[Unset, None, str]):
        participant_id (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlaybookRunList]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        page=page,
        per_page=per_page,
        sort=sort,
        direction=direction,
        statuses=statuses,
        owner_user_id=owner_user_id,
        participant_id=participant_id,
        search_term=search_term,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    team_id: str,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 1000,
    sort: Union[Unset, None, ListPlaybookRunsSort] = ListPlaybookRunsSort.CREATE_AT,
    direction: Union[Unset, None, ListPlaybookRunsDirection] = ListPlaybookRunsDirection.DESC,
    statuses: Union[Unset, None, List[ListPlaybookRunsStatusesItem]] = UNSET,
    owner_user_id: Union[Unset, None, str] = UNSET,
    participant_id: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, PlaybookRunList]]:
    """List all playbook runs

     Retrieve a paged list of playbook runs, filtered by team, status, owner, name and/or members, and
    sorted by ID, name, status, creation date, end date, team or owner ID.

    Args:
        team_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 1000.
        sort (Union[Unset, None, ListPlaybookRunsSort]):  Default: ListPlaybookRunsSort.CREATE_AT.
        direction (Union[Unset, None, ListPlaybookRunsDirection]):  Default:
            ListPlaybookRunsDirection.DESC.
        statuses (Union[Unset, None, List[ListPlaybookRunsStatusesItem]]):
        owner_user_id (Union[Unset, None, str]):
        participant_id (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlaybookRunList]
    """

    return sync_detailed(
        client=client,
        team_id=team_id,
        page=page,
        per_page=per_page,
        sort=sort,
        direction=direction,
        statuses=statuses,
        owner_user_id=owner_user_id,
        participant_id=participant_id,
        search_term=search_term,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    team_id: str,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 1000,
    sort: Union[Unset, None, ListPlaybookRunsSort] = ListPlaybookRunsSort.CREATE_AT,
    direction: Union[Unset, None, ListPlaybookRunsDirection] = ListPlaybookRunsDirection.DESC,
    statuses: Union[Unset, None, List[ListPlaybookRunsStatusesItem]] = UNSET,
    owner_user_id: Union[Unset, None, str] = UNSET,
    participant_id: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, PlaybookRunList]]:
    """List all playbook runs

     Retrieve a paged list of playbook runs, filtered by team, status, owner, name and/or members, and
    sorted by ID, name, status, creation date, end date, team or owner ID.

    Args:
        team_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 1000.
        sort (Union[Unset, None, ListPlaybookRunsSort]):  Default: ListPlaybookRunsSort.CREATE_AT.
        direction (Union[Unset, None, ListPlaybookRunsDirection]):  Default:
            ListPlaybookRunsDirection.DESC.
        statuses (Union[Unset, None, List[ListPlaybookRunsStatusesItem]]):
        owner_user_id (Union[Unset, None, str]):
        participant_id (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlaybookRunList]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        page=page,
        per_page=per_page,
        sort=sort,
        direction=direction,
        statuses=statuses,
        owner_user_id=owner_user_id,
        participant_id=participant_id,
        search_term=search_term,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    team_id: str,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 1000,
    sort: Union[Unset, None, ListPlaybookRunsSort] = ListPlaybookRunsSort.CREATE_AT,
    direction: Union[Unset, None, ListPlaybookRunsDirection] = ListPlaybookRunsDirection.DESC,
    statuses: Union[Unset, None, List[ListPlaybookRunsStatusesItem]] = UNSET,
    owner_user_id: Union[Unset, None, str] = UNSET,
    participant_id: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, PlaybookRunList]]:
    """List all playbook runs

     Retrieve a paged list of playbook runs, filtered by team, status, owner, name and/or members, and
    sorted by ID, name, status, creation date, end date, team or owner ID.

    Args:
        team_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 1000.
        sort (Union[Unset, None, ListPlaybookRunsSort]):  Default: ListPlaybookRunsSort.CREATE_AT.
        direction (Union[Unset, None, ListPlaybookRunsDirection]):  Default:
            ListPlaybookRunsDirection.DESC.
        statuses (Union[Unset, None, List[ListPlaybookRunsStatusesItem]]):
        owner_user_id (Union[Unset, None, str]):
        participant_id (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlaybookRunList]
    """

    return (
        await asyncio_detailed(
            client=client,
            team_id=team_id,
            page=page,
            per_page=per_page,
            sort=sort,
            direction=direction,
            statuses=statuses,
            owner_user_id=owner_user_id,
            participant_id=participant_id,
            search_term=search_term,
        )
    ).parsed
