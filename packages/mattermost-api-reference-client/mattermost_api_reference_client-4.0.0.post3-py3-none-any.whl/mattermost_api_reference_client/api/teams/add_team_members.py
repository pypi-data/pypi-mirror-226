from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.team_member import TeamMember
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: str,
    *,
    json_body: List["TeamMember"],
    graceful: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["graceful"] = graceful

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = []
    for json_body_item_data in json_body:
        json_body_item = json_body_item_data.to_dict()

        json_json_body.append(json_body_item)

    return {
        "method": "post",
        "url": "/api/v4/teams/{team_id}/members/batch".format(
            team_id=team_id,
        ),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["TeamMember"]]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = TeamMember.from_dict(response_201_item_data)

            response_201.append(response_201_item)

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, List["TeamMember"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: List["TeamMember"],
    graceful: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, List["TeamMember"]]]:
    """Add multiple users to team

     Add a number of users to the team by user_id.
    ##### Permissions
    Must be authenticated. Authenticated user must have the `add_user_to_team` permission.

    Args:
        team_id (str):
        graceful (Union[Unset, None, bool]):
        json_body (List['TeamMember']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['TeamMember']]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        json_body=json_body,
        graceful=graceful,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: List["TeamMember"],
    graceful: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, List["TeamMember"]]]:
    """Add multiple users to team

     Add a number of users to the team by user_id.
    ##### Permissions
    Must be authenticated. Authenticated user must have the `add_user_to_team` permission.

    Args:
        team_id (str):
        graceful (Union[Unset, None, bool]):
        json_body (List['TeamMember']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['TeamMember']]
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        json_body=json_body,
        graceful=graceful,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: List["TeamMember"],
    graceful: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, List["TeamMember"]]]:
    """Add multiple users to team

     Add a number of users to the team by user_id.
    ##### Permissions
    Must be authenticated. Authenticated user must have the `add_user_to_team` permission.

    Args:
        team_id (str):
        graceful (Union[Unset, None, bool]):
        json_body (List['TeamMember']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['TeamMember']]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        json_body=json_body,
        graceful=graceful,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: List["TeamMember"],
    graceful: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, List["TeamMember"]]]:
    """Add multiple users to team

     Add a number of users to the team by user_id.
    ##### Permissions
    Must be authenticated. Authenticated user must have the `add_user_to_team` permission.

    Args:
        team_id (str):
        graceful (Union[Unset, None, bool]):
        json_body (List['TeamMember']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['TeamMember']]
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            json_body=json_body,
            graceful=graceful,
        )
    ).parsed
