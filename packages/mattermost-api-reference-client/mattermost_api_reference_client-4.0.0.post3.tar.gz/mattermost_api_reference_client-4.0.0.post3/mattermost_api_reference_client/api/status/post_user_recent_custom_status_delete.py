from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_user_recent_custom_status_delete_json_body import PostUserRecentCustomStatusDeleteJsonBody
from ...types import Response


def _get_kwargs(
    user_id: str,
    *,
    json_body: PostUserRecentCustomStatusDeleteJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/users/{user_id}/status/custom/recent/delete".format(
            user_id=user_id,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PostUserRecentCustomStatusDeleteJsonBody,
) -> Response[Any]:
    """Delete user's recent custom status

     Deletes a user's recent custom status by removing the specific status from the recentCustomStatuses
    in the user's props and updates the user.
    ##### Permissions
    Must be logged in as the user whose recent custom status is being deleted.

    Args:
        user_id (str):
        json_body (PostUserRecentCustomStatusDeleteJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PostUserRecentCustomStatusDeleteJsonBody,
) -> Response[Any]:
    """Delete user's recent custom status

     Deletes a user's recent custom status by removing the specific status from the recentCustomStatuses
    in the user's props and updates the user.
    ##### Permissions
    Must be logged in as the user whose recent custom status is being deleted.

    Args:
        user_id (str):
        json_body (PostUserRecentCustomStatusDeleteJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
