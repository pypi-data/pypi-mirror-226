from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChannelModeratedRolesPatch")


@_attrs_define
class ChannelModeratedRolesPatch:
    """
    Attributes:
        guests (Union[Unset, bool]):
        members (Union[Unset, bool]):
    """

    guests: Union[Unset, bool] = UNSET
    members: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        guests = self.guests
        members = self.members

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if guests is not UNSET:
            field_dict["guests"] = guests
        if members is not UNSET:
            field_dict["members"] = members

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        guests = d.pop("guests", UNSET)

        members = d.pop("members", UNSET)

        channel_moderated_roles_patch = cls(
            guests=guests,
            members=members,
        )

        channel_moderated_roles_patch.additional_properties = d
        return channel_moderated_roles_patch

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
