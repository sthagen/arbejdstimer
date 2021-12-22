# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import datetime as dti

import pytest
from pydantic.error_wrappers import ValidationError

import arbejdstimer.api as api


def _subs(count: int, what: str) -> str:
    """DRY."""
    return f'{count} validation error{"" if count == 1 else "s"} for {what}'


def test_api_hour_noon():
    twelve = api.Hour(__root__='12')  # type: ignore
    assert twelve.__root__ == 12


def test_api_hour_42():
    with pytest.raises(ValidationError, match=_subs(1, 'Hour')) as err:
        _ = api.Hour(__root__='42')  # type: ignore
    assert '\n__root__\n  ensure this value is less than or equal to 23' in str(err.value)


def test_api_hour_negative():
    with pytest.raises(ValidationError, match=_subs(1, 'Hour')) as err:
        _ = api.Hour(__root__='-1')  # type: ignore
    assert '\n__root__\n  ensure this value is greater than or equal to 0' in str(err.value)


def test_api_hour_no_digit():
    with pytest.raises(ValidationError, match=_subs(1, 'Hour')) as err:
        _ = api.Hour(__root__='_')  # type: ignore
    assert '\n__root__\n  value is not a valid integer' in str(err.value)


def test_api_date_range_wun():
    wun = api.DateRange(__root__=['2021-12-31'])  # type: ignore
    assert wun.__root__ == [dti.date(2021, 12, 31)]


def test_api_date_range_two():
    two = api.DateRange(__root__=['2021-12-31', '2022-01-01'])  # type: ignore
    assert two.__root__ == [dti.date(2021, 12, 31), dti.date(2022, 1, 1)]


def test_api_date_range_three():
    three = api.DateRange(__root__=['2021-12-31', '2022-01-01', '2022-01-02'])  # type: ignore
    assert three.__root__ == [dti.date(2021, 12, 31), dti.date(2022, 1, 1), dti.date(2022, 1, 2)]


def test_api_date_range_duplicate():
    with pytest.raises(ValidationError, match=_subs(1, 'DateRange')) as err:
        _ = api.DateRange(__root__=['2021-12-31', '2021-12-31'])  # type: ignore
    assert '\n__root__\n  dates in a date range must be unique' in str(err.value)


def test_api_working_hours_nine_to_five():
    nine = api.Hour(__root__='9')  # type: ignore
    five = api.Hour(__root__='17')  # type: ignore
    assert api.WorkingHours(__root__=[nine, five]).__root__ == [nine, five]


def test_api_working_hours_empty_list():
    with pytest.raises(ValidationError, match=_subs(1, 'WorkingHours')) as err:
        _ = api.WorkingHours(__root__=[])  # type: ignore
    assert '\n__root__\n  ensure this value has at least 2 items' in str(err.value)


def test_api_working_hours_nine_single_value():
    nine = api.Hour(__root__='9')  # type: ignore
    with pytest.raises(ValidationError, match=_subs(1, 'WorkingHours')) as err:
        _ = api.WorkingHours(__root__=[nine])  # type: ignore
    assert '\n__root__\n  ensure this value has at least 2 items' in str(err.value)


def test_api_working_hours_nine_nine_five_triplet():
    nine = api.Hour(__root__='9')  # type: ignore
    five = api.Hour(__root__='17')  # type: ignore
    with pytest.raises(ValidationError, match=_subs(1, 'WorkingHours')) as err:
        _ = api.WorkingHours(__root__=[nine, nine, five])  # type: ignore
    assert '\n__root__\n  ensure this value has at most 2 items' in str(err.value)
