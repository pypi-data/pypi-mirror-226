from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_job_json_body_data import CreateJobJsonBodyData


T = TypeVar("T", bound="CreateJobJsonBody")


@_attrs_define
class CreateJobJsonBody:
    """
    Attributes:
        type (str): The type of job to create
        data (Union[Unset, CreateJobJsonBodyData]): An object containing any additional data required for this job type
    """

    type: str
    data: Union[Unset, "CreateJobJsonBodyData"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_job_json_body_data import CreateJobJsonBodyData

        d = src_dict.copy()
        type = d.pop("type")

        _data = d.pop("data", UNSET)
        data: Union[Unset, CreateJobJsonBodyData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = CreateJobJsonBodyData.from_dict(_data)

        create_job_json_body = cls(
            type=type,
            data=data,
        )

        create_job_json_body.additional_properties = d
        return create_job_json_body

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
