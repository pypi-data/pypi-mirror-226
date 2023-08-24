from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.cdr_patch_dto_approval_status import CdrPatchDtoApprovalStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CdrPatchDto")


@attr.s(auto_attribs=True)
class CdrPatchDto:
    """
    Attributes:
        approval_status (Union[Unset, CdrPatchDtoApprovalStatus]):  Default: CdrPatchDtoApprovalStatus.VALUE_0.
    """

    approval_status: Union[Unset, CdrPatchDtoApprovalStatus] = CdrPatchDtoApprovalStatus.VALUE_0
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        approval_status: Union[Unset, int] = UNSET
        if not isinstance(self.approval_status, Unset):
            approval_status = self.approval_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if approval_status is not UNSET:
            field_dict["approvalStatus"] = approval_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _approval_status = d.pop("approvalStatus", UNSET)
        approval_status: Union[Unset, CdrPatchDtoApprovalStatus]
        if isinstance(_approval_status, Unset):
            approval_status = UNSET
        else:
            approval_status = CdrPatchDtoApprovalStatus(_approval_status)

        cdr_patch_dto = cls(
            approval_status=approval_status,
        )

        cdr_patch_dto.additional_properties = d
        return cdr_patch_dto

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
