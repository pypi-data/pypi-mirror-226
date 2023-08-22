from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_teams_json_body import SearchTeamsJsonBody
from ...models.search_teams_response_200 import SearchTeamsResponse200
from ...types import Response


def _get_kwargs(
    *,
    json_body: SearchTeamsJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/teams/search",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, SearchTeamsResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SearchTeamsResponse200.from_dict(response.json())

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
) -> Response[Union[Any, SearchTeamsResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchTeamsJsonBody,
) -> Response[Union[Any, SearchTeamsResponse200]]:
    r"""Search teams

     Search teams based on search term and options provided in the request body.

    ##### Permissions
    Logged in user only shows open teams
    Logged in user with \"manage_system\" permission shows all teams

    Args:
        json_body (SearchTeamsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchTeamsResponse200]]
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
    json_body: SearchTeamsJsonBody,
) -> Optional[Union[Any, SearchTeamsResponse200]]:
    r"""Search teams

     Search teams based on search term and options provided in the request body.

    ##### Permissions
    Logged in user only shows open teams
    Logged in user with \"manage_system\" permission shows all teams

    Args:
        json_body (SearchTeamsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SearchTeamsResponse200]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchTeamsJsonBody,
) -> Response[Union[Any, SearchTeamsResponse200]]:
    r"""Search teams

     Search teams based on search term and options provided in the request body.

    ##### Permissions
    Logged in user only shows open teams
    Logged in user with \"manage_system\" permission shows all teams

    Args:
        json_body (SearchTeamsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchTeamsResponse200]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchTeamsJsonBody,
) -> Optional[Union[Any, SearchTeamsResponse200]]:
    r"""Search teams

     Search teams based on search term and options provided in the request body.

    ##### Permissions
    Logged in user only shows open teams
    Logged in user with \"manage_system\" permission shows all teams

    Args:
        json_body (SearchTeamsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SearchTeamsResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
