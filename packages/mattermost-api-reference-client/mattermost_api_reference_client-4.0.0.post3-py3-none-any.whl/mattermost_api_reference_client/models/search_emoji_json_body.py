from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchEmojiJsonBody")


@_attrs_define
class SearchEmojiJsonBody:
    """
    Attributes:
        term (str): The term to match against the emoji name.
        prefix_only (Union[Unset, str]): Set to only search for names starting with the search term.
    """

    term: str
    prefix_only: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        term = self.term
        prefix_only = self.prefix_only

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "term": term,
            }
        )
        if prefix_only is not UNSET:
            field_dict["prefix_only"] = prefix_only

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        term = d.pop("term")

        prefix_only = d.pop("prefix_only", UNSET)

        search_emoji_json_body = cls(
            term=term,
            prefix_only=prefix_only,
        )

        search_emoji_json_body.additional_properties = d
        return search_emoji_json_body

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
