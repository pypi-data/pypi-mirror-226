from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.annotation import Annotation
    from ..models.taxonomy import Taxonomy


T = TypeVar("T", bound="NewCompound")


@_attrs_define
class NewCompound:
    """
    Attributes:
        taxonomy (Taxonomy):
        annotations (List['Annotation']):
        database (str):
        metabolite_name (str):
        chemical_formula (str):
        hmdb_id (str):
        inchikey (str):
    """

    taxonomy: "Taxonomy"
    annotations: List["Annotation"]
    database: str
    metabolite_name: str
    chemical_formula: str
    hmdb_id: str
    inchikey: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        taxonomy = self.taxonomy.to_dict()

        annotations = []
        for annotations_item_data in self.annotations:
            annotations_item = annotations_item_data.to_dict()

            annotations.append(annotations_item)

        database = self.database
        metabolite_name = self.metabolite_name
        chemical_formula = self.chemical_formula
        hmdb_id = self.hmdb_id
        inchikey = self.inchikey

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "taxonomy": taxonomy,
                "annotations": annotations,
                "database": database,
                "metabolite_name": metabolite_name,
                "chemical_formula": chemical_formula,
                "hmdb_id": hmdb_id,
                "inchikey": inchikey,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.annotation import Annotation
        from ..models.taxonomy import Taxonomy

        d = src_dict.copy()
        taxonomy = Taxonomy.from_dict(d.pop("taxonomy"))

        annotations = []
        _annotations = d.pop("annotations")
        for annotations_item_data in _annotations:
            annotations_item = Annotation.from_dict(annotations_item_data)

            annotations.append(annotations_item)

        database = d.pop("database")

        metabolite_name = d.pop("metabolite_name")

        chemical_formula = d.pop("chemical_formula")

        hmdb_id = d.pop("hmdb_id")

        inchikey = d.pop("inchikey")

        new_compound = cls(
            taxonomy=taxonomy,
            annotations=annotations,
            database=database,
            metabolite_name=metabolite_name,
            chemical_formula=chemical_formula,
            hmdb_id=hmdb_id,
            inchikey=inchikey,
        )

        new_compound.additional_properties = d
        return new_compound

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
