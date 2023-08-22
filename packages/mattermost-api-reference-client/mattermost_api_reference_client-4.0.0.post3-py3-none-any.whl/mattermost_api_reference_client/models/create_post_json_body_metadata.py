from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_post_json_body_metadata_priority import CreatePostJsonBodyMetadataPriority


T = TypeVar("T", bound="CreatePostJsonBodyMetadata")


@_attrs_define
class CreatePostJsonBodyMetadata:
    """A JSON object to add post metadata, e.g the post's priority

    Attributes:
        priority (Union[Unset, CreatePostJsonBodyMetadataPriority]): An object containing the post's priority properties
    """

    priority: Union[Unset, "CreatePostJsonBodyMetadataPriority"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        priority: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if priority is not UNSET:
            field_dict["priority"] = priority

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_post_json_body_metadata_priority import CreatePostJsonBodyMetadataPriority

        d = src_dict.copy()
        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, CreatePostJsonBodyMetadataPriority]
        if isinstance(_priority, Unset):
            priority = UNSET
        else:
            priority = CreatePostJsonBodyMetadataPriority.from_dict(_priority)

        create_post_json_body_metadata = cls(
            priority=priority,
        )

        create_post_json_body_metadata.additional_properties = d
        return create_post_json_body_metadata

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
