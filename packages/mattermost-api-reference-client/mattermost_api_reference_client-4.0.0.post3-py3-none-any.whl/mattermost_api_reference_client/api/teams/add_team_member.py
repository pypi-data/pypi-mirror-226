from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_team_member_json_body import AddTeamMemberJsonBody
from ...models.team_member import TeamMember
from ...types import Response


def _get_kwargs(
    team_id: str,
    *,
    json_body: AddTeamMemberJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/teams/{team_id}/members".format(
            team_id=team_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, TeamMember]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = TeamMember.from_dict(response.json())

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
) -> Response[Union[Any, TeamMember]]:
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
    json_body: AddTeamMemberJsonBody,
) -> Response[Union[Any, TeamMember]]:
    """Add user to team

     Add user to the team by user_id.
    ##### Permissions
    Must be authenticated and team be open to add self. For adding another user, authenticated user must
    have the `add_user_to_team` permission.

    Args:
        team_id (str):
        json_body (AddTeamMemberJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, TeamMember]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: AddTeamMemberJsonBody,
) -> Optional[Union[Any, TeamMember]]:
    """Add user to team

     Add user to the team by user_id.
    ##### Permissions
    Must be authenticated and team be open to add self. For adding another user, authenticated user must
    have the `add_user_to_team` permission.

    Args:
        team_id (str):
        json_body (AddTeamMemberJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, TeamMember]
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: AddTeamMemberJsonBody,
) -> Response[Union[Any, TeamMember]]:
    """Add user to team

     Add user to the team by user_id.
    ##### Permissions
    Must be authenticated and team be open to add self. For adding another user, authenticated user must
    have the `add_user_to_team` permission.

    Args:
        team_id (str):
        json_body (AddTeamMemberJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, TeamMember]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: AddTeamMemberJsonBody,
) -> Optional[Union[Any, TeamMember]]:
    """Add user to team

     Add user to the team by user_id.
    ##### Permissions
    Must be authenticated and team be open to add self. For adding another user, authenticated user must
    have the `add_user_to_team` permission.

    Args:
        team_id (str):
        json_body (AddTeamMemberJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, TeamMember]
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
