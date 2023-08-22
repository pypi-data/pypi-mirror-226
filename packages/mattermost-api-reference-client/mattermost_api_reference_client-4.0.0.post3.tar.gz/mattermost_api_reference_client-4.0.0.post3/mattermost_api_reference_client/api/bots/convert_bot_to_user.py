from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.convert_bot_to_user_json_body import ConvertBotToUserJsonBody
from ...models.status_ok import StatusOK
from ...types import UNSET, Response, Unset


def _get_kwargs(
    bot_user_id: str,
    *,
    json_body: ConvertBotToUserJsonBody,
    set_system_admin: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["set_system_admin"] = set_system_admin

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/bots/{bot_user_id}/convert_to_user".format(
            bot_user_id=bot_user_id,
        ),
        "json": json_json_body,
        "params": params,
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
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
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
    json_body: ConvertBotToUserJsonBody,
    set_system_admin: Union[Unset, None, bool] = False,
) -> Response[Union[Any, StatusOK]]:
    """Convert a bot into a user

     Convert a bot into a user.

    __Minimum server version__: 5.26

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        bot_user_id (str):
        set_system_admin (Union[Unset, None, bool]):
        json_body (ConvertBotToUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        bot_user_id=bot_user_id,
        json_body=json_body,
        set_system_admin=set_system_admin,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    bot_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ConvertBotToUserJsonBody,
    set_system_admin: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, StatusOK]]:
    """Convert a bot into a user

     Convert a bot into a user.

    __Minimum server version__: 5.26

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        bot_user_id (str):
        set_system_admin (Union[Unset, None, bool]):
        json_body (ConvertBotToUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        bot_user_id=bot_user_id,
        client=client,
        json_body=json_body,
        set_system_admin=set_system_admin,
    ).parsed


async def asyncio_detailed(
    bot_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ConvertBotToUserJsonBody,
    set_system_admin: Union[Unset, None, bool] = False,
) -> Response[Union[Any, StatusOK]]:
    """Convert a bot into a user

     Convert a bot into a user.

    __Minimum server version__: 5.26

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        bot_user_id (str):
        set_system_admin (Union[Unset, None, bool]):
        json_body (ConvertBotToUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        bot_user_id=bot_user_id,
        json_body=json_body,
        set_system_admin=set_system_admin,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    bot_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ConvertBotToUserJsonBody,
    set_system_admin: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, StatusOK]]:
    """Convert a bot into a user

     Convert a bot into a user.

    __Minimum server version__: 5.26

    ##### Permissions
    Must have `manage_system` permission.

    Args:
        bot_user_id (str):
        set_system_admin (Union[Unset, None, bool]):
        json_body (ConvertBotToUserJsonBody):

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
            json_body=json_body,
            set_system_admin=set_system_admin,
        )
    ).parsed
