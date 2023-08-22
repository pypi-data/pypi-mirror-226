from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.file_info import FileInfo
from ...types import UNSET, Response, Unset


def _get_kwargs(
    post_id: str,
    *,
    include_deleted: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["include_deleted"] = include_deleted

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/posts/{post_id}/files/info".format(
            post_id=post_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["FileInfo"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = FileInfo.from_dict(response_200_item_data)

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
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, List["FileInfo"]]]:
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
    include_deleted: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List["FileInfo"]]]:
    """Get file info for post

     Gets a list of file information objects for the files attached to a post.
    ##### Permissions
    Must have `read_channel` permission for the channel the post is in.

    Args:
        post_id (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['FileInfo']]]
    """

    kwargs = _get_kwargs(
        post_id=post_id,
        include_deleted=include_deleted,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List["FileInfo"]]]:
    """Get file info for post

     Gets a list of file information objects for the files attached to a post.
    ##### Permissions
    Must have `read_channel` permission for the channel the post is in.

    Args:
        post_id (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['FileInfo']]
    """

    return sync_detailed(
        post_id=post_id,
        client=client,
        include_deleted=include_deleted,
    ).parsed


async def asyncio_detailed(
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List["FileInfo"]]]:
    """Get file info for post

     Gets a list of file information objects for the files attached to a post.
    ##### Permissions
    Must have `read_channel` permission for the channel the post is in.

    Args:
        post_id (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['FileInfo']]]
    """

    kwargs = _get_kwargs(
        post_id=post_id,
        include_deleted=include_deleted,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List["FileInfo"]]]:
    """Get file info for post

     Gets a list of file information objects for the files attached to a post.
    ##### Permissions
    Must have `read_channel` permission for the channel the post is in.

    Args:
        post_id (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['FileInfo']]
    """

    return (
        await asyncio_detailed(
            post_id=post_id,
            client=client,
            include_deleted=include_deleted,
        )
    ).parsed
