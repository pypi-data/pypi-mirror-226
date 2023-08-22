from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.channel import Channel
from ...models.search_channels_json_body import SearchChannelsJsonBody
from ...types import Response


def _get_kwargs(
    team_id: str,
    *,
    json_body: SearchChannelsJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/teams/{team_id}/channels/search".format(
            team_id=team_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["Channel"]]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = Channel.from_dict(response_201_item_data)

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
) -> Response[Union[Any, List["Channel"]]]:
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
    json_body: SearchChannelsJsonBody,
) -> Response[Union[Any, List["Channel"]]]:
    """Search channels

     Search public channels on a team based on the search term provided in the request body.
    ##### Permissions
    Must have the `list_team_channels` permission.

    In server version 5.16 and later, a user without the `list_team_channels` permission will be able to
    use this endpoint, with the search results limited to the channels that the user is a member of.

    Args:
        team_id (str):
        json_body (SearchChannelsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Channel']]]
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
    json_body: SearchChannelsJsonBody,
) -> Optional[Union[Any, List["Channel"]]]:
    """Search channels

     Search public channels on a team based on the search term provided in the request body.
    ##### Permissions
    Must have the `list_team_channels` permission.

    In server version 5.16 and later, a user without the `list_team_channels` permission will be able to
    use this endpoint, with the search results limited to the channels that the user is a member of.

    Args:
        team_id (str):
        json_body (SearchChannelsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Channel']]
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
    json_body: SearchChannelsJsonBody,
) -> Response[Union[Any, List["Channel"]]]:
    """Search channels

     Search public channels on a team based on the search term provided in the request body.
    ##### Permissions
    Must have the `list_team_channels` permission.

    In server version 5.16 and later, a user without the `list_team_channels` permission will be able to
    use this endpoint, with the search results limited to the channels that the user is a member of.

    Args:
        team_id (str):
        json_body (SearchChannelsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Channel']]]
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
    json_body: SearchChannelsJsonBody,
) -> Optional[Union[Any, List["Channel"]]]:
    """Search channels

     Search public channels on a team based on the search term provided in the request body.
    ##### Permissions
    Must have the `list_team_channels` permission.

    In server version 5.16 and later, a user without the `list_team_channels` permission will be able to
    use this endpoint, with the search results limited to the channels that the user is a member of.

    Args:
        team_id (str):
        json_body (SearchChannelsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Channel']]
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
