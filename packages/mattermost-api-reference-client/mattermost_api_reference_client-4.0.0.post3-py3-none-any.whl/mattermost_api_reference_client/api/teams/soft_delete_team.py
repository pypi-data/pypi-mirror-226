from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.status_ok import StatusOK
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: str,
    *,
    permanent: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["permanent"] = permanent

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": "/api/v4/teams/{team_id}".format(
            team_id=team_id,
        ),
        "params": params,
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
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
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
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    permanent: Union[Unset, None, bool] = False,
) -> Response[Union[Any, StatusOK]]:
    """Delete a team

     Soft deletes a team, by marking the team as deleted in the database. Soft deleted teams will not be
    accessible in the user interface.

    Optionally use the permanent query parameter to hard delete the team for compliance reasons. As of
    server version 5.0, to use this feature `ServiceSettings.EnableAPITeamDeletion` must be set to
    `true` in the server's configuration.
    ##### Permissions
    Must have the `manage_team` permission.

    Args:
        team_id (str):
        permanent (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        permanent=permanent,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    permanent: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, StatusOK]]:
    """Delete a team

     Soft deletes a team, by marking the team as deleted in the database. Soft deleted teams will not be
    accessible in the user interface.

    Optionally use the permanent query parameter to hard delete the team for compliance reasons. As of
    server version 5.0, to use this feature `ServiceSettings.EnableAPITeamDeletion` must be set to
    `true` in the server's configuration.
    ##### Permissions
    Must have the `manage_team` permission.

    Args:
        team_id (str):
        permanent (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        permanent=permanent,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    permanent: Union[Unset, None, bool] = False,
) -> Response[Union[Any, StatusOK]]:
    """Delete a team

     Soft deletes a team, by marking the team as deleted in the database. Soft deleted teams will not be
    accessible in the user interface.

    Optionally use the permanent query parameter to hard delete the team for compliance reasons. As of
    server version 5.0, to use this feature `ServiceSettings.EnableAPITeamDeletion` must be set to
    `true` in the server's configuration.
    ##### Permissions
    Must have the `manage_team` permission.

    Args:
        team_id (str):
        permanent (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        permanent=permanent,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    permanent: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, StatusOK]]:
    """Delete a team

     Soft deletes a team, by marking the team as deleted in the database. Soft deleted teams will not be
    accessible in the user interface.

    Optionally use the permanent query parameter to hard delete the team for compliance reasons. As of
    server version 5.0, to use this feature `ServiceSettings.EnableAPITeamDeletion` must be set to
    `true` in the server's configuration.
    ##### Permissions
    Must have the `manage_team` permission.

    Args:
        team_id (str):
        permanent (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            permanent=permanent,
        )
    ).parsed
