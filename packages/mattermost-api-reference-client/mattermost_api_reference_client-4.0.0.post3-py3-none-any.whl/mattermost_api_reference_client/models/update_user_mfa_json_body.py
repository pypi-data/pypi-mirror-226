from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateUserMfaJsonBody")


@_attrs_define
class UpdateUserMfaJsonBody:
    """
    Attributes:
        activate (bool): Use `true` to activate, `false` to deactivate
        code (Union[Unset, str]): The code produced by your MFA client. Required if `activate` is true
    """

    activate: bool
    code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        activate = self.activate
        code = self.code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "activate": activate,
            }
        )
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        activate = d.pop("activate")

        code = d.pop("code", UNSET)

        update_user_mfa_json_body = cls(
            activate=activate,
            code=code,
        )

        update_user_mfa_json_body.additional_properties = d
        return update_user_mfa_json_body

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
