from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.config import Config
from ...types import Response


def _get_kwargs(
    *,
    json_body: Config,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/api/v4/config",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Config]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Config.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Config]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Config,
) -> Response[Union[Any, Config]]:
    """Update configuration

     Submit a new configuration for the server to use. As of server version 4.8, the
    `PluginSettings.EnableUploads` setting cannot be modified by this endpoint.
    Note that the parameters that aren't set in the configuration that you provide will be reset to
    default values. Therefore, if you want to change a configuration parameter and leave the other ones
    unchanged, you need to get the existing configuration first, change the field that you want, then
    put that new configuration.
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (Config):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Config]]
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
    json_body: Config,
) -> Optional[Union[Any, Config]]:
    """Update configuration

     Submit a new configuration for the server to use. As of server version 4.8, the
    `PluginSettings.EnableUploads` setting cannot be modified by this endpoint.
    Note that the parameters that aren't set in the configuration that you provide will be reset to
    default values. Therefore, if you want to change a configuration parameter and leave the other ones
    unchanged, you need to get the existing configuration first, change the field that you want, then
    put that new configuration.
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (Config):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Config]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Config,
) -> Response[Union[Any, Config]]:
    """Update configuration

     Submit a new configuration for the server to use. As of server version 4.8, the
    `PluginSettings.EnableUploads` setting cannot be modified by this endpoint.
    Note that the parameters that aren't set in the configuration that you provide will be reset to
    default values. Therefore, if you want to change a configuration parameter and leave the other ones
    unchanged, you need to get the existing configuration first, change the field that you want, then
    put that new configuration.
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (Config):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Config]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Config,
) -> Optional[Union[Any, Config]]:
    """Update configuration

     Submit a new configuration for the server to use. As of server version 4.8, the
    `PluginSettings.EnableUploads` setting cannot be modified by this endpoint.
    Note that the parameters that aren't set in the configuration that you provide will be reset to
    default values. Therefore, if you want to change a configuration parameter and leave the other ones
    unchanged, you need to get the existing configuration first, change the field that you want, then
    put that new configuration.
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (Config):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Config]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
