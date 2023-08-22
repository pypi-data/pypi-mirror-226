from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_list import PostList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    post_id: str,
    *,
    per_page: Union[Unset, None, int] = 0,
    from_post: Union[Unset, None, str] = "",
    from_create_at: Union[Unset, None, int] = 0,
    direction: Union[Unset, None, str] = "",
    skip_fetch_threads: Union[Unset, None, bool] = False,
    collapsed_threads: Union[Unset, None, bool] = False,
    collapsed_threads_extended: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["perPage"] = per_page

    params["fromPost"] = from_post

    params["fromCreateAt"] = from_create_at

    params["direction"] = direction

    params["skipFetchThreads"] = skip_fetch_threads

    params["collapsedThreads"] = collapsed_threads

    params["collapsedThreadsExtended"] = collapsed_threads_extended

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/posts/{post_id}/thread".format(
            post_id=post_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PostList]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PostList.from_dict(response.json())

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
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, PostList]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    per_page: Union[Unset, None, int] = 0,
    from_post: Union[Unset, None, str] = "",
    from_create_at: Union[Unset, None, int] = 0,
    direction: Union[Unset, None, str] = "",
    skip_fetch_threads: Union[Unset, None, bool] = False,
    collapsed_threads: Union[Unset, None, bool] = False,
    collapsed_threads_extended: Union[Unset, None, bool] = False,
) -> Response[Union[Any, PostList]]:
    """Get a thread

     Get a post and the rest of the posts in the same thread.
    ##### Permissions
    Must have `read_channel` permission for the channel the post is in or if the channel is public, have
    the `read_public_channels` permission for the team.

    Args:
        post_id (str):
        per_page (Union[Unset, None, int]):
        from_post (Union[Unset, None, str]):  Default: ''.
        from_create_at (Union[Unset, None, int]):
        direction (Union[Unset, None, str]):  Default: ''.
        skip_fetch_threads (Union[Unset, None, bool]):
        collapsed_threads (Union[Unset, None, bool]):
        collapsed_threads_extended (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PostList]]
    """

    kwargs = _get_kwargs(
        post_id=post_id,
        per_page=per_page,
        from_post=from_post,
        from_create_at=from_create_at,
        direction=direction,
        skip_fetch_threads=skip_fetch_threads,
        collapsed_threads=collapsed_threads,
        collapsed_threads_extended=collapsed_threads_extended,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    per_page: Union[Unset, None, int] = 0,
    from_post: Union[Unset, None, str] = "",
    from_create_at: Union[Unset, None, int] = 0,
    direction: Union[Unset, None, str] = "",
    skip_fetch_threads: Union[Unset, None, bool] = False,
    collapsed_threads: Union[Unset, None, bool] = False,
    collapsed_threads_extended: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, PostList]]:
    """Get a thread

     Get a post and the rest of the posts in the same thread.
    ##### Permissions
    Must have `read_channel` permission for the channel the post is in or if the channel is public, have
    the `read_public_channels` permission for the team.

    Args:
        post_id (str):
        per_page (Union[Unset, None, int]):
        from_post (Union[Unset, None, str]):  Default: ''.
        from_create_at (Union[Unset, None, int]):
        direction (Union[Unset, None, str]):  Default: ''.
        skip_fetch_threads (Union[Unset, None, bool]):
        collapsed_threads (Union[Unset, None, bool]):
        collapsed_threads_extended (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PostList]
    """

    return sync_detailed(
        post_id=post_id,
        client=client,
        per_page=per_page,
        from_post=from_post,
        from_create_at=from_create_at,
        direction=direction,
        skip_fetch_threads=skip_fetch_threads,
        collapsed_threads=collapsed_threads,
        collapsed_threads_extended=collapsed_threads_extended,
    ).parsed


async def asyncio_detailed(
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    per_page: Union[Unset, None, int] = 0,
    from_post: Union[Unset, None, str] = "",
    from_create_at: Union[Unset, None, int] = 0,
    direction: Union[Unset, None, str] = "",
    skip_fetch_threads: Union[Unset, None, bool] = False,
    collapsed_threads: Union[Unset, None, bool] = False,
    collapsed_threads_extended: Union[Unset, None, bool] = False,
) -> Response[Union[Any, PostList]]:
    """Get a thread

     Get a post and the rest of the posts in the same thread.
    ##### Permissions
    Must have `read_channel` permission for the channel the post is in or if the channel is public, have
    the `read_public_channels` permission for the team.

    Args:
        post_id (str):
        per_page (Union[Unset, None, int]):
        from_post (Union[Unset, None, str]):  Default: ''.
        from_create_at (Union[Unset, None, int]):
        direction (Union[Unset, None, str]):  Default: ''.
        skip_fetch_threads (Union[Unset, None, bool]):
        collapsed_threads (Union[Unset, None, bool]):
        collapsed_threads_extended (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PostList]]
    """

    kwargs = _get_kwargs(
        post_id=post_id,
        per_page=per_page,
        from_post=from_post,
        from_create_at=from_create_at,
        direction=direction,
        skip_fetch_threads=skip_fetch_threads,
        collapsed_threads=collapsed_threads,
        collapsed_threads_extended=collapsed_threads_extended,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    per_page: Union[Unset, None, int] = 0,
    from_post: Union[Unset, None, str] = "",
    from_create_at: Union[Unset, None, int] = 0,
    direction: Union[Unset, None, str] = "",
    skip_fetch_threads: Union[Unset, None, bool] = False,
    collapsed_threads: Union[Unset, None, bool] = False,
    collapsed_threads_extended: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, PostList]]:
    """Get a thread

     Get a post and the rest of the posts in the same thread.
    ##### Permissions
    Must have `read_channel` permission for the channel the post is in or if the channel is public, have
    the `read_public_channels` permission for the team.

    Args:
        post_id (str):
        per_page (Union[Unset, None, int]):
        from_post (Union[Unset, None, str]):  Default: ''.
        from_create_at (Union[Unset, None, int]):
        direction (Union[Unset, None, str]):  Default: ''.
        skip_fetch_threads (Union[Unset, None, bool]):
        collapsed_threads (Union[Unset, None, bool]):
        collapsed_threads_extended (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PostList]
    """

    return (
        await asyncio_detailed(
            post_id=post_id,
            client=client,
            per_page=per_page,
            from_post=from_post,
            from_create_at=from_create_at,
            direction=direction,
            skip_fetch_threads=skip_fetch_threads,
            collapsed_threads=collapsed_threads,
            collapsed_threads_extended=collapsed_threads_extended,
        )
    ).parsed
