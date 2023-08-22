from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="UploadFileMultipartData")


@_attrs_define
class UploadFileMultipartData:
    """
    Attributes:
        files (Union[Unset, File]): A file to be uploaded
        channel_id (Union[Unset, str]): The ID of the channel that this file will be uploaded to
        client_ids (Union[Unset, str]): A unique identifier for the file that will be returned in the response
    """

    files: Union[Unset, File] = UNSET
    channel_id: Union[Unset, str] = UNSET
    client_ids: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        files: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.files, Unset):
            files = self.files.to_tuple()

        channel_id = self.channel_id
        client_ids = self.client_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if files is not UNSET:
            field_dict["files"] = files
        if channel_id is not UNSET:
            field_dict["channel_id"] = channel_id
        if client_ids is not UNSET:
            field_dict["client_ids"] = client_ids

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        files: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.files, Unset):
            files = self.files.to_tuple()

        channel_id = (
            self.channel_id
            if isinstance(self.channel_id, Unset)
            else (None, str(self.channel_id).encode(), "text/plain")
        )
        client_ids = (
            self.client_ids
            if isinstance(self.client_ids, Unset)
            else (None, str(self.client_ids).encode(), "text/plain")
        )

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update({})
        if files is not UNSET:
            field_dict["files"] = files
        if channel_id is not UNSET:
            field_dict["channel_id"] = channel_id
        if client_ids is not UNSET:
            field_dict["client_ids"] = client_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _files = d.pop("files", UNSET)
        files: Union[Unset, File]
        if isinstance(_files, Unset):
            files = UNSET
        else:
            files = File(payload=BytesIO(_files))

        channel_id = d.pop("channel_id", UNSET)

        client_ids = d.pop("client_ids", UNSET)

        upload_file_multipart_data = cls(
            files=files,
            channel_id=channel_id,
            client_ids=client_ids,
        )

        upload_file_multipart_data.additional_properties = d
        return upload_file_multipart_data

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
