from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.set_bot_icon_image_multipart_data import SetBotIconImageMultipartData
from ...models.status_ok import StatusOK
from ...types import Response


def _get_kwargs(
    bot_user_id: str,
    *,
    multipart_data: SetBotIconImageMultipartData,
) -> Dict[str, Any]:
    pass

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": "/api/v4/bots/{bot_user_id}/icon".format(
            bot_user_id=bot_user_id,
        ),
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
    if response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
        response_413 = cast(Any, None)
        return response_413
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
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
    bot_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: SetBotIconImageMultipartData,
) -> Response[Union[Any, StatusOK]]:
    """Set bot's LHS icon image

     Set a bot's LHS icon image based on bot_user_id string parameter. Icon image must be SVG format, all
    other formats are rejected.
    ##### Permissions
    Must have `manage_bots` permission.
    __Minimum server version__: 5.14

    Args:
        bot_user_id (str):
        multipart_data (SetBotIconImageMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        bot_user_id=bot_user_id,
        multipart_data=multipart_data,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    bot_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: SetBotIconImageMultipartData,
) -> Optional[Union[Any, StatusOK]]:
    """Set bot's LHS icon image

     Set a bot's LHS icon image based on bot_user_id string parameter. Icon image must be SVG format, all
    other formats are rejected.
    ##### Permissions
    Must have `manage_bots` permission.
    __Minimum server version__: 5.14

    Args:
        bot_user_id (str):
        multipart_data (SetBotIconImageMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        bot_user_id=bot_user_id,
        client=client,
        multipart_data=multipart_data,
    ).parsed


async def asyncio_detailed(
    bot_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: SetBotIconImageMultipartData,
) -> Response[Union[Any, StatusOK]]:
    """Set bot's LHS icon image

     Set a bot's LHS icon image based on bot_user_id string parameter. Icon image must be SVG format, all
    other formats are rejected.
    ##### Permissions
    Must have `manage_bots` permission.
    __Minimum server version__: 5.14

    Args:
        bot_user_id (str):
        multipart_data (SetBotIconImageMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        bot_user_id=bot_user_id,
        multipart_data=multipart_data,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    bot_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    multipart_data: SetBotIconImageMultipartData,
) -> Optional[Union[Any, StatusOK]]:
    """Set bot's LHS icon image

     Set a bot's LHS icon image based on bot_user_id string parameter. Icon image must be SVG format, all
    other formats are rejected.
    ##### Permissions
    Must have `manage_bots` permission.
    __Minimum server version__: 5.14

    Args:
        bot_user_id (str):
        multipart_data (SetBotIconImageMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            bot_user_id=bot_user_id,
            client=client,
            multipart_data=multipart_data,
        )
    ).parsed
