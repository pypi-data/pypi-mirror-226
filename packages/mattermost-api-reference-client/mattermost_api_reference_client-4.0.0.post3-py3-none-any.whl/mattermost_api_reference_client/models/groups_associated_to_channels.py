from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.group_with_scheme_admin import GroupWithSchemeAdmin


T = TypeVar("T", bound="GroupsAssociatedToChannels")


@_attrs_define
class GroupsAssociatedToChannels:
    """a map of channel id(s) to the set of groups that constrain the corresponding channel in a team"""

    additional_properties: Dict[str, List["GroupWithSchemeAdmin"]] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = []
            for additional_property_item_data in prop:
                additional_property_item = additional_property_item_data.to_dict()

                field_dict[prop_name].append(additional_property_item)

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.group_with_scheme_admin import GroupWithSchemeAdmin

        d = src_dict.copy()
        groups_associated_to_channels = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = []
            _additional_property = prop_dict
            for additional_property_item_data in _additional_property:
                additional_property_item = GroupWithSchemeAdmin.from_dict(additional_property_item_data)

                additional_property.append(additional_property_item)

            additional_properties[prop_name] = additional_property

        groups_associated_to_channels.additional_properties = additional_properties
        return groups_associated_to_channels

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> List["GroupWithSchemeAdmin"]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: List["GroupWithSchemeAdmin"]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
