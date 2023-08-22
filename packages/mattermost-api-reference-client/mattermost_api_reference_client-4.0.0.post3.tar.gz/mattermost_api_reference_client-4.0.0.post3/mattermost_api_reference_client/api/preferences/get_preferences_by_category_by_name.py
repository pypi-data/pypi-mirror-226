from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.preference import Preference
from ...types import Response


def _get_kwargs(
    user_id: str,
    category: str,
    preference_name: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/api/v4/users/{user_id}/preferences/{category}/name/{preference_name}".format(
            user_id=user_id,
            category=category,
            preference_name=preference_name,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Preference]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Preference.from_dict(response.json())

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
) -> Response[Union[Any, Preference]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    category: str,
    preference_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Preference]]:
    """Get a specific user preference

     Gets a single preference for the current user with the given category and name.
    ##### Permissions
    Must be logged in as the user being updated or have the `edit_other_users` permission.

    Args:
        user_id (str):
        category (str):
        preference_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Preference]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        category=category,
        preference_name=preference_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    category: str,
    preference_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Preference]]:
    """Get a specific user preference

     Gets a single preference for the current user with the given category and name.
    ##### Permissions
    Must be logged in as the user being updated or have the `edit_other_users` permission.

    Args:
        user_id (str):
        category (str):
        preference_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Preference]
    """

    return sync_detailed(
        user_id=user_id,
        category=category,
        preference_name=preference_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    category: str,
    preference_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Preference]]:
    """Get a specific user preference

     Gets a single preference for the current user with the given category and name.
    ##### Permissions
    Must be logged in as the user being updated or have the `edit_other_users` permission.

    Args:
        user_id (str):
        category (str):
        preference_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Preference]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        category=category,
        preference_name=preference_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    category: str,
    preference_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Preference]]:
    """Get a specific user preference

     Gets a single preference for the current user with the given category and name.
    ##### Permissions
    Must be logged in as the user being updated or have the `edit_other_users` permission.

    Args:
        user_id (str):
        category (str):
        preference_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Preference]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            category=category,
            preference_name=preference_name,
            client=client,
        )
    ).parsed
