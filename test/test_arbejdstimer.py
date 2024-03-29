import datetime as dti
import test.conftest as fix

import pytest

import arbejdstimer.arbejdstimer as at
from arbejdstimer import date_from_fractional_year, day_count, day_count_from_date, fractional_year_from_date

TODAY = dti.date.today().strftime('%Y-%m-%d')
ERR_CMD_TUPLE = ('', '', '', False)


def _subs(count: int, what: str) -> str:
    """DRY."""
    return f'{count} validation error{"" if count == 1 else "s"} for {what}'


def test_at_main_now():
    assert at.main(('now', '', str(fix.CFG_FS_HOLIDAYS), False)) in (0, 1)


def test_at_main_now_meta_only():
    assert at.main(('now', '', str(fix.CFG_FS_META_ONLY), True)) == 2


def test_at_main_now_load_error_processing(capsys):
    assert at.main(('now', '', str(fix.CFG_FS_INVALID_MINIMAL), True)) == 2
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_at_main_explain():
    assert at.main(('explain', '', str(fix.CFG_FS_HOLIDAYS), True)) in (0, 1)


def test_at_main_explain_load_error_processing(capsys):
    assert at.main(('explain', '', str(fix.CFG_FS_INVALID_MINIMAL), True)) == 2
    out, err = capsys.readouterr()
    assert 'Configuration file failed to parse (INVALID)' in out
    message_part = "input should be 'and', 'or' or 'xor'"
    assert message_part in err.lower()


def test_at_verify_request_too_few():
    assert at.verify_request([1]) == (2, 'received wrong number of arguments', ERR_CMD_TUPLE)  # type: ignore


def test_at_verify_request_unknown_command():
    assert at.verify_request(('unknown', '', 'does not matter', True)) == (2, 'received unknown command', ERR_CMD_TUPLE)


def test_at_verify_request_falsy_input():
    assert at.verify_request(('now', '', '', True)) == (2, 'configuration missing', ERR_CMD_TUPLE)


def test_at_main_holidays(capsys):
    assert at.main(('explain', '2022-10-22', str(fix.CFG_FS_HOLIDAYS), True)) in (0, 1)
    out, err = capsys.readouterr()
    assert 'consider 32 holidays' in out.lower()
    assert 'is within date range of configuration' in out.lower()
    assert 'is not a holiday' in out.lower()
    assert 'is weekend.' in out.lower()
    assert not err


def test_at_load_empty():
    assert at.load({}) == (0, 'empty configuration, using default', [], at.DEFAULT_WORK_HOURS_MARKER)


def test_at_load_falsy():
    assert at.load(None) == (0, 'empty configuration, using default', [], at.DEFAULT_WORK_HOURS_MARKER)  # type: ignore


def test_at_load_no_meta():
    message_start = '1 validation error for Arbejdstimer\noperator\n  Field required '
    code, message, data, marker = at.load({'a': 'b'})
    assert code == 2
    assert message.startswith(message_start)
    assert data == []
    assert marker == at.DEFAULT_WORK_HOURS_MARKER


def test_at_load_alien_meta():
    code, message, holidays, hours = at.load({'operator': 'or', 'application': None})  # type: ignore
    assert code == 0
    assert message == ''
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER


def test_at_load_alien_application():
    code, message, holidays, hours = at.load({'operator': 'or', 'application': 'b'})  # type: ignore
    assert code == 2
    expected_part = "1 validation error for Arbejdstimer\napplication\n  Input should be 'arbejdstimer'"
    assert expected_part in message
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER


def test_at_load_alien_api_version():
    cfg = {'operator': 'or', 'application': 'b', 'api': None}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 2
    expected_part = "Input should be 'arbejdstimer'"
    assert expected_part in message
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER

    cfg = {'operator': 'dirac', 'application': 'arbejdstimer', 'api': 1}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 2
    expected_part = "1 validation error for Arbejdstimer\noperator\n  Input should be 'and', 'or' or 'xor'"
    assert expected_part in message
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER

    cfg = {'operator': 42, 'application': 'arbejdstimer', 'api': 1}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 2
    expected_part = "1 validation error for Arbejdstimer\noperator\n  Input should be 'and', 'or' or 'xor'"
    assert expected_part in message
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER


