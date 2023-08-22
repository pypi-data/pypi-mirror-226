from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.status_ok import StatusOK
from ...models.upload_saml_public_certificate_multipart_data import UploadSamlPublicCertificateMultipartData
from ...types import Response


def _get_kwargs(
    *,
    multipart_data: UploadSamlPublicCertificateMultipartData,
) -> Dict[str, Any]:
    pass

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": "/api/v4/saml/certificate/public",
        "files": multipart_multipart_data,
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
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
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
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: UploadSamlPublicCertificateMultipartData,
) -> Response[Union[Any, StatusOK]]:
    """Upload public certificate

     Upload the public certificate to be used for encryption with your SAML configuration. The server
    will pick a hard-coded filename for the PublicCertificateFile setting in your `config.json`.
    ##### Permissions
    Must have `sysconsole_write_authentication` permission.

    Args:
        multipart_data (UploadSamlPublicCertificateMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        multipart_data=multipart_data,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: UploadSamlPublicCertificateMultipartData,
) -> Optional[Union[Any, StatusOK]]:
    """Upload public certificate

     Upload the public certificate to be used for encryption with your SAML configuration. The server
    will pick a hard-coded filename for the PublicCertificateFile setting in your `config.json`.
    ##### Permissions
    Must have `sysconsole_write_authentication` permission.

    Args:
        multipart_data (UploadSamlPublicCertificateMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: UploadSamlPublicCertificateMultipartData,
) -> Response[Union[Any, StatusOK]]:
    """Upload public certificate

     Upload the public certificate to be used for encryption with your SAML configuration. The server
    will pick a hard-coded filename for the PublicCertificateFile setting in your `config.json`.
    ##### Permissions
    Must have `sysconsole_write_authentication` permission.

    Args:
        multipart_data (UploadSamlPublicCertificateMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        multipart_data=multipart_data,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: UploadSamlPublicCertificateMultipartData,
) -> Optional[Union[Any, StatusOK]]:
    """Upload public certificate

     Upload the public certificate to be used for encryption with your SAML configuration. The server
    will pick a hard-coded filename for the PublicCertificateFile setting in your `config.json`.
    ##### Permissions
    Must have `sysconsole_write_authentication` permission.

    Args:
        multipart_data (UploadSamlPublicCertificateMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
        )
    ).parsed
