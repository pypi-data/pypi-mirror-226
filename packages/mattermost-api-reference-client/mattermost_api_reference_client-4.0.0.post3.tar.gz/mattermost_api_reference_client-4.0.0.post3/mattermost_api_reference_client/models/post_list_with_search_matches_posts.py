from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.post import Post


T = TypeVar("T", bound="PostListWithSearchMatchesPosts")


@_attrs_define
class PostListWithSearchMatchesPosts:
    """ """

    additional_properties: Dict[str, "Post"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.post import Post

        d = src_dict.copy()
        post_list_with_search_matches_posts = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = Post.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        post_list_with_search_matches_posts.additional_properties = additional_properties
        return post_list_with_search_matches_posts

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "Post":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "Post") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
