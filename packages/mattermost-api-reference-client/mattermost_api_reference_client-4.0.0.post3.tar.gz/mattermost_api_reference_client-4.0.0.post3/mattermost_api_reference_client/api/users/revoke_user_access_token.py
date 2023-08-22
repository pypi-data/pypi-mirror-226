from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.revoke_user_access_token_json_body import RevokeUserAccessTokenJsonBody
from ...models.status_ok import StatusOK
from ...types import Response


def _get_kwargs(
    *,
    json_body: RevokeUserAccessTokenJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/users/tokens/revoke",
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
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RevokeUserAccessTokenJsonBody,
) -> Response[Union[Any, StatusOK]]:
    """Revoke a user access token

     Revoke a user access token and delete any sessions using the token.

    __Minimum server version__: 4.1

    ##### Permissions
    Must have `revoke_user_access_token` permission. For non-self requests, must also have the
    `edit_other_users` permission.

    Args:
        json_body (RevokeUserAccessTokenJsonBody):

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
    json_body: RevokeUserAccessTokenJsonBody,
) -> Optional[Union[Any, StatusOK]]:
    """Revoke a user access token

     Revoke a user access token and delete any sessions using the token.

    __Minimum server version__: 4.1

    ##### Permissions
    Must have `revoke_user_access_token` permission. For non-self requests, must also have the
    `edit_other_users` permission.

    Args:
        json_body (RevokeUserAccessTokenJsonBody):

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
    json_body: RevokeUserAccessTokenJsonBody,
) -> Response[Union[Any, StatusOK]]:
    """Revoke a user access token

     Revoke a user access token and delete any sessions using the token.

    __Minimum server version__: 4.1

    ##### Permissions
    Must have `revoke_user_access_token` permission. For non-self requests, must also have the
    `edit_other_users` permission.

    Args:
        json_body (RevokeUserAccessTokenJsonBody):

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
    json_body: RevokeUserAccessTokenJsonBody,
) -> Optional[Union[Any, StatusOK]]:
    """Revoke a user access token

     Revoke a user access token and delete any sessions using the token.

    __Minimum server version__: 4.1

    ##### Permissions
    Must have `revoke_user_access_token` permission. For non-self requests, must also have the
    `edit_other_users` permission.

    Args:
        json_body (RevokeUserAccessTokenJsonBody):

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