def test_at_load_no_holidays_alien_or_empty():
    cfg = {'operator': 'or', 'application': 'arbejdstimer', 'api': 1}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 0
    assert message == ''
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER

    cfg = {**cfg, 'holidays': None}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 0
    assert message == ''
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER

    cfg = {**cfg, 'holidays': []}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 0
    assert message == ''
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER


def test_at_load_holidays_alien():
    cfg = {'operator': 'or', 'application': 'arbejdstimer', 'api': 1}
    cfg = {**cfg, 'holidays': {'holi': 'days'}}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 2
    expected_part = '1 validation error for Arbejdstimer\nholidays\n  Input should be a valid list'
    assert expected_part in message
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER

    cfg = {**cfg, 'holidays': 42}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 2
    assert expected_part in message
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER


def test_at_load_holidays_missing_date_range():
    cfg = {'operator': 'or', 'application': 'arbejdstimer', 'api': 1}
    cfg = {**cfg, 'holidays': [{'at': ['ignore']}, {}]}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 2
    expected_parts = (
        '2 validation errors for Arbejdstimer\nholidays.0.at.0\n'
        '  Input should be a valid date or datetime, input is too short',
    )
    for part in expected_parts:
        assert part in message
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER


def test_at_load_and_apply_today_holiday(capsys):
    error, message, holidays, _ = at.load(fix.CFG_PY_TODAY_HOLIDAY)
    assert not error
    assert not message
    expected = (2, '- Day is not within year range of configuration')
    assert at.apply(holidays, (None, None), 'explain', TODAY, True) == expected
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_at_load_triplet_holidays():
    error, message, holidays, hours = at.load(fix.CFG_PY_TRIPLET_HOLIDAYS)
    assert not error
    assert not message
    assert len(holidays) == 3
    assert hours == tuple(fix.CFG_PY_TRIPLET_HOLIDAYS['working_hours'])


def test_at_apply_now_monday_noon():
    at.weekday = fix.always_monday
    at.the_hour = fix.the_noon_hour
    expected = (2, '- empty date range of configuration')
    assert at.apply([], at.DEFAULT_WORK_HOURS_MARKER, 'now', TODAY, True) == expected


def test_at_apply_now_sunday_noon():
    at.weekday = fix.always_sunday
    at.the_hour = fix.the_noon_hour
    error, message = at.apply([dti.date.today()], at.DEFAULT_WORK_HOURS_MARKER, 'now', TODAY, True)
    assert error == 2
    assert message == '- Day is not within year range of configuration'


def test_at_apply_now_monday_midnight():
    at.weekday = fix.always_monday
    at.the_hour = fix.the_zero_hour
    expected = (2, '- empty date range of configuration')
    assert at.apply([], at.DEFAULT_WORK_HOURS_MARKER, 'now', TODAY, True) == expected


def test_at_apply_now_sunday_midnight():
    at.weekday = fix.always_sunday
    at.the_hour = fix.the_zero_hour
    error, message = at.apply([dti.date.today()], at.DEFAULT_WORK_HOURS_MARKER, 'now', TODAY, True)
    assert error == 2
    assert message == '- Day is not within year range of configuration'


def test_at_apply_explain_monday_noon(capsys):
    at.weekday = fix.always_monday
    at.the_hour = fix.the_noon_hour
    expected = (2, '- Day is not within year range of configuration')
    assert at.apply([dti.date.today()], at.DEFAULT_WORK_HOURS_MARKER, 'explain', TODAY, True) == expected
    out, err = capsys.readouterr()
    assert not err


def test_workdays_count_per_month():
    wds = [dti.date(2022, 1, 3), dti.date(2022, 12, 1), dti.date(2022, 12, 2)]
    assert at.workdays_count_per_month(wds) == {'2022-01': 1, '2022-12': 2}


