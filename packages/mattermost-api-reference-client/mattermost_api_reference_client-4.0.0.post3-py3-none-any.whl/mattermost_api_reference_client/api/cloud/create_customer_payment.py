from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.payment_setup_intent import PaymentSetupIntent
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    pass

    return {
        "method": "post",
        "url": "/api/v4/cloud/payment",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PaymentSetupIntent]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = PaymentSetupIntent.from_dict(response.json())

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
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, PaymentSetupIntent]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, PaymentSetupIntent]]:
    """Create a customer setup payment intent

     Creates a customer setup payment intent for the given Mattermost cloud installation.

    ##### Permissions

    Must have `manage_system` permission and be licensed for Cloud.

    __Minimum server version__: 5.28
    __Note:__: This is intended for internal use and is subject to change.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PaymentSetupIntent]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, PaymentSetupIntent]]:
    """Create a customer setup payment intent

     Creates a customer setup payment intent for the given Mattermost cloud installation.

    ##### Permissions

    Must have `manage_system` permission and be licensed for Cloud.

    __Minimum server version__: 5.28
    __Note:__: This is intended for internal use and is subject to change.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PaymentSetupIntent]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, PaymentSetupIntent]]:
    """Create a customer setup payment intent

     Creates a customer setup payment intent for the given Mattermost cloud installation.

    ##### Permissions

    Must have `manage_system` permission and be licensed for Cloud.

    __Minimum server version__: 5.28
    __Note:__: This is intended for internal use and is subject to change.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PaymentSetupIntent]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, PaymentSetupIntent]]:
    """Create a customer setup payment intent

     Creates a customer setup payment intent for the given Mattermost cloud installation.

    ##### Permissions

    Must have `manage_system` permission and be licensed for Cloud.

    __Minimum server version__: 5.28
    __Note:__: This is intended for internal use and is subject to change.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PaymentSetupIntent]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
