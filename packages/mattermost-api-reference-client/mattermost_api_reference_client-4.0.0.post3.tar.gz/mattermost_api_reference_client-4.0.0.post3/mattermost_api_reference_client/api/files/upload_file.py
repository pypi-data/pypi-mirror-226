from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.upload_file_multipart_data import UploadFileMultipartData
from ...models.upload_file_response_201 import UploadFileResponse201
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    multipart_data: UploadFileMultipartData,
    channel_id: Union[Unset, None, str] = UNSET,
    filename: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["channel_id"] = channel_id

    params["filename"] = filename

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": "/api/v4/files",
        "files": multipart_multipart_data,
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, UploadFileResponse201]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = UploadFileResponse201.from_dict(response.json())

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
    if response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
        response_413 = cast(Any, None)
        return response_413
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, UploadFileResponse201]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: UploadFileMultipartData,
    channel_id: Union[Unset, None, str] = UNSET,
    filename: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, UploadFileResponse201]]:
    """Upload a file

     Uploads a file that can later be attached to a post.

    This request can either be a multipart/form-data request with a channel_id, files and optional
    client_ids defined in the FormData, or it can be a request with the channel_id and filename
    defined as query parameters with the contents of a single file in the body of the request.

    Only multipart/form-data requests are supported by server versions up to and including 4.7.
    Server versions 4.8 and higher support both types of requests.

    ##### Permissions
    Must have `upload_file` permission.

    Args:
        channel_id (Union[Unset, None, str]):
        filename (Union[Unset, None, str]):
        multipart_data (UploadFileMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UploadFileResponse201]]
    """

    kwargs = _get_kwargs(
        multipart_data=multipart_data,
        channel_id=channel_id,
        filename=filename,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: UploadFileMultipartData,
    channel_id: Union[Unset, None, str] = UNSET,
    filename: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, UploadFileResponse201]]:
    """Upload a file

     Uploads a file that can later be attached to a post.

    This request can either be a multipart/form-data request with a channel_id, files and optional
    client_ids defined in the FormData, or it can be a request with the channel_id and filename
    defined as query parameters with the contents of a single file in the body of the request.

    Only multipart/form-data requests are supported by server versions up to and including 4.7.
    Server versions 4.8 and higher support both types of requests.

    ##### Permissions
    Must have `upload_file` permission.

    Args:
        channel_id (Union[Unset, None, str]):
        filename (Union[Unset, None, str]):
        multipart_data (UploadFileMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UploadFileResponse201]
    """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        channel_id=channel_id,
        filename=filename,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: UploadFileMultipartData,
    channel_id: Union[Unset, None, str] = UNSET,
    filename: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, UploadFileResponse201]]:
    """Upload a file

     Uploads a file that can later be attached to a post.

    This request can either be a multipart/form-data request with a channel_id, files and optional
    client_ids defined in the FormData, or it can be a request with the channel_id and filename
    defined as query parameters with the contents of a single file in the body of the request.

    Only multipart/form-data requests are supported by server versions up to and including 4.7.
    Server versions 4.8 and higher support both types of requests.

    ##### Permissions
    Must have `upload_file` permission.

    Args:
        channel_id (Union[Unset, None, str]):
        filename (Union[Unset, None, str]):
        multipart_data (UploadFileMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UploadFileResponse201]]
    """

    kwargs = _get_kwargs(
        multipart_data=multipart_data,
        channel_id=channel_id,
        filename=filename,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: UploadFileMultipartData,
    channel_id: Union[Unset, None, str] = UNSET,
    filename: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, UploadFileResponse201]]:
    """Upload a file

     Uploads a file that can later be attached to a post.

    This request can either be a multipart/form-data request with a channel_id, files and optional
    client_ids defined in the FormData, or it can be a request with the channel_id and filename
    defined as query parameters with the contents of a single file in the body of the request.

    Only multipart/form-data requests are supported by server versions up to and including 4.7.
    Server versions 4.8 and higher support both types of requests.

    ##### Permissions
    Must have `upload_file` permission.

    Args:
        channel_id (Union[Unset, None, str]):
        filename (Union[Unset, None, str]):
        multipart_data (UploadFileMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UploadFileResponse201]
    """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            channel_id=channel_id,
            filename=filename,
        )
    ).parsed
