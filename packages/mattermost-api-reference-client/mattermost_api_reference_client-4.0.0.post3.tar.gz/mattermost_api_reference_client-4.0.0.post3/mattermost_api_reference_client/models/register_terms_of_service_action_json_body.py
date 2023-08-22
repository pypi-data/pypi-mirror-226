from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RegisterTermsOfServiceActionJsonBody")


@_attrs_define
class RegisterTermsOfServiceActionJsonBody:
    """
    Attributes:
        service_terms_id (str): terms of service ID on which the user is acting on
        accepted (str): true or false, indicates whether the user accepted or rejected the terms of service.
    """

    service_terms_id: str
    accepted: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        service_terms_id = self.service_terms_id
        accepted = self.accepted

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "serviceTermsId": service_terms_id,
                "accepted": accepted,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        service_terms_id = d.pop("serviceTermsId")

        accepted = d.pop("accepted")

        register_terms_of_service_action_json_body = cls(
            service_terms_id=service_terms_id,
            accepted=accepted,
        )

        register_terms_of_service_action_json_body.additional_properties = d
        return register_terms_of_service_action_json_body

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
