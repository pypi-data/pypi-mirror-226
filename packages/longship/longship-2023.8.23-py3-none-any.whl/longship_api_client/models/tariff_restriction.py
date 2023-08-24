import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.tariff_restriction_day_of_week_item import TariffRestrictionDayOfWeekItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="TariffRestriction")


@attr.s(auto_attribs=True)
class TariffRestriction:
    """
    Attributes:
        start_time (Union[Unset, str]):
        end_time (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):
        day_of_week (Union[Unset, List[TariffRestrictionDayOfWeekItem]]):
    """

    start_time: Union[Unset, str] = UNSET
    end_time: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    day_of_week: Union[Unset, List[TariffRestrictionDayOfWeekItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_time = self.start_time
        end_time = self.end_time
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        day_of_week: Union[Unset, List[int]] = UNSET
        if not isinstance(self.day_of_week, Unset):
            day_of_week = []
            for day_of_week_item_data in self.day_of_week:
                day_of_week_item = day_of_week_item_data.value

                day_of_week.append(day_of_week_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if day_of_week is not UNSET:
            field_dict["day_of_week"] = day_of_week

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_time = d.pop("start_time", UNSET)

        end_time = d.pop("end_time", UNSET)

        _start_date = d.pop("start_date", UNSET)
        start_date: Union[Unset, datetime.datetime]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date)

        _end_date = d.pop("end_date", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        day_of_week = []
        _day_of_week = d.pop("day_of_week", UNSET)
        for day_of_week_item_data in _day_of_week or []:
            day_of_week_item = TariffRestrictionDayOfWeekItem(day_of_week_item_data)

            day_of_week.append(day_of_week_item)

        tariff_restriction = cls(
            start_time=start_time,
            end_time=end_time,
            start_date=start_date,
            end_date=end_date,
            day_of_week=day_of_week,
        )

        tariff_restriction.additional_properties = d
        return tariff_restriction

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
