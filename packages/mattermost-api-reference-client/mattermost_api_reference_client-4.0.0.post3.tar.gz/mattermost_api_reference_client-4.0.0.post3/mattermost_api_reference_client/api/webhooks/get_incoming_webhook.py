from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.incoming_webhook import IncomingWebhook
from ...types import Response


def _get_kwargs(
    hook_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/api/v4/hooks/incoming/{hook_id}".format(
            hook_id=hook_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, IncomingWebhook]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = IncomingWebhook.from_dict(response.json())

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
) -> Response[Union[Any, IncomingWebhook]]:
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
) -> Response[Union[Any, IncomingWebhook]]:
    """Get an incoming webhook

     Get an incoming webhook given the hook id.
    ##### Permissions
    `manage_webhooks` for system or `manage_webhooks` for the specific team or `manage_webhooks` for the
    channel.

    Args:
        hook_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, IncomingWebhook]]
    """

    kwargs = _get_kwargs(
        hook_id=hook_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    hook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, IncomingWebhook]]:
    """Get an incoming webhook

     Get an incoming webhook given the hook id.
    ##### Permissions
    `manage_webhooks` for system or `manage_webhooks` for the specific team or `manage_webhooks` for the
    channel.

    Args:
        hook_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, IncomingWebhook]
    """

    return sync_detailed(
        hook_id=hook_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    hook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, IncomingWebhook]]:
    """Get an incoming webhook

     Get an incoming webhook given the hook id.
    ##### Permissions
    `manage_webhooks` for system or `manage_webhooks` for the specific team or `manage_webhooks` for the
    channel.

    Args:
        hook_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, IncomingWebhook]]
    """

    kwargs = _get_kwargs(
        hook_id=hook_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    hook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, IncomingWebhook]]:
    """Get an incoming webhook

     Get an incoming webhook given the hook id.
    ##### Permissions
    `manage_webhooks` for system or `manage_webhooks` for the specific team or `manage_webhooks` for the
    channel.

    Args:
        hook_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, IncomingWebhook]
    """

    return (
        await asyncio_detailed(
            hook_id=hook_id,
            client=client,
        )
    ).parsed
