from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import File, Unset

T = TypeVar("T", bound="CreateEmojiMultipartData")


@_attrs_define
class CreateEmojiMultipartData:
    """
    Attributes:
        image (File): A file to be uploaded
        emoji (str): A JSON object containing a `name` field with the name of the emoji and a `creator_id` field with
            the id of the authenticated user.
    """

    image: File
    emoji: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        image = self.image.to_tuple()

        emoji = self.emoji

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
                "emoji": emoji,
            }
        )

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        image = self.image.to_tuple()

        emoji = self.emoji if isinstance(self.emoji, Unset) else (None, str(self.emoji).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "image": image,
                "emoji": emoji,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        image = File(payload=BytesIO(d.pop("image")))

        emoji = d.pop("emoji")

        create_emoji_multipart_data = cls(
            image=image,
            emoji=emoji,
        )

        create_emoji_multipart_data.additional_properties = d
        return create_emoji_multipart_data

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
