from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bot import Bot
from ...types import UNSET, Response, Unset


def _get_kwargs(
    bot_user_id: str,
    *,
    include_deleted: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["include_deleted"] = include_deleted

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/bots/{bot_user_id}".format(
            bot_user_id=bot_user_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Bot]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Bot.from_dict(response.json())

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
) -> Response[Union[Any, Bot]]:
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
    include_deleted: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, Bot]]:
    """Get a bot

     Get a bot specified by its bot id.
    ##### Permissions
    Must have `read_bots` permission for bots you are managing, and `read_others_bots` permission for
    bots others are managing.
    __Minimum server version__: 5.10

    Args:
        bot_user_id (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Bot]]
    """

    kwargs = _get_kwargs(
        bot_user_id=bot_user_id,
        include_deleted=include_deleted,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    bot_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, Bot]]:
    """Get a bot

     Get a bot specified by its bot id.
    ##### Permissions
    Must have `read_bots` permission for bots you are managing, and `read_others_bots` permission for
    bots others are managing.
    __Minimum server version__: 5.10

    Args:
        bot_user_id (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Bot]
    """

    return sync_detailed(
        bot_user_id=bot_user_id,
        client=client,
        include_deleted=include_deleted,
    ).parsed


async def asyncio_detailed(
    bot_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, Bot]]:
    """Get a bot

     Get a bot specified by its bot id.
    ##### Permissions
    Must have `read_bots` permission for bots you are managing, and `read_others_bots` permission for
    bots others are managing.
    __Minimum server version__: 5.10

    Args:
        bot_user_id (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Bot]]
    """

    kwargs = _get_kwargs(
        bot_user_id=bot_user_id,
        include_deleted=include_deleted,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    bot_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, Bot]]:
    """Get a bot

     Get a bot specified by its bot id.
    ##### Permissions
    Must have `read_bots` permission for bots you are managing, and `read_others_bots` permission for
    bots others are managing.
    __Minimum server version__: 5.10

    Args:
        bot_user_id (str):
        include_deleted (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Bot]
    """

    return (
        await asyncio_detailed(
            bot_user_id=bot_user_id,
            client=client,
            include_deleted=include_deleted,
        )
    ).parsed
