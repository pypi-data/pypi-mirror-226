from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.switch_account_type_json_body import SwitchAccountTypeJsonBody
from ...models.switch_account_type_response_200 import SwitchAccountTypeResponse200
from ...types import Response


def _get_kwargs(
    *,
    json_body: SwitchAccountTypeJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/users/login/switch",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, SwitchAccountTypeResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SwitchAccountTypeResponse200.from_dict(response.json())

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
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, SwitchAccountTypeResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SwitchAccountTypeJsonBody,
) -> Response[Union[Any, SwitchAccountTypeResponse200]]:
    """Switch login method

     Switch a user's login method from using email to OAuth2/SAML/LDAP or back to email. When switching
    to OAuth2/SAML, account switching is not complete until the user follows the returned link and
    completes any steps on the OAuth2/SAML service provider.

    To switch from email to OAuth2/SAML, specify `current_service`, `new_service`, `email` and
    `password`.

    To switch from OAuth2/SAML to email, specify `current_service`, `new_service`, `email` and
    `new_password`.

    To switch from email to LDAP/AD, specify `current_service`, `new_service`, `email`, `password`,
    `ldap_ip` and `new_password` (this is the user's LDAP password).

    To switch from LDAP/AD to email, specify `current_service`, `new_service`, `ldap_ip`, `password`
    (this is the user's LDAP password), `email`  and `new_password`.

    Additionally, specify `mfa_code` when trying to switch an account on LDAP/AD or email that has MFA
    activated.

    ##### Permissions
    No current authentication required except when switching from OAuth2/SAML to email.

    Args:
        json_body (SwitchAccountTypeJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SwitchAccountTypeResponse200]]
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
    json_body: SwitchAccountTypeJsonBody,
) -> Optional[Union[Any, SwitchAccountTypeResponse200]]:
    """Switch login method

     Switch a user's login method from using email to OAuth2/SAML/LDAP or back to email. When switching
    to OAuth2/SAML, account switching is not complete until the user follows the returned link and
    completes any steps on the OAuth2/SAML service provider.

    To switch from email to OAuth2/SAML, specify `current_service`, `new_service`, `email` and
    `password`.

    To switch from OAuth2/SAML to email, specify `current_service`, `new_service`, `email` and
    `new_password`.

    To switch from email to LDAP/AD, specify `current_service`, `new_service`, `email`, `password`,
    `ldap_ip` and `new_password` (this is the user's LDAP password).

    To switch from LDAP/AD to email, specify `current_service`, `new_service`, `ldap_ip`, `password`
    (this is the user's LDAP password), `email`  and `new_password`.

    Additionally, specify `mfa_code` when trying to switch an account on LDAP/AD or email that has MFA
    activated.

    ##### Permissions
    No current authentication required except when switching from OAuth2/SAML to email.

    Args:
        json_body (SwitchAccountTypeJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SwitchAccountTypeResponse200]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SwitchAccountTypeJsonBody,
) -> Response[Union[Any, SwitchAccountTypeResponse200]]:
    """Switch login method

     Switch a user's login method from using email to OAuth2/SAML/LDAP or back to email. When switching
    to OAuth2/SAML, account switching is not complete until the user follows the returned link and
    completes any steps on the OAuth2/SAML service provider.

    To switch from email to OAuth2/SAML, specify `current_service`, `new_service`, `email` and
    `password`.

    To switch from OAuth2/SAML to email, specify `current_service`, `new_service`, `email` and
    `new_password`.

    To switch from email to LDAP/AD, specify `current_service`, `new_service`, `email`, `password`,
    `ldap_ip` and `new_password` (this is the user's LDAP password).

    To switch from LDAP/AD to email, specify `current_service`, `new_service`, `ldap_ip`, `password`
    (this is the user's LDAP password), `email`  and `new_password`.

    Additionally, specify `mfa_code` when trying to switch an account on LDAP/AD or email that has MFA
    activated.

    ##### Permissions
    No current authentication required except when switching from OAuth2/SAML to email.

    Args:
        json_body (SwitchAccountTypeJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SwitchAccountTypeResponse200]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SwitchAccountTypeJsonBody,
) -> Optional[Union[Any, SwitchAccountTypeResponse200]]:
    """Switch login method

     Switch a user's login method from using email to OAuth2/SAML/LDAP or back to email. When switching
    to OAuth2/SAML, account switching is not complete until the user follows the returned link and
    completes any steps on the OAuth2/SAML service provider.

    To switch from email to OAuth2/SAML, specify `current_service`, `new_service`, `email` and
    `password`.

    To switch from OAuth2/SAML to email, specify `current_service`, `new_service`, `email` and
    `new_password`.

    To switch from email to LDAP/AD, specify `current_service`, `new_service`, `email`, `password`,
    `ldap_ip` and `new_password` (this is the user's LDAP password).

    To switch from LDAP/AD to email, specify `current_service`, `new_service`, `ldap_ip`, `password`
    (this is the user's LDAP password), `email`  and `new_password`.

    Additionally, specify `mfa_code` when trying to switch an account on LDAP/AD or email that has MFA
    activated.

    ##### Permissions
    No current authentication required except when switching from OAuth2/SAML to email.

    Args:
        json_body (SwitchAccountTypeJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SwitchAccountTypeResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
