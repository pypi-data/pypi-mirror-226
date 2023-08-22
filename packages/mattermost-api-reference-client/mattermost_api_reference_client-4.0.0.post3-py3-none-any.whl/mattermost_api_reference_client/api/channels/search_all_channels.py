from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_all_channels_json_body import SearchAllChannelsJsonBody
from ...models.search_all_channels_response_200 import SearchAllChannelsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    json_body: SearchAllChannelsJsonBody,
    system_console: Union[Unset, None, bool] = True,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["system_console"] = system_console

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/channels/search",
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, SearchAllChannelsResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SearchAllChannelsResponse200.from_dict(response.json())

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
) -> Response[Union[Any, SearchAllChannelsResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchAllChannelsJsonBody,
    system_console: Union[Unset, None, bool] = True,
) -> Response[Union[Any, SearchAllChannelsResponse200]]:
    """Search all private and open type channels across all teams

     Returns all private and open type channels where 'term' matches on the name, display name, or
    purpose of
    the channel.

    Configured 'default' channels (ex Town Square and Off-Topic) can be excluded from the results
    with the `exclude_default_channels` boolean parameter.

    Channels that are associated (via GroupChannel records) to a given group can be excluded from the
    results
    with the `not_associated_to_group` parameter and a group id string.

    Args:
        system_console (Union[Unset, None, bool]):  Default: True.
        json_body (SearchAllChannelsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchAllChannelsResponse200]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        system_console=system_console,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchAllChannelsJsonBody,
    system_console: Union[Unset, None, bool] = True,
) -> Optional[Union[Any, SearchAllChannelsResponse200]]:
    """Search all private and open type channels across all teams

     Returns all private and open type channels where 'term' matches on the name, display name, or
    purpose of
    the channel.

    Configured 'default' channels (ex Town Square and Off-Topic) can be excluded from the results
    with the `exclude_default_channels` boolean parameter.

    Channels that are associated (via GroupChannel records) to a given group can be excluded from the
    results
    with the `not_associated_to_group` parameter and a group id string.

    Args:
        system_console (Union[Unset, None, bool]):  Default: True.
        json_body (SearchAllChannelsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SearchAllChannelsResponse200]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        system_console=system_console,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchAllChannelsJsonBody,
    system_console: Union[Unset, None, bool] = True,
) -> Response[Union[Any, SearchAllChannelsResponse200]]:
    """Search all private and open type channels across all teams

     Returns all private and open type channels where 'term' matches on the name, display name, or
    purpose of
    the channel.

    Configured 'default' channels (ex Town Square and Off-Topic) can be excluded from the results
    with the `exclude_default_channels` boolean parameter.

    Channels that are associated (via GroupChannel records) to a given group can be excluded from the
    results
    with the `not_associated_to_group` parameter and a group id string.

    Args:
        system_console (Union[Unset, None, bool]):  Default: True.
        json_body (SearchAllChannelsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchAllChannelsResponse200]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        system_console=system_console,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchAllChannelsJsonBody,
    system_console: Union[Unset, None, bool] = True,
) -> Optional[Union[Any, SearchAllChannelsResponse200]]:
    """Search all private and open type channels across all teams

     Returns all private and open type channels where 'term' matches on the name, display name, or
    purpose of
    the channel.

    Configured 'default' channels (ex Town Square and Off-Topic) can be excluded from the results
    with the `exclude_default_channels` boolean parameter.

    Channels that are associated (via GroupChannel records) to a given group can be excluded from the
    results
    with the `not_associated_to_group` parameter and a group id string.

    Args:
        system_console (Union[Unset, None, bool]):  Default: True.
        json_body (SearchAllChannelsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SearchAllChannelsResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            system_console=system_console,
        )
    ).parsed
