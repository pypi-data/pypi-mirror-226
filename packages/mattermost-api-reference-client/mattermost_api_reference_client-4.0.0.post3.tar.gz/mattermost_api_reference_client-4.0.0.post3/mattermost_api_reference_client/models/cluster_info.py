from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ClusterInfo")


@_attrs_define
class ClusterInfo:
    """
    Attributes:
        id (Union[Unset, str]): The unique ID for the node
        version (Union[Unset, str]): The server version the node is on
        config_hash (Union[Unset, str]): The hash of the configuartion file the node is using
        internode_url (Union[Unset, str]): The URL used to communicate with those node from other nodes
        hostname (Union[Unset, str]): The hostname for this node
        last_ping (Union[Unset, int]): The time of the last ping to this node
        is_alive (Union[Unset, bool]): Whether or not the node is alive and well
    """

    id: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    config_hash: Union[Unset, str] = UNSET
    internode_url: Union[Unset, str] = UNSET
    hostname: Union[Unset, str] = UNSET
    last_ping: Union[Unset, int] = UNSET
    is_alive: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        version = self.version
        config_hash = self.config_hash
        internode_url = self.internode_url
        hostname = self.hostname
        last_ping = self.last_ping
        is_alive = self.is_alive

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if version is not UNSET:
            field_dict["version"] = version
        if config_hash is not UNSET:
            field_dict["config_hash"] = config_hash
        if internode_url is not UNSET:
            field_dict["internode_url"] = internode_url
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if last_ping is not UNSET:
            field_dict["last_ping"] = last_ping
        if is_alive is not UNSET:
            field_dict["is_alive"] = is_alive

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        version = d.pop("version", UNSET)

        config_hash = d.pop("config_hash", UNSET)

        internode_url = d.pop("internode_url", UNSET)

        hostname = d.pop("hostname", UNSET)

        last_ping = d.pop("last_ping", UNSET)

        is_alive = d.pop("is_alive", UNSET)

        cluster_info = cls(
            id=id,
            version=version,
            config_hash=config_hash,
            internode_url=internode_url,
            hostname=hostname,
            last_ping=last_ping,
            is_alive=is_alive,
        )

        cluster_info.additional_properties = d
        return cluster_info

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
