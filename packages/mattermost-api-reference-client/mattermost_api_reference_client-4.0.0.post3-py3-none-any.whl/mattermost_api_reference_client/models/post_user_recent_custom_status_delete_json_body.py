from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PostUserRecentCustomStatusDeleteJsonBody")


@_attrs_define
class PostUserRecentCustomStatusDeleteJsonBody:
    """
    Attributes:
        emoji (str): Any emoji
        text (str): Any custom status text
        duration (str): Duration of custom status, can be `thirty_minutes`, `one_hour`, `four_hours`, `today`,
            `this_week` or `date_and_time`
        expires_at (str): The time at which custom status should be expired. It should be in ISO format.
    """

    emoji: str
    text: str
    duration: str
    expires_at: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        emoji = self.emoji
        text = self.text
        duration = self.duration
        expires_at = self.expires_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "emoji": emoji,
                "text": text,
                "duration": duration,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        emoji = d.pop("emoji")

        text = d.pop("text")

        duration = d.pop("duration")

        expires_at = d.pop("expires_at")

        post_user_recent_custom_status_delete_json_body = cls(
            emoji=emoji,
            text=text,
            duration=duration,
            expires_at=expires_at,
        )

        post_user_recent_custom_status_delete_json_body.additional_properties = d
        return post_user_recent_custom_status_delete_json_body

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
