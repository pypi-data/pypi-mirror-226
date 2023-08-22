from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSamlMetadataFromIdpJsonBody")


@_attrs_define
class GetSamlMetadataFromIdpJsonBody:
    """
    Attributes:
        saml_metadata_url (Union[Unset, str]): The URL from which to retrieve the SAML IDP data.
    """

    saml_metadata_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        saml_metadata_url = self.saml_metadata_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if saml_metadata_url is not UNSET:
            field_dict["saml_metadata_url"] = saml_metadata_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        saml_metadata_url = d.pop("saml_metadata_url", UNSET)

        get_saml_metadata_from_idp_json_body = cls(
            saml_metadata_url=saml_metadata_url,
        )

        get_saml_metadata_from_idp_json_body.additional_properties = d
        return get_saml_metadata_from_idp_json_body

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
