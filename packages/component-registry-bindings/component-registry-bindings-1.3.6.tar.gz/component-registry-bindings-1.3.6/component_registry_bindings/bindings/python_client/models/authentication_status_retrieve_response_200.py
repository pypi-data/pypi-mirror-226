from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, ComponentRegistryModel, Unset

T = TypeVar("T", bound="AuthenticationStatusRetrieveResponse200")


@attr.s(auto_attribs=True)
class AuthenticationStatusRetrieveResponse200(ComponentRegistryModel):
    """ """

    oidc_enabled: Union[Unset, str] = UNSET
    user: Union[Unset, str] = UNSET
    auth: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        oidc_enabled = self.oidc_enabled
        user = self.user
        auth = self.auth

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if oidc_enabled is not UNSET:
            field_dict["oidc_enabled"] = oidc_enabled
        if user is not UNSET:
            field_dict["user"] = user
        if auth is not UNSET:
            field_dict["auth"] = auth

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy() if isinstance(src_dict, dict) else {}
        oidc_enabled = d.pop("oidc_enabled", UNSET)

        user = d.pop("user", UNSET)

        auth = d.pop("auth", UNSET)

        authentication_status_retrieve_response_200 = cls(
            oidc_enabled=oidc_enabled,
            user=user,
            auth=auth,
        )

        authentication_status_retrieve_response_200.additional_properties = d
        return authentication_status_retrieve_response_200

    @staticmethod
    def get_fields():
        return {
            "oidc_enabled": str,
            "user": str,
            "auth": str,
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
