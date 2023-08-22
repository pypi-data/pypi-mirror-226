from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.migrate_auth_to_saml_json_body_matches import MigrateAuthToSamlJsonBodyMatches


T = TypeVar("T", bound="MigrateAuthToSamlJsonBody")


@_attrs_define
class MigrateAuthToSamlJsonBody:
    """
    Attributes:
        from_ (str): The current authentication type for the matched users.
        matches (MigrateAuthToSamlJsonBodyMatches): Users map.
        auto (bool):
    """

    from_: str
    matches: "MigrateAuthToSamlJsonBodyMatches"
    auto: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from_ = self.from_
        matches = self.matches.to_dict()

        auto = self.auto

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "matches": matches,
                "auto": auto,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.migrate_auth_to_saml_json_body_matches import MigrateAuthToSamlJsonBodyMatches

        d = src_dict.copy()
        from_ = d.pop("from")

        matches = MigrateAuthToSamlJsonBodyMatches.from_dict(d.pop("matches"))

        auto = d.pop("auto")

        migrate_auth_to_saml_json_body = cls(
            from_=from_,
            matches=matches,
            auto=auto,
        )

        migrate_auth_to_saml_json_body.additional_properties = d
        return migrate_auth_to_saml_json_body

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
