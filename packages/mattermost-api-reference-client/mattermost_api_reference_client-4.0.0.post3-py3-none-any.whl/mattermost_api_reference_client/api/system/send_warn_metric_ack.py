from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.send_warn_metric_ack_json_body import SendWarnMetricAckJsonBody
from ...models.status_ok import StatusOK
from ...types import Response


def _get_kwargs(
    warn_metric_id: str,
    *,
    json_body: SendWarnMetricAckJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/warn_metrics/ack/{warn_metric_id}".format(
            warn_metric_id=warn_metric_id,
        ),
        "json": json_json_body,
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
    json_body: SendWarnMetricAckJsonBody,
) -> Response[Union[Any, StatusOK]]:
    r"""Acknowledge a warning of a metric status

     Acknowledge a warning for the warn_metric_id metric crossing a threshold (or some
    similar condition being fulfilled) - attempts to send an ack email to
    acknowledge@mattermost.com and sets the \"ack\" status for all the warn metrics in the system.

    __Minimum server version__: 5.26

    ##### Permissions

    Must have `manage_system` permission.

    Args:
        warn_metric_id (str):
        json_body (SendWarnMetricAckJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        warn_metric_id=warn_metric_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    warn_metric_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SendWarnMetricAckJsonBody,
) -> Optional[Union[Any, StatusOK]]:
    r"""Acknowledge a warning of a metric status

     Acknowledge a warning for the warn_metric_id metric crossing a threshold (or some
    similar condition being fulfilled) - attempts to send an ack email to
    acknowledge@mattermost.com and sets the \"ack\" status for all the warn metrics in the system.

    __Minimum server version__: 5.26

    ##### Permissions

    Must have `manage_system` permission.

    Args:
        warn_metric_id (str):
        json_body (SendWarnMetricAckJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        warn_metric_id=warn_metric_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    warn_metric_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SendWarnMetricAckJsonBody,
) -> Response[Union[Any, StatusOK]]:
    r"""Acknowledge a warning of a metric status

     Acknowledge a warning for the warn_metric_id metric crossing a threshold (or some
    similar condition being fulfilled) - attempts to send an ack email to
    acknowledge@mattermost.com and sets the \"ack\" status for all the warn metrics in the system.

    __Minimum server version__: 5.26

    ##### Permissions

    Must have `manage_system` permission.

    Args:
        warn_metric_id (str):
        json_body (SendWarnMetricAckJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        warn_metric_id=warn_metric_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    warn_metric_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SendWarnMetricAckJsonBody,
) -> Optional[Union[Any, StatusOK]]:
    r"""Acknowledge a warning of a metric status

     Acknowledge a warning for the warn_metric_id metric crossing a threshold (or some
    similar condition being fulfilled) - attempts to send an ack email to
    acknowledge@mattermost.com and sets the \"ack\" status for all the warn metrics in the system.

    __Minimum server version__: 5.26

    ##### Permissions

    Must have `manage_system` permission.

    Args:
        warn_metric_id (str):
        json_body (SendWarnMetricAckJsonBody):

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
            json_body=json_body,
        )
    ).parsed
