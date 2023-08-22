from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.outgoing_webhook import OutgoingWebhook
from ...models.update_outgoing_webhook_json_body import UpdateOutgoingWebhookJsonBody
from ...types import Response


def _get_kwargs(
    hook_id: str,
    *,
    json_body: UpdateOutgoingWebhookJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/api/v4/hooks/outgoing/{hook_id}".format(
            hook_id=hook_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, OutgoingWebhook]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = OutgoingWebhook.from_dict(response.json())

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
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, OutgoingWebhook]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    hook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateOutgoingWebhookJsonBody,
) -> Response[Union[Any, OutgoingWebhook]]:
    """Update an outgoing webhook

     Update an outgoing webhook given the hook id.
    ##### Permissions
    `manage_webhooks` for system or `manage_webhooks` for the specific team or `manage_webhooks` for the
    channel.

    Args:
        hook_id (str):
        json_body (UpdateOutgoingWebhookJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OutgoingWebhook]]
    """

    kwargs = _get_kwargs(
        hook_id=hook_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    hook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateOutgoingWebhookJsonBody,
) -> Optional[Union[Any, OutgoingWebhook]]:
    """Update an outgoing webhook

     Update an outgoing webhook given the hook id.
    ##### Permissions
    `manage_webhooks` for system or `manage_webhooks` for the specific team or `manage_webhooks` for the
    channel.

    Args:
        hook_id (str):
        json_body (UpdateOutgoingWebhookJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OutgoingWebhook]
    """

    return sync_detailed(
        hook_id=hook_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    hook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateOutgoingWebhookJsonBody,
) -> Response[Union[Any, OutgoingWebhook]]:
    """Update an outgoing webhook

     Update an outgoing webhook given the hook id.
    ##### Permissions
    `manage_webhooks` for system or `manage_webhooks` for the specific team or `manage_webhooks` for the
    channel.

    Args:
        hook_id (str):
        json_body (UpdateOutgoingWebhookJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OutgoingWebhook]]
    """

    kwargs = _get_kwargs(
        hook_id=hook_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    hook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateOutgoingWebhookJsonBody,
) -> Optional[Union[Any, OutgoingWebhook]]:
    """Update an outgoing webhook

     Update an outgoing webhook given the hook id.
    ##### Permissions
    `manage_webhooks` for system or `manage_webhooks` for the specific team or `manage_webhooks` for the
    channel.

    Args:
        hook_id (str):
        json_body (UpdateOutgoingWebhookJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OutgoingWebhook]
    """

    return (
        await asyncio_detailed(
            hook_id=hook_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
