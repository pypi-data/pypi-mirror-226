from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.open_graph import OpenGraph
from ...models.open_graph_json_body import OpenGraphJsonBody
from ...types import Response


def _get_kwargs(
    *,
    json_body: OpenGraphJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/opengraph",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, OpenGraph]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = OpenGraph.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, OpenGraph]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: OpenGraphJsonBody,
) -> Response[Union[Any, OpenGraph]]:
    """Get open graph metadata for url

     Get Open Graph Metadata for a specif URL. Use the Open Graph protocol to get some generic metadata
    about a URL. Used for creating link previews.

    __Minimum server version__: 3.10

    ##### Permissions
    No permission required but must be logged in.

    Args:
        json_body (OpenGraphJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OpenGraph]]
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
    json_body: OpenGraphJsonBody,
) -> Optional[Union[Any, OpenGraph]]:
    """Get open graph metadata for url

     Get Open Graph Metadata for a specif URL. Use the Open Graph protocol to get some generic metadata
    about a URL. Used for creating link previews.

    __Minimum server version__: 3.10

    ##### Permissions
    No permission required but must be logged in.

    Args:
        json_body (OpenGraphJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OpenGraph]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: OpenGraphJsonBody,
) -> Response[Union[Any, OpenGraph]]:
    """Get open graph metadata for url

     Get Open Graph Metadata for a specif URL. Use the Open Graph protocol to get some generic metadata
    about a URL. Used for creating link previews.

    __Minimum server version__: 3.10

    ##### Permissions
    No permission required but must be logged in.

    Args:
        json_body (OpenGraphJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OpenGraph]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: OpenGraphJsonBody,
) -> Optional[Union[Any, OpenGraph]]:
    """Get open graph metadata for url

     Get Open Graph Metadata for a specif URL. Use the Open Graph protocol to get some generic metadata
    about a URL. Used for creating link previews.

    __Minimum server version__: 3.10

    ##### Permissions
    No permission required but must be logged in.

    Args:
        json_body (OpenGraphJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OpenGraph]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
