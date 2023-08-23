from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, ComponentRegistryModel, Unset

T = TypeVar("T", bound="TokenAuthTestRetrieveResponse200")


@attr.s(auto_attribs=True)
class TokenAuthTestRetrieveResponse200(ComponentRegistryModel):
    """ """

    user: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user = self.user

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy() if isinstance(src_dict, dict) else {}
        user = d.pop("user", UNSET)

        token_auth_test_retrieve_response_200 = cls(
            user=user,
        )

        token_auth_test_retrieve_response_200.additional_properties = d
        return token_auth_test_retrieve_response_200

    @staticmethod
    def get_fields():
        return {
            "user": str,
        }

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
