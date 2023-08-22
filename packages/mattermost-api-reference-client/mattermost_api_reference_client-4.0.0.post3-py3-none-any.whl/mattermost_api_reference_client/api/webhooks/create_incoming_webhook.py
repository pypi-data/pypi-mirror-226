from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_incoming_webhook_json_body import CreateIncomingWebhookJsonBody
from ...models.incoming_webhook import IncomingWebhook
from ...types import Response


def _get_kwargs(
    *,
    json_body: CreateIncomingWebhookJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/hooks/incoming",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, IncomingWebhook]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = IncomingWebhook.from_dict(response.json())

        return response_201
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
) -> Response[Union[Any, IncomingWebhook]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateIncomingWebhookJsonBody,
) -> Response[Union[Any, IncomingWebhook]]:
    """Create an incoming webhook

     Create an incoming webhook for a channel.
    ##### Permissions
    `manage_webhooks` for the team the webhook is in.

    `manage_others_incoming_webhooks` for the team the webhook is in if the user is different than the
    requester.

    Args:
        json_body (CreateIncomingWebhookJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, IncomingWebhook]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateIncomingWebhookJsonBody,
) -> Optional[Union[Any, IncomingWebhook]]:
    """Create an incoming webhook

     Create an incoming webhook for a channel.
    ##### Permissions
    `manage_webhooks` for the team the webhook is in.

    `manage_others_incoming_webhooks` for the team the webhook is in if the user is different than the
    requester.

    Args:
        json_body (CreateIncomingWebhookJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, IncomingWebhook]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateIncomingWebhookJsonBody,
) -> Response[Union[Any, IncomingWebhook]]:
    """Create an incoming webhook

     Create an incoming webhook for a channel.
    ##### Permissions
    `manage_webhooks` for the team the webhook is in.

    `manage_others_incoming_webhooks` for the team the webhook is in if the user is different than the
    requester.

    Args:
        json_body (CreateIncomingWebhookJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, IncomingWebhook]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateIncomingWebhookJsonBody,
) -> Optional[Union[Any, IncomingWebhook]]:
    """Create an incoming webhook

     Create an incoming webhook for a channel.
    ##### Permissions
    `manage_webhooks` for the team the webhook is in.

    `manage_others_incoming_webhooks` for the team the webhook is in if the user is different than the
    requester.

    Args:
        json_body (CreateIncomingWebhookJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, IncomingWebhook]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
