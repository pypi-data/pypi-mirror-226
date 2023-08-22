from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_user_json_body import CreateUserJsonBody
from ...models.user import User
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    json_body: CreateUserJsonBody,
    t: Union[Unset, None, str] = UNSET,
    iid: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["t"] = t

    params["iid"] = iid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/users",
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, User]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = User.from_dict(response.json())

        return response_201
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
) -> Response[Union[Any, User]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateUserJsonBody,
    t: Union[Unset, None, str] = UNSET,
    iid: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, User]]:
    """Create a user

     Create a new user on the system. Password is required for email login. For other authentication
    types such as LDAP or SAML, auth_data and auth_service fields are required.
    ##### Permissions
    No permission required for creating email/username accounts on an open server. Auth Token is
    required for other authentication types such as LDAP or SAML.

    Args:
        t (Union[Unset, None, str]):
        iid (Union[Unset, None, str]):
        json_body (CreateUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, User]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        t=t,
        iid=iid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateUserJsonBody,
    t: Union[Unset, None, str] = UNSET,
    iid: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, User]]:
    """Create a user

     Create a new user on the system. Password is required for email login. For other authentication
    types such as LDAP or SAML, auth_data and auth_service fields are required.
    ##### Permissions
    No permission required for creating email/username accounts on an open server. Auth Token is
    required for other authentication types such as LDAP or SAML.

    Args:
        t (Union[Unset, None, str]):
        iid (Union[Unset, None, str]):
        json_body (CreateUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, User]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        t=t,
        iid=iid,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateUserJsonBody,
    t: Union[Unset, None, str] = UNSET,
    iid: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, User]]:
    """Create a user

     Create a new user on the system. Password is required for email login. For other authentication
    types such as LDAP or SAML, auth_data and auth_service fields are required.
    ##### Permissions
    No permission required for creating email/username accounts on an open server. Auth Token is
    required for other authentication types such as LDAP or SAML.

    Args:
        t (Union[Unset, None, str]):
        iid (Union[Unset, None, str]):
        json_body (CreateUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, User]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        t=t,
        iid=iid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateUserJsonBody,
    t: Union[Unset, None, str] = UNSET,
    iid: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, User]]:
    """Create a user

     Create a new user on the system. Password is required for email login. For other authentication
    types such as LDAP or SAML, auth_data and auth_service fields are required.
    ##### Permissions
    No permission required for creating email/username accounts on an open server. Auth Token is
    required for other authentication types such as LDAP or SAML.

    Args:
        t (Union[Unset, None, str]):
        iid (Union[Unset, None, str]):
        json_body (CreateUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, User]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            t=t,
            iid=iid,
        )
    ).parsed
