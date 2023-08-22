from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.scheme import Scheme
from ...types import Response


def _get_kwargs(
    scheme_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/api/v4/schemes/{scheme_id}".format(
            scheme_id=scheme_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Scheme]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Scheme.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
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
) -> Response[Union[Any, Scheme]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scheme_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Scheme]]:
    """Get a scheme

     Get a scheme from the provided scheme id.

    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.0

    Args:
        scheme_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Scheme]]
    """

    kwargs = _get_kwargs(
        scheme_id=scheme_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    scheme_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Scheme]]:
    """Get a scheme

     Get a scheme from the provided scheme id.

    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.0

    Args:
        scheme_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Scheme]
    """

    return sync_detailed(
        scheme_id=scheme_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    scheme_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Scheme]]:
    """Get a scheme

     Get a scheme from the provided scheme id.

    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.0

    Args:
        scheme_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Scheme]]
    """

    kwargs = _get_kwargs(
        scheme_id=scheme_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scheme_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Scheme]]:
    """Get a scheme

     Get a scheme from the provided scheme id.

    ##### Permissions
    Must have `manage_system` permission.

    __Minimum server version__: 5.0

    Args:
        scheme_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Scheme]
    """

    return (
        await asyncio_detailed(
            scheme_id=scheme_id,
            client=client,
        )
    ).parsed
