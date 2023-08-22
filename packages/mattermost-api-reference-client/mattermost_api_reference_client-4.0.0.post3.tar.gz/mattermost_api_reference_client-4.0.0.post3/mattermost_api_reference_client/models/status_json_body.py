from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StatusJsonBody")


@_attrs_define
class StatusJsonBody:
    """
    Attributes:
        message (str): The status update message. Example: Starting to investigate..
        reminder (Union[Unset, float]): The number of seconds until the system will send a reminder to the owner to
            update the status. No reminder will be scheduled if reminder is 0 or omitted. Example: 600.
    """

    message: str
    reminder: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        reminder = self.reminder

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
            }
        )
        if reminder is not UNSET:
            field_dict["reminder"] = reminder

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message")

        reminder = d.pop("reminder", UNSET)

        status_json_body = cls(
            message=message,
            reminder=reminder,
        )

        status_json_body.additional_properties = d
        return status_json_body

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
