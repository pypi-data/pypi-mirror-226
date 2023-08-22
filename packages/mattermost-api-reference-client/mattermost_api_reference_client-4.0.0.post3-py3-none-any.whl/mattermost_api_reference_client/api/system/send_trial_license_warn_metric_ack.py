from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.status_ok import StatusOK
from ...types import Response


def _get_kwargs(
    warn_metric_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "post",
        "url": "/api/v4/warn_metrics/trial-license-ack/{warn_metric_id}".format(
            warn_metric_id=warn_metric_id,
        ),
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
    warn_metric_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, StatusOK]]:
    r"""Request trial license and acknowledge a warning of a metric status

     Request a trial license and acknowledge a warning for the warn_metric_id metric crossing a threshold
    (or some
    similar condition being fulfilled) - sets the \"ack\" status for all the warn metrics in the system.

    __Minimum server version__: 5.28

    ##### Permissions

    Must have `manage_system` permission.

    Args:
        warn_metric_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        warn_metric_id=warn_metric_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    warn_metric_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, StatusOK]]:
    r"""Request trial license and acknowledge a warning of a metric status

     Request a trial license and acknowledge a warning for the warn_metric_id metric crossing a threshold
    (or some
    similar condition being fulfilled) - sets the \"ack\" status for all the warn metrics in the system.

    __Minimum server version__: 5.28

    ##### Permissions

    Must have `manage_system` permission.

    Args:
        warn_metric_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        warn_metric_id=warn_metric_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    warn_metric_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, StatusOK]]:
    r"""Request trial license and acknowledge a warning of a metric status

     Request a trial license and acknowledge a warning for the warn_metric_id metric crossing a threshold
    (or some
    similar condition being fulfilled) - sets the \"ack\" status for all the warn metrics in the system.

    __Minimum server version__: 5.28

    ##### Permissions

    Must have `manage_system` permission.

    Args:
        warn_metric_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        warn_metric_id=warn_metric_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    warn_metric_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, StatusOK]]:
    r"""Request trial license and acknowledge a warning of a metric status

     Request a trial license and acknowledge a warning for the warn_metric_id metric crossing a threshold
    (or some
    similar condition being fulfilled) - sets the \"ack\" status for all the warn metrics in the system.

    __Minimum server version__: 5.28

    ##### Permissions

    Must have `manage_system` permission.

    Args:
        warn_metric_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            warn_metric_id=warn_metric_id,
            client=client,
        )
    ).parsed
