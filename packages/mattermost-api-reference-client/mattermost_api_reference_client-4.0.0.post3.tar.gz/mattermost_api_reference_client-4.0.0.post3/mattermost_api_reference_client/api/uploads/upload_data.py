from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.file_info import FileInfo
from ...models.upload_data_data import UploadDataData
from ...types import Response


def _get_kwargs(
    upload_id: str,
    form_data: UploadDataData,
) -> Dict[str, Any]:
    pass

    return {
        "method": "post",
        "url": "/api/v4/uploads/{upload_id}".format(
            upload_id=upload_id,
        ),
        "data": form_data.to_dict(),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, FileInfo]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = FileInfo.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
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
) -> Response[Union[Any, FileInfo]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    upload_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    form_data: UploadDataData,
) -> Response[Union[Any, FileInfo]]:
    """Perform a file upload

     Starts or resumes a file upload.
    To resume an existing (incomplete) upload, data should be sent starting from the offset specified in
    the upload session object.

    The request body can be in one of two formats:
    - Binary file content streamed in request's body
    - multipart/form-data

    ##### Permissions
    Must be logged in as the user who created the upload session.

    Args:
        upload_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, FileInfo]]
    """

    kwargs = _get_kwargs(
        upload_id=upload_id,
        form_data=form_data,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    upload_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    form_data: UploadDataData,
) -> Optional[Union[Any, FileInfo]]:
    """Perform a file upload

     Starts or resumes a file upload.
    To resume an existing (incomplete) upload, data should be sent starting from the offset specified in
    the upload session object.

    The request body can be in one of two formats:
    - Binary file content streamed in request's body
    - multipart/form-data

    ##### Permissions
    Must be logged in as the user who created the upload session.

    Args:
        upload_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, FileInfo]
    """

    return sync_detailed(
        upload_id=upload_id,
        client=client,
        form_data=form_data,
    ).parsed


async def asyncio_detailed(
    upload_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    form_data: UploadDataData,
) -> Response[Union[Any, FileInfo]]:
    """Perform a file upload

     Starts or resumes a file upload.
    To resume an existing (incomplete) upload, data should be sent starting from the offset specified in
    the upload session object.

    The request body can be in one of two formats:
    - Binary file content streamed in request's body
    - multipart/form-data

    ##### Permissions
    Must be logged in as the user who created the upload session.

    Args:
        upload_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, FileInfo]]
    """

    kwargs = _get_kwargs(
        upload_id=upload_id,
        form_data=form_data,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    upload_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    form_data: UploadDataData,
) -> Optional[Union[Any, FileInfo]]:
    """Perform a file upload

     Starts or resumes a file upload.
    To resume an existing (incomplete) upload, data should be sent starting from the offset specified in
    the upload session object.

    The request body can be in one of two formats:
    - Binary file content streamed in request's body
    - multipart/form-data

    ##### Permissions
    Must be logged in as the user who created the upload session.

    Args:
        upload_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, FileInfo]
    """

    return (
        await asyncio_detailed(
            upload_id=upload_id,
            client=client,
            form_data=form_data,
        )
    ).parsed
