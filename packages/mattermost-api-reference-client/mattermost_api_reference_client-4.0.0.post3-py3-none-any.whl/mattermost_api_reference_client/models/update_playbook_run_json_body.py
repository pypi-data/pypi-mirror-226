from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdatePlaybookRunJsonBody")


@_attrs_define
class UpdatePlaybookRunJsonBody:
    """
    Attributes:
        active_stage (Union[Unset, int]): Zero-based index of the stage that will be made active. Example: 2.
    """

    active_stage: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        active_stage = self.active_stage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if active_stage is not UNSET:
            field_dict["active_stage"] = active_stage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        active_stage = d.pop("active_stage", UNSET)

        update_playbook_run_json_body = cls(
            active_stage=active_stage,
        )

        update_playbook_run_json_body.additional_properties = d
        return update_playbook_run_json_body

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
