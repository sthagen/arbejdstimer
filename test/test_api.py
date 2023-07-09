# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import datetime as dti
import test.conftest as fix

import pytest
from pydantic import ValidationError

import arbejdstimer.api as api
import arbejdstimer.arbejdstimer as at


def _subs(count: int, what: str) -> str:
    """DRY."""
    return f'{count} validation error{"" if count == 1 else "s"} for {what}'


def test_api_hour_noon():
    twelve = api.Hour('12')  # type: ignore
    assert twelve.root == 12


def test_api_hour_42():
    with pytest.raises(ValidationError, match=_subs(1, 'Hour')) as err:
        _ = api.Hour('42')  # type: ignore
    assert '1 validation error for Hour\n  Input should be less than or equal to 23 ' in str(err.value)


def test_api_hour_negative():
    with pytest.raises(ValidationError, match=_subs(1, 'Hour')) as err:
        _ = api.Hour('-1')  # type: ignore
    assert '1 validation error for Hour\n  Input should be greater than or equal to 0 ' in str(err.value)


def test_api_hour_no_digit():
    message_part = (
        '1 validation error for Hour\n  Input should be a valid integer, unable to parse string as an integer '
    )
    with pytest.raises(ValidationError, match=_subs(1, 'Hour')) as err:
        _ = api.Hour('_')  # type: ignore
    assert message_part in str(err.value)


def test_api_date_range_wun():
    wun = api.Dates(['2021-12-31'])  # type: ignore
    assert wun.root == [dti.date(2021, 12, 31)]


def test_api_date_range_two():
    two = api.Dates(['2021-12-31', '2022-01-01'])  # type: ignore
    assert two.root == [dti.date(2021, 12, 31), dti.date(2022, 1, 1)]


def test_api_date_range_three():
    three = api.Dates(['2021-12-31', '2022-01-01', '2022-01-02'])  # type: ignore
    assert three.root == [dti.date(2021, 12, 31), dti.date(2022, 1, 1), dti.date(2022, 1, 2)]


def test_api_date_range_duplicate():
    with pytest.raises(ValidationError, match=_subs(1, 'Dates')) as err:
        _ = api.Dates(['2021-12-31', '2021-12-31'])  # type: ignore
    assert '1 validation error for Dates\n  Value error, dates must be unique ' in str(err.value)


def test_api_working_hours_nine_to_five():
    nine = api.Hour('9')  # type: ignore
    five = api.Hour('17')  # type: ignore
    assert api.WorkingHours([nine, five]).root == [nine, five]


def test_api_working_hours_empty_list():
    message_part = '1 validation error for WorkingHours\n  List should have at least 2 items after validation, not 0 '
    with pytest.raises(ValidationError, match=_subs(1, 'WorkingHours')) as err:
        _ = api.WorkingHours([])  # type: ignore
    assert message_part in str(err.value)


def test_api_working_hours_nine_single_value():
    nine = api.Hour('9')  # type: ignore
    message_part = '1 validation error for WorkingHours\n  List should have at least 2 items after validation, not 1 '
    with pytest.raises(ValidationError, match=_subs(1, 'WorkingHours')) as err:
        _ = api.WorkingHours([nine])  # type: ignore
    assert message_part in str(err.value)


def test_api_working_hours_nine_nine_five_triplet():
    nine = api.Hour('9')  # type: ignore
    five = api.Hour('17')  # type: ignore
    message_part = '1 validation error for WorkingHours\n  List should have at most 2 items after validation, not 3 '
    with pytest.raises(ValidationError, match=_subs(1, 'WorkingHours')) as err:
        _ = api.WorkingHours([nine, nine, five])  # type: ignore
    assert message_part in str(err.value)


def test_api_holiday_wun():
    wun = api.Dates(['2021-12-31'])  # type: ignore
    holiday = api.Holiday(at=wun)
    assert holiday.at.root == [dti.date(2021, 12, 31)]
    assert holiday.model_dump_json() == '{"label":"","at":["2021-12-31"]}'
    data = {'label': '', 'at': ['2021-12-31']}
    # noinspection Pydantic
    another_holiday = api.Holiday(**data)  # type: ignore
    assert holiday == another_holiday


def test_api_today():
    # noinspection Pydantic
    cfg = api.Arbejdstimer(**fix.CFG_PY_TODAY_HOLIDAY)
    today_rep = fix.TODAY.strftime(at.DATE_FMT)
    expected = (
        '{"api":1,"application":"arbejdstimer","operator":"or",'
        f'"holidays":[{{"label":"","at":["{today_rep}"]}}],"working_hours":[8,17]}}'
    )
    assert cfg.model_dump_json() == expected
