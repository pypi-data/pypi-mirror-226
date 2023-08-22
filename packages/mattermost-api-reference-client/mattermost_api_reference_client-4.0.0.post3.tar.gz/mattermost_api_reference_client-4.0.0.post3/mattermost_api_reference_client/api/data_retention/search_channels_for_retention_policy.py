from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.channel_with_team_data import ChannelWithTeamData
from ...models.search_channels_for_retention_policy_json_body import SearchChannelsForRetentionPolicyJsonBody
from ...types import Response


def _get_kwargs(
    policy_id: str,
    *,
    json_body: SearchChannelsForRetentionPolicyJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v4/data_retention/policies/{policy_id}/channels/search".format(
            policy_id=policy_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["ChannelWithTeamData"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_channel_list_with_team_data_item_data in _response_200:
            componentsschemas_channel_list_with_team_data_item = ChannelWithTeamData.from_dict(
                componentsschemas_channel_list_with_team_data_item_data
            )

            response_200.append(componentsschemas_channel_list_with_team_data_item)

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
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
) -> Response[Union[Any, List["ChannelWithTeamData"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    policy_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchChannelsForRetentionPolicyJsonBody,
) -> Response[Union[Any, List["ChannelWithTeamData"]]]:
    """Search for the channels in a granular data retention policy

     Searches for the channels to which a granular data retention policy is applied.

    __Minimum server version__: 5.35

    ##### Permissions
    Must have the `sysconsole_read_compliance_data_retention` permission.

    ##### License
    Requires an E20 license.

    Args:
        policy_id (str):
        json_body (SearchChannelsForRetentionPolicyJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['ChannelWithTeamData']]]
    """

    kwargs = _get_kwargs(
        policy_id=policy_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    policy_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchChannelsForRetentionPolicyJsonBody,
) -> Optional[Union[Any, List["ChannelWithTeamData"]]]:
    """Search for the channels in a granular data retention policy

     Searches for the channels to which a granular data retention policy is applied.

    __Minimum server version__: 5.35

    ##### Permissions
    Must have the `sysconsole_read_compliance_data_retention` permission.

    ##### License
    Requires an E20 license.

    Args:
        policy_id (str):
        json_body (SearchChannelsForRetentionPolicyJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['ChannelWithTeamData']]
    """

    return sync_detailed(
        policy_id=policy_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    policy_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchChannelsForRetentionPolicyJsonBody,
) -> Response[Union[Any, List["ChannelWithTeamData"]]]:
    """Search for the channels in a granular data retention policy

     Searches for the channels to which a granular data retention policy is applied.

    __Minimum server version__: 5.35

    ##### Permissions
    Must have the `sysconsole_read_compliance_data_retention` permission.

    ##### License
    Requires an E20 license.

    Args:
        policy_id (str):
        json_body (SearchChannelsForRetentionPolicyJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['ChannelWithTeamData']]]
    """

    kwargs = _get_kwargs(
        policy_id=policy_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    policy_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SearchChannelsForRetentionPolicyJsonBody,
) -> Optional[Union[Any, List["ChannelWithTeamData"]]]:
    """Search for the channels in a granular data retention policy

     Searches for the channels to which a granular data retention policy is applied.

    __Minimum server version__: 5.35

    ##### Permissions
    Must have the `sysconsole_read_compliance_data_retention` permission.

    ##### License
    Requires an E20 license.

    Args:
        policy_id (str):
        json_body (SearchChannelsForRetentionPolicyJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['ChannelWithTeamData']]
    """

    return (
        await asyncio_detailed(
            policy_id=policy_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
