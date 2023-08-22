from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_user_access_tokens_json_body import SearchUserAccessTokensJsonBody
from ...models.user_access_token_sanitized import UserAccessTokenSanitized
from ...types import Response


def _get_kwargs(
    *,
    json_body: SearchUserAccessTokensJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/users/tokens/search",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["UserAccessTokenSanitized"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UserAccessTokenSanitized.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["UserAccessTokenSanitized"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchUserAccessTokensJsonBody,
) -> Response[List["UserAccessTokenSanitized"]]:
    """Search tokens

     Get a list of tokens based on search criteria provided in the request body. Searches are done
    against the token id, user id and username.

    __Minimum server version__: 4.7

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (SearchUserAccessTokensJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['UserAccessTokenSanitized']]
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
    json_body: SearchUserAccessTokensJsonBody,
) -> Optional[List["UserAccessTokenSanitized"]]:
    """Search tokens

     Get a list of tokens based on search criteria provided in the request body. Searches are done
    against the token id, user id and username.

    __Minimum server version__: 4.7

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (SearchUserAccessTokensJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['UserAccessTokenSanitized']
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchUserAccessTokensJsonBody,
) -> Response[List["UserAccessTokenSanitized"]]:
    """Search tokens

     Get a list of tokens based on search criteria provided in the request body. Searches are done
    against the token id, user id and username.

    __Minimum server version__: 4.7

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (SearchUserAccessTokensJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['UserAccessTokenSanitized']]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchUserAccessTokensJsonBody,
) -> Optional[List["UserAccessTokenSanitized"]]:
    """Search tokens

     Get a list of tokens based on search criteria provided in the request body. Searches are done
    against the token id, user id and username.

    __Minimum server version__: 4.7

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (SearchUserAccessTokensJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['UserAccessTokenSanitized']
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
