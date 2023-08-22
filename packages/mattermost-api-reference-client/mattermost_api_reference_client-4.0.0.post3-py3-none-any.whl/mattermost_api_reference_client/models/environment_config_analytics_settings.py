from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EnvironmentConfigAnalyticsSettings")


@_attrs_define
class EnvironmentConfigAnalyticsSettings:
    """
    Attributes:
        max_users_for_statistics (Union[Unset, bool]):
    """

    max_users_for_statistics: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        max_users_for_statistics = self.max_users_for_statistics

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_users_for_statistics is not UNSET:
            field_dict["MaxUsersForStatistics"] = max_users_for_statistics

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        max_users_for_statistics = d.pop("MaxUsersForStatistics", UNSET)

        environment_config_analytics_settings = cls(
            max_users_for_statistics=max_users_for_statistics,
        )

        environment_config_analytics_settings.additional_properties = d
        return environment_config_analytics_settings

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
