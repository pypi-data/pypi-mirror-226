from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.user import User
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    json_body: List[str],
    since: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["since"] = since

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body

    return {
        "method": "post",
        "url": "/api/v4/users/ids",
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["User"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = User.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[Any, List["User"]]]:
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
    since: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, List["User"]]]:
    """Get users by ids

     Get a list of users based on a provided list of user ids.
    ##### Permissions
    Requires an active session but no other permissions.

    Args:
        since (Union[Unset, None, int]):
        json_body (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['User']]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        since=since,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: List[str],
    since: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, List["User"]]]:
    """Get users by ids

     Get a list of users based on a provided list of user ids.
    ##### Permissions
    Requires an active session but no other permissions.

    Args:
        since (Union[Unset, None, int]):
        json_body (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['User']]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        since=since,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: List[str],
    since: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, List["User"]]]:
    """Get users by ids

     Get a list of users based on a provided list of user ids.
    ##### Permissions
    Requires an active session but no other permissions.

    Args:
        since (Union[Unset, None, int]):
        json_body (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['User']]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        since=since,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: List[str],
    since: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, List["User"]]]:
    """Get users by ids

     Get a list of users based on a provided list of user ids.
    ##### Permissions
    Requires an active session but no other permissions.

    Args:
        since (Union[Unset, None, int]):
        json_body (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['User']]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            since=since,
        )
    ).parsed
