from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.system import System
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/api/v4/plugins/marketplace/first_admin_visit",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, System]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = System.from_dict(response.json())

        return response_200
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
) -> Response[Union[Any, System]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, System]]:
    """Get if the Plugin Marketplace has been visited by at least an admin.

     Retrieves the status that specifies that at least one System Admin has visited the in-product Plugin
    Marketplace.
    __Minimum server version: 5.33__
    ##### Permissions
    Must have `manage_system` permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, System]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, System]]:
    """Get if the Plugin Marketplace has been visited by at least an admin.

     Retrieves the status that specifies that at least one System Admin has visited the in-product Plugin
    Marketplace.
    __Minimum server version: 5.33__
    ##### Permissions
    Must have `manage_system` permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, System]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, System]]:
    """Get if the Plugin Marketplace has been visited by at least an admin.

     Retrieves the status that specifies that at least one System Admin has visited the in-product Plugin
    Marketplace.
    __Minimum server version: 5.33__
    ##### Permissions
    Must have `manage_system` permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, System]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, System]]:
    """Get if the Plugin Marketplace has been visited by at least an admin.

     Retrieves the status that specifies that at least one System Admin has visited the in-product Plugin
    Marketplace.
    __Minimum server version: 5.33__
    ##### Permissions
    Must have `manage_system` permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, System]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
