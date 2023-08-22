from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateUserPasswordJsonBody")


@_attrs_define
class UpdateUserPasswordJsonBody:
    """
    Attributes:
        new_password (str): The new password for the user
        current_password (Union[Unset, str]): The current password for the user
    """

    new_password: str
    current_password: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        new_password = self.new_password
        current_password = self.current_password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_password": new_password,
            }
        )
        if current_password is not UNSET:
            field_dict["current_password"] = current_password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_password = d.pop("new_password")

        current_password = d.pop("current_password", UNSET)

        update_user_password_json_body = cls(
            new_password=new_password,
            current_password=current_password,
        )

        update_user_password_json_body.additional_properties = d
        return update_user_password_json_body

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
