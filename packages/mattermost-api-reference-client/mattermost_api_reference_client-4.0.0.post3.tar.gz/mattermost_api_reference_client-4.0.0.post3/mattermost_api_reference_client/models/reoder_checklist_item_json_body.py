from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ReoderChecklistItemJsonBody")


@_attrs_define
class ReoderChecklistItemJsonBody:
    """
    Attributes:
        item_num (int): Zero-based index of the item to reorder. Example: 2.
        new_location (int): Zero-based index of the new place to move the item to. Example: 2.
    """

    item_num: int
    new_location: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        item_num = self.item_num
        new_location = self.new_location

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "item_num": item_num,
                "new_location": new_location,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        item_num = d.pop("item_num")

        new_location = d.pop("new_location")

        reoder_checklist_item_json_body = cls(
            item_num=item_num,
            new_location=new_location,
        )

        reoder_checklist_item_json_body.additional_properties = d
        return reoder_checklist_item_json_body

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