def test_day_count_2020():
    assert day_count(2020) == 366


def test_day_count_2022():
    assert day_count(2022) == 365


def test_day_count_from_date():
    assert day_count_from_date(dti.date(2022, 1, 1)) == 365


def test_fractional_year_from_date():
    assert fractional_year_from_date(dti.date(2022, 1, 1)) == 2022.0


def test_fractional_year_from_date_half_in_year():
    assert fractional_year_from_date(dti.date(2022, 7, 1)) == pytest.approx(2022.5, abs=0.01)


def test_date_from_fractional_year():
    assert date_from_fractional_year(2022.0) == dti.date(2022, 1, 1)


def test_date_from_fractional_year_halfway():
    assert date_from_fractional_year(2022.5) == dti.date(2022, 7, 1)


def test_workdays_of_month():
    work_days = [dti.date(2022, 1, 3), dti.date(2022, 7, 1), dti.date(2022, 8, 1), dti.date(2022, 12, 30)]
    count = at.workdays_of_month
    assert count(work_days, '2022-01') == [dti.date(2022, 1, 3)]
    assert count(work_days, '2022-03') == []
    assert count(work_days, '2022-08') == [dti.date(2022, 8, 1)]
    assert count(work_days, '2022-12') == [dti.date(2022, 12, 30)]


def test_cumulative_workdays_count_per_month():
    work_days = [dti.date(2022, 1, 3), dti.date(2022, 7, 1), dti.date(2022, 8, 1), dti.date(2022, 12, 30)]
    cum = at.cumulative_workdays_count_per_month
    assert cum(work_days) == {
        '2022-01': 1,
        '2022-07': 2,
        '2022-08': 3,
        '2022-12': 4,
    }


def test_workdays_count_of_month_in_between():
    work_days = [dti.date(2022, 1, 3), dti.date(2022, 7, 1), dti.date(2022, 8, 1), dti.date(2022, 12, 30)]
    done = at.workdays_count_of_month_in_between
    assert done(work_days, '2022-01', 4, '2022-01', '2022-01') == 1
    assert done(work_days, '2022-01', 2, '2022-01', '2022-01') == 0
    assert done(work_days, '2022-01', 4, '2022-07', '2022-08') == 0
    assert done(work_days, '2022-07', 2, '2022-01', '2022-08') == 1
    assert done(work_days, '2022-07', 2, '2022-07', '2022-08') == 1


def test_workdays_count_of_year_in_between():
    work_days = [dti.date(2022, 1, 3), dti.date(2022, 7, 1), dti.date(2022, 8, 1), dti.date(2022, 12, 30)]
    done = at.workdays_count_of_year_in_between
    assert done(work_days, '2022-01', 2) == 0
    assert done(work_days, '2022-03', 31) == 0
    assert done(work_days, '2022-01', 4, '2022-01', '2022-01') == 1
    assert done(work_days, '2022-01', 2, '2022-01', '2022-01') == 0
    assert done(work_days, '2022-01', 4, '2022-07', '2022-08') == 0
    assert done(work_days, '2022-07', 2, '2022-01', '2022-08') == 2
    assert done(work_days, '2022-07', 2, '2022-07', '2022-08') == 1


def test_remaining_workdays_count_of_year_in_between():
    work_days = [dti.date(2022, 1, 3), dti.date(2022, 7, 1), dti.date(2022, 8, 1), dti.date(2022, 12, 30)]
    remaining = at.remaining_workdays_count_of_year_in_between
    assert remaining(work_days, '2022-01', 2) == 4
    assert remaining(work_days, '2022-03', 31) == 0
    assert remaining(work_days, '2022-01', 4, '2022-01', '2022-01') == 0
    assert remaining(work_days, '2022-01', 2, '2022-01', '2022-01') == 1
    assert remaining(work_days, '2022-01', 4, '2022-07', '2022-08') == 2
