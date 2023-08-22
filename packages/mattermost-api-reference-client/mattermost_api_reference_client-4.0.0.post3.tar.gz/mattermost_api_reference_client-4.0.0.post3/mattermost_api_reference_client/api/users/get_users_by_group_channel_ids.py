from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_users_by_group_channel_ids_response_200 import GetUsersByGroupChannelIdsResponse200
from ...types import Response


def _get_kwargs(
    *,
    json_body: List[str],
) -> Dict[str, Any]:
    pass

    json_json_body = json_body

    return {
        "method": "post",
        "url": "/api/v4/users/group_channels",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetUsersByGroupChannelIdsResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetUsersByGroupChannelIdsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, GetUsersByGroupChannelIdsResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: List[str],
) -> Response[Union[Any, GetUsersByGroupChannelIdsResponse200]]:
    """Get users by group channels ids

     Get an object containing a key per group channel id in the
    query and its value as a list of users members of that group
    channel.

    The user must be a member of the group ids in the query, or
    they will be omitted from the response.
    ##### Permissions
    Requires an active session but no other permissions.

    __Minimum server version__: 5.14

    Args:
        json_body (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetUsersByGroupChannelIdsResponse200]]
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
    json_body: List[str],
) -> Optional[Union[Any, GetUsersByGroupChannelIdsResponse200]]:
    """Get users by group channels ids

     Get an object containing a key per group channel id in the
    query and its value as a list of users members of that group
    channel.

    The user must be a member of the group ids in the query, or
    they will be omitted from the response.
    ##### Permissions
    Requires an active session but no other permissions.

    __Minimum server version__: 5.14

    Args:
        json_body (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetUsersByGroupChannelIdsResponse200]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: List[str],
) -> Response[Union[Any, GetUsersByGroupChannelIdsResponse200]]:
    """Get users by group channels ids

     Get an object containing a key per group channel id in the
    query and its value as a list of users members of that group
    channel.

    The user must be a member of the group ids in the query, or
    they will be omitted from the response.
    ##### Permissions
    Requires an active session but no other permissions.

    __Minimum server version__: 5.14

    Args:
        json_body (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetUsersByGroupChannelIdsResponse200]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: List[str],
) -> Optional[Union[Any, GetUsersByGroupChannelIdsResponse200]]:
    """Get users by group channels ids

     Get an object containing a key per group channel id in the
    query and its value as a list of users members of that group
    channel.

    The user must be a member of the group ids in the query, or
    they will be omitted from the response.
    ##### Permissions
    Requires an active session but no other permissions.

    __Minimum server version__: 5.14

    Args:
        json_body (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetUsersByGroupChannelIdsResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
