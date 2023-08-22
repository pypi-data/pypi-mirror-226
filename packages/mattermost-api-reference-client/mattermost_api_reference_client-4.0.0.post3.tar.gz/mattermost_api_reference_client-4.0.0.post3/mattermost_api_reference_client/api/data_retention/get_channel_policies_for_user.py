from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.retention_policy_for_channel_list import RetentionPolicyForChannelList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    *,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/users/{user_id}/data_retention/channel_policies".format(
            user_id=user_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, RetentionPolicyForChannelList]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RetentionPolicyForChannelList.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, RetentionPolicyForChannelList]]:
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
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
) -> Response[Union[Any, RetentionPolicyForChannelList]]:
    """Get the policies which are applied to a user's channels

     Gets the policies which are applied to the all of the channels to which a user belongs.

    __Minimum server version__: 5.35

    ##### Permissions
    Must be logged in as the user or have the `manage_system` permission.

    ##### License
    Requires an E20 license.

    Args:
        user_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, RetentionPolicyForChannelList]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
) -> Optional[Union[Any, RetentionPolicyForChannelList]]:
    """Get the policies which are applied to a user's channels

     Gets the policies which are applied to the all of the channels to which a user belongs.

    __Minimum server version__: 5.35

    ##### Permissions
    Must be logged in as the user or have the `manage_system` permission.

    ##### License
    Requires an E20 license.

    Args:
        user_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, RetentionPolicyForChannelList]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
) -> Response[Union[Any, RetentionPolicyForChannelList]]:
    """Get the policies which are applied to a user's channels

     Gets the policies which are applied to the all of the channels to which a user belongs.

    __Minimum server version__: 5.35

    ##### Permissions
    Must be logged in as the user or have the `manage_system` permission.

    ##### License
    Requires an E20 license.

    Args:
        user_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, RetentionPolicyForChannelList]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
) -> Optional[Union[Any, RetentionPolicyForChannelList]]:
    """Get the policies which are applied to a user's channels

     Gets the policies which are applied to the all of the channels to which a user belongs.

    __Minimum server version__: 5.35

    ##### Permissions
    Must be logged in as the user or have the `manage_system` permission.

    ##### License
    Requires an E20 license.

    Args:
        user_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, RetentionPolicyForChannelList]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            page=page,
            per_page=per_page,
        )
    ).parsed
