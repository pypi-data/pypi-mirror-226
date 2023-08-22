from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_info import FileInfo


T = TypeVar("T", bound="UploadFileResponse201")


@_attrs_define
class UploadFileResponse201:
    """
    Attributes:
        file_infos (Union[Unset, List['FileInfo']]): A list of file metadata that has been stored in the database
        client_ids (Union[Unset, List[str]]): A list of the client_ids that were provided in the request
    """

    file_infos: Union[Unset, List["FileInfo"]] = UNSET
    client_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_infos: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.file_infos, Unset):
            file_infos = []
            for file_infos_item_data in self.file_infos:
                file_infos_item = file_infos_item_data.to_dict()

                file_infos.append(file_infos_item)

        client_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.client_ids, Unset):
            client_ids = self.client_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if file_infos is not UNSET:
            field_dict["file_infos"] = file_infos
        if client_ids is not UNSET:
            field_dict["client_ids"] = client_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_info import FileInfo

        d = src_dict.copy()
        file_infos = []
        _file_infos = d.pop("file_infos", UNSET)
        for file_infos_item_data in _file_infos or []:
            file_infos_item = FileInfo.from_dict(file_infos_item_data)

            file_infos.append(file_infos_item)

        client_ids = cast(List[str], d.pop("client_ids", UNSET))

        upload_file_response_201 = cls(
            file_infos=file_infos,
            client_ids=client_ids,
        )

        upload_file_response_201.additional_properties = d
        return upload_file_response_201

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
