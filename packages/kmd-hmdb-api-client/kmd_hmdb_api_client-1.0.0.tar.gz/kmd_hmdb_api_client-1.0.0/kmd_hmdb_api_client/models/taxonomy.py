from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Taxonomy")


@_attrs_define
class Taxonomy:
    """
    Attributes:
        class_ (str):
        kingdom (str):
        molecular_framework (str):
        sub_class (str):
        super_class (str):
        id (int):
    """

    class_: str
    kingdom: str
    molecular_framework: str
    sub_class: str
    super_class: str
    id: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        class_ = self.class_
        kingdom = self.kingdom
        molecular_framework = self.molecular_framework
        sub_class = self.sub_class
        super_class = self.super_class
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "class": class_,
                "kingdom": kingdom,
                "molecular_framework": molecular_framework,
                "sub_class": sub_class,
                "super_class": super_class,
                "ID": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        if src_dict is None:
            return cls(
                class_=None,
                kingdom=None,
                molecular_framework=None,
                sub_class=None,
                super_class=None,
                id=None,
            )

        d = src_dict.copy()
        class_ = d.pop("class")

        kingdom = d.pop("kingdom")

        molecular_framework = d.pop("molecular_framework")

        sub_class = d.pop("sub_class")

        super_class = d.pop("super_class")

        id = d.pop("ID")

        taxonomy = cls(
            class_=class_,
            kingdom=kingdom,
            molecular_framework=molecular_framework,
            sub_class=sub_class,
            super_class=super_class,
            id=id,
        )

        taxonomy.additional_properties = d
        return taxonomy

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
