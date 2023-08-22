from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.push_notification import PushNotification
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    pass

    return {
        "method": "post",
        "url": "/api/v4/upgrade_to_enterprise",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PushNotification]]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = PushNotification.from_dict(response.json())

        return response_202
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        response_429 = cast(Any, None)
        return response_429
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, PushNotification]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, PushNotification]]:
    """Executes an inplace upgrade from Team Edition to Enterprise Edition

     It downloads the Mattermost Enterprise Edition of your current version and replace your current
    version with it. After the upgrade you need to restart the Mattermost server.
    __Minimum server version__: 5.27
    ##### Permissions
    Must have `manage_system` permission.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PushNotification]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, PushNotification]]:
    """Executes an inplace upgrade from Team Edition to Enterprise Edition

     It downloads the Mattermost Enterprise Edition of your current version and replace your current
    version with it. After the upgrade you need to restart the Mattermost server.
    __Minimum server version__: 5.27
    ##### Permissions
    Must have `manage_system` permission.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PushNotification]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, PushNotification]]:
    """Executes an inplace upgrade from Team Edition to Enterprise Edition

     It downloads the Mattermost Enterprise Edition of your current version and replace your current
    version with it. After the upgrade you need to restart the Mattermost server.
    __Minimum server version__: 5.27
    ##### Permissions
    Must have `manage_system` permission.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PushNotification]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, PushNotification]]:
    """Executes an inplace upgrade from Team Edition to Enterprise Edition

     It downloads the Mattermost Enterprise Edition of your current version and replace your current
    version with it. After the upgrade you need to restart the Mattermost server.
    __Minimum server version__: 5.27
    ##### Permissions
    Must have `manage_system` permission.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PushNotification]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
