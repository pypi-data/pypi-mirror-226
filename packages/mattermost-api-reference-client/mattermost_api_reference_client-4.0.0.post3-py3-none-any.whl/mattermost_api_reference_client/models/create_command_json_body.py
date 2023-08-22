from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateCommandJsonBody")


@_attrs_define
class CreateCommandJsonBody:
    """
    Attributes:
        team_id (str): Team ID to where the command should be created
        method (str): `'P'` for post request, `'G'` for get request
        trigger (str): Activation word to trigger the command
        url (str): The URL that the command will make the request
    """

    team_id: str
    method: str
    trigger: str
    url: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        team_id = self.team_id
        method = self.method
        trigger = self.trigger
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "team_id": team_id,
                "method": method,
                "trigger": trigger,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        team_id = d.pop("team_id")

        method = d.pop("method")

        trigger = d.pop("trigger")

        url = d.pop("url")

        create_command_json_body = cls(
            team_id=team_id,
            method=method,
            trigger=trigger,
            url=url,
        )

        create_command_json_body.additional_properties = d
        return create_command_json_body

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
