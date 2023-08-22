from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.config import Config
from ...models.status_ok import StatusOK
from ...types import Response


def _get_kwargs(
    *,
    json_body: Config,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/email/test",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, StatusOK]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = StatusOK.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
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
    json_body: Config,
) -> Response[Union[Any, StatusOK]]:
    """Send a test email

     Send a test email to make sure you have your email settings configured correctly. Optionally provide
    a configuration in the request body to test. If no valid configuration is present in the request
    body the current server configuration will be tested.
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (Config):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
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
) -> Optional[Union[Any, StatusOK]]:
    """Send a test email

     Send a test email to make sure you have your email settings configured correctly. Optionally provide
    a configuration in the request body to test. If no valid configuration is present in the request
    body the current server configuration will be tested.
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (Config):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Config,
) -> Response[Union[Any, StatusOK]]:
    """Send a test email

     Send a test email to make sure you have your email settings configured correctly. Optionally provide
    a configuration in the request body to test. If no valid configuration is present in the request
    body the current server configuration will be tested.
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (Config):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
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
) -> Optional[Union[Any, StatusOK]]:
    """Send a test email

     Send a test email to make sure you have your email settings configured correctly. Optionally provide
    a configuration in the request body to test. If no valid configuration is present in the request
    body the current server configuration will be tested.
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (Config):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
