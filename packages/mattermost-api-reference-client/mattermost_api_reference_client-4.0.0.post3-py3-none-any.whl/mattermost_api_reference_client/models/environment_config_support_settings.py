from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EnvironmentConfigSupportSettings")


@_attrs_define
class EnvironmentConfigSupportSettings:
    """
    Attributes:
        terms_of_service_link (Union[Unset, bool]):
        privacy_policy_link (Union[Unset, bool]):
        about_link (Union[Unset, bool]):
        help_link (Union[Unset, bool]):
        report_a_problem_link (Union[Unset, bool]):
        support_email (Union[Unset, bool]):
    """

    terms_of_service_link: Union[Unset, bool] = UNSET
    privacy_policy_link: Union[Unset, bool] = UNSET
    about_link: Union[Unset, bool] = UNSET
    help_link: Union[Unset, bool] = UNSET
    report_a_problem_link: Union[Unset, bool] = UNSET
    support_email: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        terms_of_service_link = self.terms_of_service_link
        privacy_policy_link = self.privacy_policy_link
        about_link = self.about_link
        help_link = self.help_link
        report_a_problem_link = self.report_a_problem_link
        support_email = self.support_email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if terms_of_service_link is not UNSET:
            field_dict["TermsOfServiceLink"] = terms_of_service_link
        if privacy_policy_link is not UNSET:
            field_dict["PrivacyPolicyLink"] = privacy_policy_link
        if about_link is not UNSET:
            field_dict["AboutLink"] = about_link
        if help_link is not UNSET:
            field_dict["HelpLink"] = help_link
        if report_a_problem_link is not UNSET:
            field_dict["ReportAProblemLink"] = report_a_problem_link
        if support_email is not UNSET:
            field_dict["SupportEmail"] = support_email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        terms_of_service_link = d.pop("TermsOfServiceLink", UNSET)

        privacy_policy_link = d.pop("PrivacyPolicyLink", UNSET)

        about_link = d.pop("AboutLink", UNSET)

        help_link = d.pop("HelpLink", UNSET)

        report_a_problem_link = d.pop("ReportAProblemLink", UNSET)

        support_email = d.pop("SupportEmail", UNSET)

        environment_config_support_settings = cls(
            terms_of_service_link=terms_of_service_link,
            privacy_policy_link=privacy_policy_link,
            about_link=about_link,
            help_link=help_link,
            report_a_problem_link=report_a_problem_link,
            support_email=support_email,
        )

        environment_config_support_settings.additional_properties = d
        return environment_config_support_settings

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
