from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddChannelMemberJsonBody")


@_attrs_define
class AddChannelMemberJsonBody:
    """
    Attributes:
        user_id (str): The ID of user to add into the channel
        post_root_id (Union[Unset, str]): The ID of root post where link to add channel member originates
    """

    user_id: str
    post_root_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        post_root_id = self.post_root_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
            }
        )
        if post_root_id is not UNSET:
            field_dict["post_root_id"] = post_root_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("user_id")

        post_root_id = d.pop("post_root_id", UNSET)

        add_channel_member_json_body = cls(
            user_id=user_id,
            post_root_id=post_root_id,
        )

        add_channel_member_json_body.additional_properties = d
        return add_channel_member_json_body

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
