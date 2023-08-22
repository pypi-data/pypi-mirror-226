from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.status_ok import StatusOK
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/api/v4/warn_metrics/status",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, StatusOK]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = StatusOK.from_dict(response.json())

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
) -> Response[Union[Any, StatusOK]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, StatusOK]]:
    r"""Get the warn metrics status (enabled or disabled)

     Get the status of a set of metrics (enabled or disabled) from the Systems table.

    The returned JSON contains the metrics that we need to warn the admin on with regard
    to their status (we return the ones whose status is \"true\", which means that they are
    in a \"warnable\" state - e.g. a threshold has been crossed or some other condition has
    been fulfilled).

    __Minimum server version__: 5.26

    ##### Permissions

    Must have `manage_system` permission.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, StatusOK]]:
    r"""Get the warn metrics status (enabled or disabled)

     Get the status of a set of metrics (enabled or disabled) from the Systems table.

    The returned JSON contains the metrics that we need to warn the admin on with regard
    to their status (we return the ones whose status is \"true\", which means that they are
    in a \"warnable\" state - e.g. a threshold has been crossed or some other condition has
    been fulfilled).

    __Minimum server version__: 5.26

    ##### Permissions

    Must have `manage_system` permission.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, StatusOK]]:
    r"""Get the warn metrics status (enabled or disabled)

     Get the status of a set of metrics (enabled or disabled) from the Systems table.

    The returned JSON contains the metrics that we need to warn the admin on with regard
    to their status (we return the ones whose status is \"true\", which means that they are
    in a \"warnable\" state - e.g. a threshold has been crossed or some other condition has
    been fulfilled).

    __Minimum server version__: 5.26

    ##### Permissions

    Must have `manage_system` permission.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, StatusOK]]:
    r"""Get the warn metrics status (enabled or disabled)

     Get the status of a set of metrics (enabled or disabled) from the Systems table.

    The returned JSON contains the metrics that we need to warn the admin on with regard
    to their status (we return the ones whose status is \"true\", which means that they are
    in a \"warnable\" state - e.g. a threshold has been crossed or some other condition has
    been fulfilled).

    __Minimum server version__: 5.26

    ##### Permissions

    Must have `manage_system` permission.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
