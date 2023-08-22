from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_playbook_json_body_checklists_item_items_item import (
        CreatePlaybookJsonBodyChecklistsItemItemsItem,
    )


T = TypeVar("T", bound="CreatePlaybookJsonBodyChecklistsItem")


@_attrs_define
class CreatePlaybookJsonBodyChecklistsItem:
    """
    Attributes:
        title (str): The title of the checklist. Example: Triage issue.
        items (List['CreatePlaybookJsonBodyChecklistsItemItemsItem']): The list of tasks to do.
    """

    title: str
    items: List["CreatePlaybookJsonBodyChecklistsItemItemsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()

            items.append(items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_playbook_json_body_checklists_item_items_item import (
            CreatePlaybookJsonBodyChecklistsItemItemsItem,
        )

        d = src_dict.copy()
        title = d.pop("title")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = CreatePlaybookJsonBodyChecklistsItemItemsItem.from_dict(items_item_data)

            items.append(items_item)

        create_playbook_json_body_checklists_item = cls(
            title=title,
            items=items,
        )

        create_playbook_json_body_checklists_item.additional_properties = d
        return create_playbook_json_body_checklists_item

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
