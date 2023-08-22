from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MigrateAuthToLdapJsonBody")


@_attrs_define
class MigrateAuthToLdapJsonBody:
    """
    Attributes:
        from_ (str): The current authentication type for the matched users.
        match_field (str): Foreign user field name to match.
        force (bool):
    """

    from_: str
    match_field: str
    force: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from_ = self.from_
        match_field = self.match_field
        force = self.force

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "match_field": match_field,
                "force": force,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        from_ = d.pop("from")

        match_field = d.pop("match_field")

        force = d.pop("force")

        migrate_auth_to_ldap_json_body = cls(
            from_=from_,
            match_field=match_field,
            force=force,
        )

        migrate_auth_to_ldap_json_body.additional_properties = d
        return migrate_auth_to_ldap_json_body

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
