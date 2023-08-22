from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.item_set_state_json_body_new_state import ItemSetStateJsonBodyNewState

T = TypeVar("T", bound="ItemSetStateJsonBody")


@_attrs_define
class ItemSetStateJsonBody:
    """
    Attributes:
        new_state (ItemSetStateJsonBodyNewState): The new state of the item. Default:
            ItemSetStateJsonBodyNewState.VALUE_0. Example: closed.
    """

    new_state: ItemSetStateJsonBodyNewState = ItemSetStateJsonBodyNewState.VALUE_0
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        new_state = self.new_state.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_state": new_state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_state = ItemSetStateJsonBodyNewState(d.pop("new_state"))

        item_set_state_json_body = cls(
            new_state=new_state,
        )

        item_set_state_json_body.additional_properties = d
        return item_set_state_json_body

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
