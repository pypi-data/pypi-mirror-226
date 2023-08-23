from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.raw_data_node_3_response_200_response_result_item import RawDataNode3Response200ResponseResultItem


T = TypeVar("T", bound="RawDataNode3Response200Response")


@define
class RawDataNode3Response200Response:
    """
    Attributes:
        varchar (Union[Unset, str]):
        result (Union[Unset, List['RawDataNode3Response200ResponseResultItem']]):
    """

    varchar: Union[Unset, str] = UNSET
    result: Union[Unset, List["RawDataNode3Response200ResponseResultItem"]] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        varchar = self.varchar
        result: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.result, Unset):
            result = []
            for result_item_data in self.result:
                result_item = result_item_data.to_dict()

                result.append(result_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if varchar is not UNSET:
            field_dict[".VARCHAR"] = varchar
        if result is not UNSET:
            field_dict[".result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.raw_data_node_3_response_200_response_result_item import RawDataNode3Response200ResponseResultItem

        d = src_dict.copy()
        varchar = d.pop(".VARCHAR", UNSET)

        result = []
        _result = d.pop(".result", UNSET)
        for result_item_data in _result or []:
            result_item = RawDataNode3Response200ResponseResultItem.from_dict(result_item_data)

            result.append(result_item)

        raw_data_node_3_response_200_response = cls(
            varchar=varchar,
            result=result,
        )

        raw_data_node_3_response_200_response.additional_properties = d
        return raw_data_node_3_response_200_response

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
