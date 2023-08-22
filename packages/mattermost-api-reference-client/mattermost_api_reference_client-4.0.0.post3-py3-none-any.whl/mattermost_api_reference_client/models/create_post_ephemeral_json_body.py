from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_post_ephemeral_json_body_post import CreatePostEphemeralJsonBodyPost


T = TypeVar("T", bound="CreatePostEphemeralJsonBody")


@_attrs_define
class CreatePostEphemeralJsonBody:
    """
    Attributes:
        user_id (str): The target user id for the ephemeral post
        post (CreatePostEphemeralJsonBodyPost): Post object to create
    """

    user_id: str
    post: "CreatePostEphemeralJsonBodyPost"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        post = self.post.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "post": post,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_post_ephemeral_json_body_post import CreatePostEphemeralJsonBodyPost

        d = src_dict.copy()
        user_id = d.pop("user_id")

        post = CreatePostEphemeralJsonBodyPost.from_dict(d.pop("post"))

        create_post_ephemeral_json_body = cls(
            user_id=user_id,
            post=post,
        )

        create_post_ephemeral_json_body.additional_properties = d
        return create_post_ephemeral_json_body

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
