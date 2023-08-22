from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.team import Team
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    include_total_count: Union[Unset, None, bool] = False,
    exclude_policy_constrained: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["per_page"] = per_page

    params["include_total_count"] = include_total_count

    params["exclude_policy_constrained"] = exclude_policy_constrained

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v4/teams",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["Team"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Team.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, List["Team"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    include_total_count: Union[Unset, None, bool] = False,
    exclude_policy_constrained: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List["Team"]]]:
    r"""Get teams

     For regular users only returns open teams. Users with the \"manage_system\" permission will return
    teams regardless of type. The result is based on query string parameters - page and per_page.
    ##### Permissions
    Must be authenticated. \"manage_system\" permission is required to show all teams.

    Args:
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        include_total_count (Union[Unset, None, bool]):
        exclude_policy_constrained (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Team']]]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        include_total_count=include_total_count,
        exclude_policy_constrained=exclude_policy_constrained,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    include_total_count: Union[Unset, None, bool] = False,
    exclude_policy_constrained: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List["Team"]]]:
    r"""Get teams

     For regular users only returns open teams. Users with the \"manage_system\" permission will return
    teams regardless of type. The result is based on query string parameters - page and per_page.
    ##### Permissions
    Must be authenticated. \"manage_system\" permission is required to show all teams.

    Args:
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        include_total_count (Union[Unset, None, bool]):
        exclude_policy_constrained (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Team']]
    """

    return sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        include_total_count=include_total_count,
        exclude_policy_constrained=exclude_policy_constrained,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    include_total_count: Union[Unset, None, bool] = False,
    exclude_policy_constrained: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List["Team"]]]:
    r"""Get teams

     For regular users only returns open teams. Users with the \"manage_system\" permission will return
    teams regardless of type. The result is based on query string parameters - page and per_page.
    ##### Permissions
    Must be authenticated. \"manage_system\" permission is required to show all teams.

    Args:
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        include_total_count (Union[Unset, None, bool]):
        exclude_policy_constrained (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Team']]]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        include_total_count=include_total_count,
        exclude_policy_constrained=exclude_policy_constrained,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 0,
    per_page: Union[Unset, None, int] = 60,
    include_total_count: Union[Unset, None, bool] = False,
    exclude_policy_constrained: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List["Team"]]]:
    r"""Get teams

     For regular users only returns open teams. Users with the \"manage_system\" permission will return
    teams regardless of type. The result is based on query string parameters - page and per_page.
    ##### Permissions
    Must be authenticated. \"manage_system\" permission is required to show all teams.

    Args:
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):  Default: 60.
        include_total_count (Union[Unset, None, bool]):
        exclude_policy_constrained (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Team']]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            per_page=per_page,
            include_total_count=include_total_count,
            exclude_policy_constrained=exclude_policy_constrained,
        )
    ).parsed
