from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Informations")


@_attrs_define
class Informations:
    """
    Attributes:
        api_version (Union[Unset, str]): this API's version Example: 1.2.3.
        database_version (Union[Unset, str]): the database version Example: 1.2.3.
        long_hash (Union[Unset, str]): Git commit ID during this project build Example:
            894d7e3829781b2cbdea49eae6bd8cab943b850b.
        short_hash (Union[Unset, str]): short Git commit ID during this project build Example: 894d7e3.
        deploy_date (Union[Unset, str]): build project date Example: 2021-01-29 15:46:03.
    """

    api_version: Union[Unset, str] = UNSET
    database_version: Union[Unset, str] = UNSET
    long_hash: Union[Unset, str] = UNSET
    short_hash: Union[Unset, str] = UNSET
    deploy_date: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        api_version = self.api_version
        database_version = self.database_version
        long_hash = self.long_hash
        short_hash = self.short_hash
        deploy_date = self.deploy_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if api_version is not UNSET:
            field_dict["api_version"] = api_version
        if database_version is not UNSET:
            field_dict["database_version"] = database_version
        if long_hash is not UNSET:
            field_dict["long_hash"] = long_hash
        if short_hash is not UNSET:
            field_dict["short_hash"] = short_hash
        if deploy_date is not UNSET:
            field_dict["deploy_date"] = deploy_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        api_version = d.pop("api_version", UNSET)

        database_version = d.pop("database_version", UNSET)

        long_hash = d.pop("long_hash", UNSET)

        short_hash = d.pop("short_hash", UNSET)

        deploy_date = d.pop("deploy_date", UNSET)

        informations = cls(
            api_version=api_version,
            database_version=database_version,
            long_hash=long_hash,
            short_hash=short_hash,
            deploy_date=deploy_date,
        )

        informations.additional_properties = d
        return informations

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
