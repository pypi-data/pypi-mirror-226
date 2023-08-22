from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_checklist_item_json_body import AddChecklistItemJsonBody
from ...types import Response


def _get_kwargs(
    id: str,
    checklist: int,
    *,
    json_body: AddChecklistItemJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/plugins/playbooks/api/v0/runs/{id}/checklists/{checklist}/add".format(
            id=id,
            checklist=checklist,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
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
    id: str,
    checklist: int,
    *,
    client: AuthenticatedClient,
    json_body: AddChecklistItemJsonBody,
) -> Response[Any]:
    """Add an item to a playbook run's checklist

     The most common pattern to add a new item is to only send its title as the request payload. By
    default, it is an open item, with no assignee and no slash command.

    Args:
        id (str):
        checklist (int):
        json_body (AddChecklistItemJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        checklist=checklist,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: str,
    checklist: int,
    *,
    client: AuthenticatedClient,
    json_body: AddChecklistItemJsonBody,
) -> Response[Any]:
    """Add an item to a playbook run's checklist

     The most common pattern to add a new item is to only send its title as the request payload. By
    default, it is an open item, with no assignee and no slash command.

    Args:
        id (str):
        checklist (int):
        json_body (AddChecklistItemJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        checklist=checklist,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
