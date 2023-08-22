from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.app_error import AppError
from ...types import UNSET, Response


def _get_kwargs(
    file_id: str,
    *,
    h: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["h"] = h

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/files/{file_id}/public".format(
            file_id=file_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, AppError]]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = AppError.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, AppError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    h: str,
) -> Response[Union[Any, AppError]]:
    """Get a public file

     ##### Permissions
    No permissions required.

    Args:
        file_id (str):
        h (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, AppError]]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
        h=h,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    h: str,
) -> Optional[Union[Any, AppError]]:
    """Get a public file

     ##### Permissions
    No permissions required.

    Args:
        file_id (str):
        h (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, AppError]
    """

    return sync_detailed(
        file_id=file_id,
        client=client,
        h=h,
    ).parsed


async def asyncio_detailed(
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    h: str,
) -> Response[Union[Any, AppError]]:
    """Get a public file

     ##### Permissions
    No permissions required.

    Args:
        file_id (str):
        h (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, AppError]]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
        h=h,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    h: str,
) -> Optional[Union[Any, AppError]]:
    """Get a public file

     ##### Permissions
    No permissions required.

    Args:
        file_id (str):
        h (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, AppError]
    """

    return (
        await asyncio_detailed(
            file_id=file_id,
            client=client,
            h=h,
        )
    ).parsed
