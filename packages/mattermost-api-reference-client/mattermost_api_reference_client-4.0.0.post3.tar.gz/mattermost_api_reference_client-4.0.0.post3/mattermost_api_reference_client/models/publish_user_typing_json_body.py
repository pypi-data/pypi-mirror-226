from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PublishUserTypingJsonBody")


@_attrs_define
class PublishUserTypingJsonBody:
    """
    Attributes:
        channel_id (str): The id of the channel to which to direct the typing event.
        parent_id (Union[Unset, str]): The optional id of the root post of the thread to which the user is replying. If
            unset, the typing event is directed at the entire channel.
    """

    channel_id: str
    parent_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel_id = self.channel_id
        parent_id = self.parent_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel_id": channel_id,
            }
        )
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        channel_id = d.pop("channel_id")

        parent_id = d.pop("parent_id", UNSET)

        publish_user_typing_json_body = cls(
            channel_id=channel_id,
            parent_id=parent_id,
        )

        publish_user_typing_json_body.additional_properties = d
        return publish_user_typing_json_body

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
