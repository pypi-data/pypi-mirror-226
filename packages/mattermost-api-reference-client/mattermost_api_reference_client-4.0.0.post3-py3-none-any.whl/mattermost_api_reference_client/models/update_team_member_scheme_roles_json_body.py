from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UpdateTeamMemberSchemeRolesJsonBody")


@_attrs_define
class UpdateTeamMemberSchemeRolesJsonBody:
    """
    Attributes:
        scheme_admin (bool):
        scheme_user (bool):
    """

    scheme_admin: bool
    scheme_user: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scheme_admin = self.scheme_admin
        scheme_user = self.scheme_user

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scheme_admin": scheme_admin,
                "scheme_user": scheme_user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scheme_admin = d.pop("scheme_admin")

        scheme_user = d.pop("scheme_user")

        update_team_member_scheme_roles_json_body = cls(
            scheme_admin=scheme_admin,
            scheme_user=scheme_user,
        )

        update_team_member_scheme_roles_json_body.additional_properties = d
        return update_team_member_scheme_roles_json_body

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
