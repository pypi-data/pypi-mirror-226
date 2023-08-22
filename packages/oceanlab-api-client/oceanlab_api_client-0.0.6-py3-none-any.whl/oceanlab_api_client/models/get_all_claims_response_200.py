from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_all_claims_response_200_development_get_all_claims_response import (
        GetAllClaimsResponse200DevelopmentGetAllClaimsResponse,
    )


T = TypeVar("T", bound="GetAllClaimsResponse200")


@define
class GetAllClaimsResponse200:
    """
    Attributes:
        development_get_all_claims_response (Union[Unset, GetAllClaimsResponse200DevelopmentGetAllClaimsResponse]):
    """

    development_get_all_claims_response: Union[Unset, "GetAllClaimsResponse200DevelopmentGetAllClaimsResponse"] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        development_get_all_claims_response: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.development_get_all_claims_response, Unset):
            development_get_all_claims_response = self.development_get_all_claims_response.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if development_get_all_claims_response is not UNSET:
            field_dict["Development.GetAllClaimsResponse"] = development_get_all_claims_response

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_all_claims_response_200_development_get_all_claims_response import (
            GetAllClaimsResponse200DevelopmentGetAllClaimsResponse,
        )

        d = src_dict.copy()
        _development_get_all_claims_response = d.pop("Development.GetAllClaimsResponse", UNSET)
        development_get_all_claims_response: Union[Unset, GetAllClaimsResponse200DevelopmentGetAllClaimsResponse]
        if isinstance(_development_get_all_claims_response, Unset):
            development_get_all_claims_response = UNSET
        else:
            development_get_all_claims_response = GetAllClaimsResponse200DevelopmentGetAllClaimsResponse.from_dict(
                _development_get_all_claims_response
            )

        get_all_claims_response_200 = cls(
            development_get_all_claims_response=development_get_all_claims_response,
        )

        get_all_claims_response_200.additional_properties = d
        return get_all_claims_response_200

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
