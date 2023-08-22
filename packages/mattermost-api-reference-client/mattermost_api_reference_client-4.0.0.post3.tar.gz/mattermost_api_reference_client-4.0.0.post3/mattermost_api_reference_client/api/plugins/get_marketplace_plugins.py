from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    server_version: Union[Unset, None, str] = UNSET,
    local_only: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["per_page"] = per_page

    params["filter"] = filter_

    params["server_version"] = server_version

    params["local_only"] = local_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/plugins/marketplace",
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if response.status_code == HTTPStatus.FORBIDDEN:
        return None
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    server_version: Union[Unset, None, str] = UNSET,
    local_only: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Gets all the marketplace plugins

     Gets all plugins from the marketplace server, merging data from locally installed plugins as well as
    prepackaged plugins shipped with the server.

    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.16

    Args:
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        filter_ (Union[Unset, None, str]):
        server_version (Union[Unset, None, str]):
        local_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        filter_=filter_,
        server_version=server_version,
        local_only=local_only,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    server_version: Union[Unset, None, str] = UNSET,
    local_only: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Gets all the marketplace plugins

     Gets all plugins from the marketplace server, merging data from locally installed plugins as well as
    prepackaged plugins shipped with the server.

    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.16

    Args:
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        filter_ (Union[Unset, None, str]):
        server_version (Union[Unset, None, str]):
        local_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        filter_=filter_,
        server_version=server_version,
        local_only=local_only,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
