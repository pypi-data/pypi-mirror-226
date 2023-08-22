from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchChannelsForRetentionPolicyJsonBody")


@_attrs_define
class SearchChannelsForRetentionPolicyJsonBody:
    """
    Attributes:
        term (Union[Unset, str]): The string to search in the channel name, display name, and purpose.
        team_ids (Union[Unset, List[str]]): Filters results to channels belonging to the given team ids
        public (Union[Unset, bool]): Filters results to only return Public / Open channels, can be used in conjunction
            with `private` to return both `public` and `private` channels
        private (Union[Unset, bool]): Filters results to only return Private channels, can be used in conjunction with
            `public` to return both `private` and `public` channels
        deleted (Union[Unset, bool]): Filters results to only return deleted / archived channels
    """

    term: Union[Unset, str] = UNSET
    team_ids: Union[Unset, List[str]] = UNSET
    public: Union[Unset, bool] = UNSET
    private: Union[Unset, bool] = UNSET
    deleted: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        term = self.term
        team_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.team_ids, Unset):
            team_ids = self.team_ids

        public = self.public
        private = self.private
        deleted = self.deleted

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if term is not UNSET:
            field_dict["term"] = term
        if team_ids is not UNSET:
            field_dict["team_ids"] = team_ids
        if public is not UNSET:
            field_dict["public"] = public
        if private is not UNSET:
            field_dict["private"] = private
        if deleted is not UNSET:
            field_dict["deleted"] = deleted

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        term = d.pop("term", UNSET)

        team_ids = cast(List[str], d.pop("team_ids", UNSET))

        public = d.pop("public", UNSET)

        private = d.pop("private", UNSET)

        deleted = d.pop("deleted", UNSET)

        search_channels_for_retention_policy_json_body = cls(
            term=term,
            team_ids=team_ids,
            public=public,
            private=private,
            deleted=deleted,
        )

        search_channels_for_retention_policy_json_body.additional_properties = d
        return search_channels_for_retention_policy_json_body

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
