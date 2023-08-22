from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_group_json_body_group import CreateGroupJsonBodyGroup


T = TypeVar("T", bound="CreateGroupJsonBody")


@_attrs_define
class CreateGroupJsonBody:
    """
    Attributes:
        group (CreateGroupJsonBodyGroup): Group object to create.
        user_ids (List[str]): The user ids of the group members to add.
    """

    group: "CreateGroupJsonBodyGroup"
    user_ids: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        group = self.group.to_dict()

        user_ids = self.user_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group": group,
                "user_ids": user_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_group_json_body_group import CreateGroupJsonBodyGroup

        d = src_dict.copy()
        group = CreateGroupJsonBodyGroup.from_dict(d.pop("group"))

        user_ids = cast(List[str], d.pop("user_ids"))

        create_group_json_body = cls(
            group=group,
            user_ids=user_ids,
        )

        create_group_json_body.additional_properties = d
        return create_group_json_body

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
