from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.statistics_taxonomies import StatisticsTaxonomies


T = TypeVar("T", bound="Statistics")


@_attrs_define
class Statistics:
    """
    Attributes:
        taxonomies (Union[Unset, StatisticsTaxonomies]):
    """

    taxonomies: Union[Unset, "StatisticsTaxonomies"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        taxonomies: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.taxonomies, Unset):
            taxonomies = self.taxonomies.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if taxonomies is not UNSET:
            field_dict["taxonomies"] = taxonomies

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.statistics_taxonomies import StatisticsTaxonomies

        d = src_dict.copy()
        _taxonomies = d.pop("taxonomies", UNSET)
        taxonomies: Union[Unset, StatisticsTaxonomies]
        if isinstance(_taxonomies, Unset):
            taxonomies = UNSET
        else:
            taxonomies = StatisticsTaxonomies.from_dict(_taxonomies)

        statistics = cls(
            taxonomies=taxonomies,
        )

        statistics.additional_properties = d
        return statistics

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
