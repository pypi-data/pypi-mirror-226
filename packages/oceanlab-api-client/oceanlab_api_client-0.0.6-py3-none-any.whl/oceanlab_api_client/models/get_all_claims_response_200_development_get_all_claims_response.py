from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAllClaimsResponse200DevelopmentGetAllClaimsResponse")


@define
class GetAllClaimsResponse200DevelopmentGetAllClaimsResponse:
    """
    Attributes:
        development_varchar (Union[Unset, str]):
    """

    development_varchar: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        development_varchar = self.development_varchar

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if development_varchar is not UNSET:
            field_dict["Development.VARCHAR"] = development_varchar

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        development_varchar = d.pop("Development.VARCHAR", UNSET)

        get_all_claims_response_200_development_get_all_claims_response = cls(
            development_varchar=development_varchar,
        )

        get_all_claims_response_200_development_get_all_claims_response.additional_properties = d
        return get_all_claims_response_200_development_get_all_claims_response

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
