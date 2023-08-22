from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.user_threads import UserThreads
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    team_id: str,
    *,
    since: Union[Unset, None, int] = UNSET,
    deleted: Union[Unset, None, bool] = False,
    extended: Union[Unset, None, bool] = False,
    page: Union[Unset, None, int] = 0,
    page_size: Union[Unset, None, int] = 30,
    totals_only: Union[Unset, None, bool] = False,
    threads_only: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["since"] = since

    params["deleted"] = deleted

    params["extended"] = extended

    params["page"] = page

    params["pageSize"] = page_size

    params["totalsOnly"] = totals_only

    params["threadsOnly"] = threads_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/users/{user_id}/teams/{team_id}/threads".format(
            user_id=user_id,
            team_id=team_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, UserThreads]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UserThreads.from_dict(response.json())

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
) -> Response[Union[Any, UserThreads]]:
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
    since: Union[Unset, None, int] = UNSET,
    deleted: Union[Unset, None, bool] = False,
    extended: Union[Unset, None, bool] = False,
    page: Union[Unset, None, int] = 0,
    page_size: Union[Unset, None, int] = 30,
    totals_only: Union[Unset, None, bool] = False,
    threads_only: Union[Unset, None, bool] = False,
) -> Response[Union[Any, UserThreads]]:
    """Get all threads that user is following

     Get all threads that user is following

    __Minimum server version__: 5.29

    ##### Permissions
    Must be logged in as the user or have `edit_other_users` permission.

    Args:
        user_id (str):
        team_id (str):
        since (Union[Unset, None, int]):
        deleted (Union[Unset, None, bool]):
        extended (Union[Unset, None, bool]):
        page (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):  Default: 30.
        totals_only (Union[Unset, None, bool]):
        threads_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UserThreads]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        team_id=team_id,
        since=since,
        deleted=deleted,
        extended=extended,
        page=page,
        page_size=page_size,
        totals_only=totals_only,
        threads_only=threads_only,
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
    since: Union[Unset, None, int] = UNSET,
    deleted: Union[Unset, None, bool] = False,
    extended: Union[Unset, None, bool] = False,
    page: Union[Unset, None, int] = 0,
    page_size: Union[Unset, None, int] = 30,
    totals_only: Union[Unset, None, bool] = False,
    threads_only: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, UserThreads]]:
    """Get all threads that user is following

     Get all threads that user is following

    __Minimum server version__: 5.29

    ##### Permissions
    Must be logged in as the user or have `edit_other_users` permission.

    Args:
        user_id (str):
        team_id (str):
        since (Union[Unset, None, int]):
        deleted (Union[Unset, None, bool]):
        extended (Union[Unset, None, bool]):
        page (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):  Default: 30.
        totals_only (Union[Unset, None, bool]):
        threads_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UserThreads]
    """

    return sync_detailed(
        user_id=user_id,
        team_id=team_id,
        client=client,
        since=since,
        deleted=deleted,
        extended=extended,
        page=page,
        page_size=page_size,
        totals_only=totals_only,
        threads_only=threads_only,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, None, int] = UNSET,
    deleted: Union[Unset, None, bool] = False,
    extended: Union[Unset, None, bool] = False,
    page: Union[Unset, None, int] = 0,
    page_size: Union[Unset, None, int] = 30,
    totals_only: Union[Unset, None, bool] = False,
    threads_only: Union[Unset, None, bool] = False,
) -> Response[Union[Any, UserThreads]]:
    """Get all threads that user is following

     Get all threads that user is following

    __Minimum server version__: 5.29

    ##### Permissions
    Must be logged in as the user or have `edit_other_users` permission.

    Args:
        user_id (str):
        team_id (str):
        since (Union[Unset, None, int]):
        deleted (Union[Unset, None, bool]):
        extended (Union[Unset, None, bool]):
        page (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):  Default: 30.
        totals_only (Union[Unset, None, bool]):
        threads_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UserThreads]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        team_id=team_id,
        since=since,
        deleted=deleted,
        extended=extended,
        page=page,
        page_size=page_size,
        totals_only=totals_only,
        threads_only=threads_only,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, None, int] = UNSET,
    deleted: Union[Unset, None, bool] = False,
    extended: Union[Unset, None, bool] = False,
    page: Union[Unset, None, int] = 0,
    page_size: Union[Unset, None, int] = 30,
    totals_only: Union[Unset, None, bool] = False,
    threads_only: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, UserThreads]]:
    """Get all threads that user is following

     Get all threads that user is following

    __Minimum server version__: 5.29

    ##### Permissions
    Must be logged in as the user or have `edit_other_users` permission.

    Args:
        user_id (str):
        team_id (str):
        since (Union[Unset, None, int]):
        deleted (Union[Unset, None, bool]):
        extended (Union[Unset, None, bool]):
        page (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):  Default: 30.
        totals_only (Union[Unset, None, bool]):
        threads_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UserThreads]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            team_id=team_id,
            client=client,
            since=since,
            deleted=deleted,
            extended=extended,
            page=page,
            page_size=page_size,
            totals_only=totals_only,
            threads_only=threads_only,
        )
    ).parsed
