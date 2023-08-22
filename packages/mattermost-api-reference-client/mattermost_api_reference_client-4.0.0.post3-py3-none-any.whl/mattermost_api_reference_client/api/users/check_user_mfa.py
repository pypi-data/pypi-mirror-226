from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.check_user_mfa_json_body import CheckUserMfaJsonBody
from ...models.check_user_mfa_response_200 import CheckUserMfaResponse200
from ...types import Response


def _get_kwargs(
    *,
    json_body: CheckUserMfaJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/users/mfa",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, CheckUserMfaResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CheckUserMfaResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, CheckUserMfaResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CheckUserMfaJsonBody,
) -> Response[Union[Any, CheckUserMfaResponse200]]:
    """Check MFA

     Check if a user has multi-factor authentication active on their account by providing a login id.
    Used to check whether an MFA code needs to be provided when logging in.
    ##### Permissions
    No permission required.

    Args:
        json_body (CheckUserMfaJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CheckUserMfaResponse200]]
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
    json_body: CheckUserMfaJsonBody,
) -> Optional[Union[Any, CheckUserMfaResponse200]]:
    """Check MFA

     Check if a user has multi-factor authentication active on their account by providing a login id.
    Used to check whether an MFA code needs to be provided when logging in.
    ##### Permissions
    No permission required.

    Args:
        json_body (CheckUserMfaJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CheckUserMfaResponse200]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CheckUserMfaJsonBody,
) -> Response[Union[Any, CheckUserMfaResponse200]]:
    """Check MFA

     Check if a user has multi-factor authentication active on their account by providing a login id.
    Used to check whether an MFA code needs to be provided when logging in.
    ##### Permissions
    No permission required.

    Args:
        json_body (CheckUserMfaJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CheckUserMfaResponse200]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CheckUserMfaJsonBody,
) -> Optional[Union[Any, CheckUserMfaResponse200]]:
    """Check MFA

     Check if a user has multi-factor authentication active on their account by providing a login id.
    Used to check whether an MFA code needs to be provided when logging in.
    ##### Permissions
    No permission required.

    Args:
        json_body (CheckUserMfaJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CheckUserMfaResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
