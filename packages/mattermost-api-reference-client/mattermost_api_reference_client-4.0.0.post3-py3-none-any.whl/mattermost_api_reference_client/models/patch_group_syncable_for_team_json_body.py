from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchGroupSyncableForTeamJsonBody")


@_attrs_define
class PatchGroupSyncableForTeamJsonBody:
    """
    Attributes:
        auto_add (Union[Unset, bool]):
    """

    auto_add: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        auto_add = self.auto_add

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_add is not UNSET:
            field_dict["auto_add"] = auto_add

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        auto_add = d.pop("auto_add", UNSET)

        patch_group_syncable_for_team_json_body = cls(
            auto_add=auto_add,
        )

        patch_group_syncable_for_team_json_body.additional_properties = d
        return patch_group_syncable_for_team_json_body

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
