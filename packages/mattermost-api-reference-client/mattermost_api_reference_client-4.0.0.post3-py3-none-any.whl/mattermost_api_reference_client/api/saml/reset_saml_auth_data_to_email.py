from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.reset_saml_auth_data_to_email_json_body import ResetSamlAuthDataToEmailJsonBody
from ...models.reset_saml_auth_data_to_email_response_200 import ResetSamlAuthDataToEmailResponse200
from ...types import Response


def _get_kwargs(
    *,
    json_body: ResetSamlAuthDataToEmailJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/saml/reset_auth_data",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ResetSamlAuthDataToEmailResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ResetSamlAuthDataToEmailResponse200.from_dict(response.json())

        return response_200
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
) -> Response[Union[Any, ResetSamlAuthDataToEmailResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ResetSamlAuthDataToEmailJsonBody,
) -> Response[Union[Any, ResetSamlAuthDataToEmailResponse200]]:
    r"""Reset AuthData to Email

     Reset the AuthData field of SAML users to their email. This is meant to be used when the \"id\"
    attribute is set to an empty value (\"\") from a previously non-empty value.
    __Minimum server version__: 5.35
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (ResetSamlAuthDataToEmailJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResetSamlAuthDataToEmailResponse200]]
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
    json_body: ResetSamlAuthDataToEmailJsonBody,
) -> Optional[Union[Any, ResetSamlAuthDataToEmailResponse200]]:
    r"""Reset AuthData to Email

     Reset the AuthData field of SAML users to their email. This is meant to be used when the \"id\"
    attribute is set to an empty value (\"\") from a previously non-empty value.
    __Minimum server version__: 5.35
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (ResetSamlAuthDataToEmailJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResetSamlAuthDataToEmailResponse200]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ResetSamlAuthDataToEmailJsonBody,
) -> Response[Union[Any, ResetSamlAuthDataToEmailResponse200]]:
    r"""Reset AuthData to Email

     Reset the AuthData field of SAML users to their email. This is meant to be used when the \"id\"
    attribute is set to an empty value (\"\") from a previously non-empty value.
    __Minimum server version__: 5.35
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (ResetSamlAuthDataToEmailJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResetSamlAuthDataToEmailResponse200]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ResetSamlAuthDataToEmailJsonBody,
) -> Optional[Union[Any, ResetSamlAuthDataToEmailResponse200]]:
    r"""Reset AuthData to Email

     Reset the AuthData field of SAML users to their email. This is meant to be used when the \"id\"
    attribute is set to an empty value (\"\") from a previously non-empty value.
    __Minimum server version__: 5.35
    ##### Permissions
    Must have `manage_system` permission.

    Args:
        json_body (ResetSamlAuthDataToEmailJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResetSamlAuthDataToEmailResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
