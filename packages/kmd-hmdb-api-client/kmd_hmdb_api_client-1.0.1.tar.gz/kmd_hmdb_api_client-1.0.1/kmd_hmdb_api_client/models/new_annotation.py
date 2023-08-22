from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NewAnnotation")


@_attrs_define
class NewAnnotation:
    """
    Attributes:
        name (str):
        kendricks_mass (str):
        kendricks_mass_defect (str):
        monisotopic_molecular_weight (str):
        nominal_mass (str):
        polarity (str):
    """

    name: str
    kendricks_mass: str
    kendricks_mass_defect: str
    monisotopic_molecular_weight: str
    nominal_mass: str
    polarity: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        kendricks_mass = self.kendricks_mass
        kendricks_mass_defect = self.kendricks_mass_defect
        monisotopic_molecular_weight = self.monisotopic_molecular_weight
        nominal_mass = self.nominal_mass
        polarity = self.polarity

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "kendricks_mass": kendricks_mass,
                "kendricks_mass_defect": kendricks_mass_defect,
                "monisotopic_molecular_weight": monisotopic_molecular_weight,
                "nominal_mass": nominal_mass,
                "polarity": polarity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        kendricks_mass = d.pop("kendricks_mass")

        kendricks_mass_defect = d.pop("kendricks_mass_defect")

        monisotopic_molecular_weight = d.pop("monisotopic_molecular_weight")

        nominal_mass = d.pop("nominal_mass")

        polarity = d.pop("polarity")

        new_annotation = cls(
            name=name,
            kendricks_mass=kendricks_mass,
            kendricks_mass_defect=kendricks_mass_defect,
            monisotopic_molecular_weight=monisotopic_molecular_weight,
            nominal_mass=nominal_mass,
            polarity=polarity,
        )

        new_annotation.additional_properties = d
        return new_annotation

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
