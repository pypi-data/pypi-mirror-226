from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.file_info_list import FileInfoList
from ...models.search_files_multipart_data import SearchFilesMultipartData
from ...types import Response


def _get_kwargs(
    team_id: str,
    *,
    multipart_data: SearchFilesMultipartData,
) -> Dict[str, Any]:
    pass

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": "/api/v4/teams/{team_id}/files/search".format(
            team_id=team_id,
        ),
        "files": multipart_multipart_data,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, FileInfoList]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = FileInfoList.from_dict(response.json())

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
) -> Response[Union[Any, FileInfoList]]:
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
    multipart_data: SearchFilesMultipartData,
) -> Response[Union[Any, FileInfoList]]:
    """Search files in a team

     Search for files in a team based on file name, extention and file content (if file content
    extraction is enabled and supported for the files).
    __Minimum server version__: 5.34
    ##### Permissions
    Must be authenticated and have the `view_team` permission.

    Args:
        team_id (str):
        multipart_data (SearchFilesMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, FileInfoList]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        multipart_data=multipart_data,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: SearchFilesMultipartData,
) -> Optional[Union[Any, FileInfoList]]:
    """Search files in a team

     Search for files in a team based on file name, extention and file content (if file content
    extraction is enabled and supported for the files).
    __Minimum server version__: 5.34
    ##### Permissions
    Must be authenticated and have the `view_team` permission.

    Args:
        team_id (str):
        multipart_data (SearchFilesMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, FileInfoList]
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        multipart_data=multipart_data,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: SearchFilesMultipartData,
) -> Response[Union[Any, FileInfoList]]:
    """Search files in a team

     Search for files in a team based on file name, extention and file content (if file content
    extraction is enabled and supported for the files).
    __Minimum server version__: 5.34
    ##### Permissions
    Must be authenticated and have the `view_team` permission.

    Args:
        team_id (str):
        multipart_data (SearchFilesMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, FileInfoList]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        multipart_data=multipart_data,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: SearchFilesMultipartData,
) -> Optional[Union[Any, FileInfoList]]:
    """Search files in a team

     Search for files in a team based on file name, extention and file content (if file content
    extraction is enabled and supported for the files).
    __Minimum server version__: 5.34
    ##### Permissions
    Must be authenticated and have the `view_team` permission.

    Args:
        team_id (str):
        multipart_data (SearchFilesMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, FileInfoList]
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            multipart_data=multipart_data,
        )
    ).parsed
