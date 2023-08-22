from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="UploadPluginMultipartData")


@_attrs_define
class UploadPluginMultipartData:
    """
    Attributes:
        plugin (File): The plugin image to be uploaded
        force (Union[Unset, str]): Set to 'true' to overwrite a previously installed plugin with the same ID, if any
    """

    plugin: File
    force: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        plugin = self.plugin.to_tuple()

        force = self.force

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plugin": plugin,
            }
        )
        if force is not UNSET:
            field_dict["force"] = force

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        plugin = self.plugin.to_tuple()

        force = self.force if isinstance(self.force, Unset) else (None, str(self.force).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "plugin": plugin,
            }
        )
        if force is not UNSET:
            field_dict["force"] = force

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        plugin = File(payload=BytesIO(d.pop("plugin")))

        force = d.pop("force", UNSET)

        upload_plugin_multipart_data = cls(
            plugin=plugin,
            force=force,
        )

        upload_plugin_multipart_data.additional_properties = d
        return upload_plugin_multipart_data

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
