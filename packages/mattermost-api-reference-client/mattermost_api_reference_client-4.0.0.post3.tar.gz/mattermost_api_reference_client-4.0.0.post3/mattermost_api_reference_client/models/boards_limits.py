from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BoardsLimits")


@_attrs_define
class BoardsLimits:
    """
    Attributes:
        cards (Union[Unset, None, int]):
        views (Union[Unset, None, int]):
    """

    cards: Union[Unset, None, int] = UNSET
    views: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cards = self.cards
        views = self.views

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cards is not UNSET:
            field_dict["cards"] = cards
        if views is not UNSET:
            field_dict["views"] = views

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cards = d.pop("cards", UNSET)

        views = d.pop("views", UNSET)

        boards_limits = cls(
            cards=cards,
            views=views,
        )

        boards_limits.additional_properties = d
        return boards_limits

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
