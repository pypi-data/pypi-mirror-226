from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_group_members_json_body import DeleteGroupMembersJsonBody
from ...models.status_ok import StatusOK
from ...types import Response


def _get_kwargs(
    group_id: str,
    *,
    json_body: DeleteGroupMembersJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "delete",
        "url": "/api/v4/groups/{group_id}/members".format(
            group_id=group_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, StatusOK]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = StatusOK.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
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
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DeleteGroupMembersJsonBody,
) -> Response[Union[Any, StatusOK]]:
    """Removes members from a custom group

     Soft deletes a custom group members.

    ##### Permissions
    Must have `custom_group_manage_members` permission for the given group.

    __Minimum server version__: 6.3

    Args:
        group_id (str):
        json_body (DeleteGroupMembersJsonBody): An object containing the user ids of the members
            to remove.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DeleteGroupMembersJsonBody,
) -> Optional[Union[Any, StatusOK]]:
    """Removes members from a custom group

     Soft deletes a custom group members.

    ##### Permissions
    Must have `custom_group_manage_members` permission for the given group.

    __Minimum server version__: 6.3

    Args:
        group_id (str):
        json_body (DeleteGroupMembersJsonBody): An object containing the user ids of the members
            to remove.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DeleteGroupMembersJsonBody,
) -> Response[Union[Any, StatusOK]]:
    """Removes members from a custom group

     Soft deletes a custom group members.

    ##### Permissions
    Must have `custom_group_manage_members` permission for the given group.

    __Minimum server version__: 6.3

    Args:
        group_id (str):
        json_body (DeleteGroupMembersJsonBody): An object containing the user ids of the members
            to remove.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, StatusOK]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: DeleteGroupMembersJsonBody,
) -> Optional[Union[Any, StatusOK]]:
    """Removes members from a custom group

     Soft deletes a custom group members.

    ##### Permissions
    Must have `custom_group_manage_members` permission for the given group.

    __Minimum server version__: 6.3

    Args:
        group_id (str):
        json_body (DeleteGroupMembersJsonBody): An object containing the user ids of the members
            to remove.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, StatusOK]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
