from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateUploadJsonBody")


@_attrs_define
class CreateUploadJsonBody:
    """
    Attributes:
        channel_id (str): The ID of the channel to upload to.
        filename (str): The name of the file to upload.
        file_size (int): The size of the file to upload in bytes.
    """

    channel_id: str
    filename: str
    file_size: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel_id = self.channel_id
        filename = self.filename
        file_size = self.file_size

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel_id": channel_id,
                "filename": filename,
                "file_size": file_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        channel_id = d.pop("channel_id")

        filename = d.pop("filename")

        file_size = d.pop("file_size")

        create_upload_json_body = cls(
            channel_id=channel_id,
            filename=filename,
            file_size=file_size,
        )

        create_upload_json_body.additional_properties = d
        return create_upload_json_body

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
