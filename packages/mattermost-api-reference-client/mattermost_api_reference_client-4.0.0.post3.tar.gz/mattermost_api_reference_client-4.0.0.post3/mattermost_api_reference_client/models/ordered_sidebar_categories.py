from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sidebar_category_with_channels import SidebarCategoryWithChannels


T = TypeVar("T", bound="OrderedSidebarCategories")


@_attrs_define
class OrderedSidebarCategories:
    """List of user's categories with their channels

    Attributes:
        order (Union[Unset, List[str]]):
        categories (Union[Unset, List['SidebarCategoryWithChannels']]):
    """

    order: Union[Unset, List[str]] = UNSET
    categories: Union[Unset, List["SidebarCategoryWithChannels"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        order: Union[Unset, List[str]] = UNSET
        if not isinstance(self.order, Unset):
            order = self.order

        categories: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()

                categories.append(categories_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order is not UNSET:
            field_dict["order"] = order
        if categories is not UNSET:
            field_dict["categories"] = categories

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sidebar_category_with_channels import SidebarCategoryWithChannels

        d = src_dict.copy()
        order = cast(List[str], d.pop("order", UNSET))

        categories = []
        _categories = d.pop("categories", UNSET)
        for categories_item_data in _categories or []:
            categories_item = SidebarCategoryWithChannels.from_dict(categories_item_data)

            categories.append(categories_item)

        ordered_sidebar_categories = cls(
            order=order,
            categories=categories,
        )

        ordered_sidebar_categories.additional_properties = d
        return ordered_sidebar_categories

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
