from datetime import datetime
from enum import Enum

import holidays


class Cost(Enum):
    G11 = 1
    G12 = 2
    G12W = 3

    def price(self, date: datetime, price_day: float, price_night: float) -> float:
        match self.value:
            case 2:
                if (6 < date.hour < 15) or (17 < date.hour < 22):
                    return price_day
                else:
                    return price_night
            case 3:
                if is_holiday(date) or date.weekday() in (5, 6):
                    return price_night
                elif (6 < date.hour < 15) or (17 < date.hour < 22):
                    return price_day
                else:
                    return price_night
            case _:
                return price_day

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)


def get_cost_by_value(value: int) -> Cost:
    for cost in Cost:
        if cost.value == value:
            return cost
    return Cost.G11


def is_holiday(date: datetime) -> bool:
    return date in holidays.country_holidays('PL')
