from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResetSamlAuthDataToEmailJsonBody")


@_attrs_define
class ResetSamlAuthDataToEmailJsonBody:
    """
    Attributes:
        include_deleted (Union[Unset, bool]): Whether to include deleted users.
        dry_run (Union[Unset, bool]): If set to true, the number of users who would be affected is returned.
        user_ids (Union[Unset, List[str]]): If set to a non-empty array, then users whose IDs are not in the array will
            be excluded.
    """

    include_deleted: Union[Unset, bool] = False
    dry_run: Union[Unset, bool] = False
    user_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        include_deleted = self.include_deleted
        dry_run = self.dry_run
        user_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.user_ids, Unset):
            user_ids = self.user_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if include_deleted is not UNSET:
            field_dict["include_deleted"] = include_deleted
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run
        if user_ids is not UNSET:
            field_dict["user_ids"] = user_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        include_deleted = d.pop("include_deleted", UNSET)

        dry_run = d.pop("dry_run", UNSET)

        user_ids = cast(List[str], d.pop("user_ids", UNSET))

        reset_saml_auth_data_to_email_json_body = cls(
            include_deleted=include_deleted,
            dry_run=dry_run,
            user_ids=user_ids,
        )

        reset_saml_auth_data_to_email_json_body.additional_properties = d
        return reset_saml_auth_data_to_email_json_body

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
