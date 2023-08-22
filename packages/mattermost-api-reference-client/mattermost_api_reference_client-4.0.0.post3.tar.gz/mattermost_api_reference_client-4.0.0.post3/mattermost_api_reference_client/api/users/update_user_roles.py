from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.status_ok import StatusOK
from ...models.update_user_roles_json_body import UpdateUserRolesJsonBody
from ...types import Response


def _get_kwargs(
    user_id: str,
    *,
    json_body: UpdateUserRolesJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/api/v4/users/{user_id}/roles".format(
            user_id=user_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, StatusOK]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = StatusOK.from_dict(response.json())

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
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateUserRolesJsonBody,
) -> Response[Union[Any, StatusOK]]:
    r"""Update a user's roles

     Update a user's system-level roles. Valid user roles are \"system_user\", \"system_admin\" or both
    of them. Overwrites any previously assigned system-level roles.
    ##### Permissions
    Must have the `manage_roles` permission.

    Args:
        user_id (str):
        json_body (UpdateUserRolesJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateUserRolesJsonBody,
) -> Optional[Union[Any, StatusOK]]:
    r"""Update a user's roles

     Update a user's system-level roles. Valid user roles are \"system_user\", \"system_admin\" or both
    of them. Overwrites any previously assigned system-level roles.
    ##### Permissions
    Must have the `manage_roles` permission.

    Args:
        user_id (str):
        json_body (UpdateUserRolesJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateUserRolesJsonBody,
) -> Response[Union[Any, StatusOK]]:
    r"""Update a user's roles

     Update a user's system-level roles. Valid user roles are \"system_user\", \"system_admin\" or both
    of them. Overwrites any previously assigned system-level roles.
    ##### Permissions
    Must have the `manage_roles` permission.

    Args:
        user_id (str):
        json_body (UpdateUserRolesJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateUserRolesJsonBody,
) -> Optional[Union[Any, StatusOK]]:
    r"""Update a user's roles

     Update a user's system-level roles. Valid user roles are \"system_user\", \"system_admin\" or both
    of them. Overwrites any previously assigned system-level roles.
    ##### Permissions
    Must have the `manage_roles` permission.

    Args:
        user_id (str):
        json_body (UpdateUserRolesJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
