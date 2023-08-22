from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.command import Command
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    team_id: Union[Unset, None, str] = UNSET,
    custom_only: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["team_id"] = team_id

    params["custom_only"] = custom_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/commands",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["Command"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Command.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, List["Command"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    team_id: Union[Unset, None, str] = UNSET,
    custom_only: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List["Command"]]]:
    """List commands for a team

     List commands for a team.
    ##### Permissions
    `manage_slash_commands` if need list custom commands.

    Args:
        team_id (Union[Unset, None, str]):
        custom_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Command']]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        custom_only=custom_only,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    team_id: Union[Unset, None, str] = UNSET,
    custom_only: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List["Command"]]]:
    """List commands for a team

     List commands for a team.
    ##### Permissions
    `manage_slash_commands` if need list custom commands.

    Args:
        team_id (Union[Unset, None, str]):
        custom_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Command']]
    """

    return sync_detailed(
        client=client,
        team_id=team_id,
        custom_only=custom_only,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    team_id: Union[Unset, None, str] = UNSET,
    custom_only: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List["Command"]]]:
    """List commands for a team

     List commands for a team.
    ##### Permissions
    `manage_slash_commands` if need list custom commands.

    Args:
        team_id (Union[Unset, None, str]):
        custom_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Command']]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        custom_only=custom_only,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    team_id: Union[Unset, None, str] = UNSET,
    custom_only: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List["Command"]]]:
    """List commands for a team

     List commands for a team.
    ##### Permissions
    `manage_slash_commands` if need list custom commands.

    Args:
        team_id (Union[Unset, None, str]):
        custom_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Command']]
    """

    return (
        await asyncio_detailed(
            client=client,
            team_id=team_id,
            custom_only=custom_only,
        )
    ).parsed
