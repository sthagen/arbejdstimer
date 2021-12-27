# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import arbejdstimer.arbejdstimer as at
import tests.conftest as fix


def _subs(count: int, what: str) -> str:
    """DRY."""
    return f'{count} validation error{"" if count == 1 else "s"} for {what}'


def test_at_main_now():
    assert at.main(['now', str(fix.CFG_FS_HOLIDAYS)]) in (0, 1)


def test_at_main_now_meta_only():
    assert at.main(['now', str(fix.CFG_FS_META_ONLY)]) in (0, 1)


def test_at_main_now_load_error_processing(capsys):
    assert at.main(['now', str(fix.CFG_FS_INVALID_MINIMAL)]) == 2
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_at_main_explain():
    assert at.main(['explain', str(fix.CFG_FS_HOLIDAYS)]) in (0, 1)


def test_at_main_explain_load_error_processing(capsys):
    assert at.main(['explain', str(fix.CFG_FS_INVALID_MINIMAL)]) == 2
    out, err = capsys.readouterr()
    assert not out
    message_part = (
        '1 validation error for arbejdstimer\noperator\n  value is not a valid enumeration member;'
        " permitted: 'and', 'or', 'xor'"
    )
    assert message_part in err.lower()


def test_at_verify_request_too_few():
    assert at.verify_request([1]) == (2, 'received wrong number of arguments', [''])  # type: ignore


def test_at_verify_request_unknown_command():
    assert at.verify_request(['unknown', 'does not matter']) == (2, 'received unknown command', [''])


def test_at_verify_request_falsy_input():
    assert at.verify_request(['now', '']) == (2, 'configuration missing', [''])


def test_at_main_holidays(capsys):
    assert at.main(['explain', str(fix.CFG_FS_HOLIDAYS)]) in (0, 1)
    out, err = capsys.readouterr()
    assert 'consider 11 holidays' in out.lower()
    assert not err


def test_at_load_empty():
    assert at.load({}) == (0, 'empty configuration, using default', [], at.DEFAULT_WORK_HOURS_MARKER)


def test_at_load_falsy():
    assert at.load(None) == (0, 'empty configuration, using default', [], at.DEFAULT_WORK_HOURS_MARKER)  # type: ignore


def test_at_load_no_meta():
    message = '1 validation error for Arbejdstimer\noperator\n  field required (type=value_error.missing)'
    assert at.load({'a': 'b'}) == (2, message, [], at.DEFAULT_WORK_HOURS_MARKER)  # type: ignore


def test_at_load_alien_meta():
    code, message, holidays, hours = at.load({'operator': 'or', 'application': None})  # type: ignore
    assert code == 0
    assert message == ''
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER


def test_at_load_alien_application():
    code, message, holidays, hours = at.load({'operator': 'or', 'application': 'b'})  # type: ignore
    assert code == 2
    expected_part = (
        '1 validation error for Arbejdstimer\napplication\n  value is not a valid enumeration member;'
        " permitted: 'arbejdstimer'"
    )
    assert expected_part in message
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER


def test_at_load_alien_api_version():
    cfg = {'operator': 'or', 'application': 'b', 'api': None}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 2
    expected_part = (
        '1 validation error for Arbejdstimer\napplication\n  value is not a valid enumeration member;'
        " permitted: 'arbejdstimer'"
    )
    assert expected_part in message
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER

    cfg = {'operator': 'dirac', 'application': 'arbejdstimer', 'api': 1}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 2
    expected_part = (
        '1 validation error for Arbejdstimer\noperator\n  value is not a valid enumeration member;'
        " permitted: 'and', 'or', 'xor'"
    )
    assert expected_part in message
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER

    cfg = {'operator': 42, 'application': 'arbejdstimer', 'api': 1}
    code, message, holidays, hours = at.load(cfg)  # type: ignore
    assert code == 2
    expected_part = (
        '1 validation error for Arbejdstimer\noperator\n  value is not a valid enumeration member;'
        " permitted: 'and', 'or', 'xor'"
    )
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
    expected_part = '1 validation error for Arbejdstimer\nholidays -> __root__\n  value is not a valid list'
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
        '2 validation errors for Arbejdstimer',
        'holidays -> __root__ -> 0 -> at -> __root__ -> 0',
        'invalid date format',
        'holidays -> __root__ -> 1 -> at',
        'field required',
    )
    for part in expected_parts:
        assert part in message
    assert holidays == []
    assert hours == at.DEFAULT_WORK_HOURS_MARKER


def test_at_load_and_apply_today_holiday(capsys):
    error, message, holidays, _ = at.load(fix.CFG_PY_TODAY_HOLIDAY)
    assert not error
    assert not message
    assert at.apply(holidays, (None, None), 'explain') == (1, '- Today is a holiday.')
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
    assert at.apply([], at.DEFAULT_WORK_HOURS_MARKER, 'now') == (0, '')


def test_at_apply_now_sunday_noon():
    at.weekday = fix.always_sunday
    at.the_hour = fix.the_noon_hour
    error, message = at.apply([], at.DEFAULT_WORK_HOURS_MARKER, 'now')
    assert error == 1
    assert message == '- Today is weekend.'


def test_at_apply_now_monday_midnight():
    at.weekday = fix.always_monday
    at.the_hour = fix.the_zero_hour
    assert at.apply([], at.DEFAULT_WORK_HOURS_MARKER, 'now') == (1, f'- No worktime at hour({at.the_hour()}).')


def test_at_apply_now_sunday_midnight():
    at.weekday = fix.always_sunday
    at.the_hour = fix.the_zero_hour
    error, message = at.apply([], at.DEFAULT_WORK_HOURS_MARKER, 'now')
    assert error == 1
    assert message == '- Today is weekend.'


def test_at_apply_explain_monday_noon(capsys):
    at.weekday = fix.always_monday
    at.the_hour = fix.the_noon_hour
    assert at.apply([], at.DEFAULT_WORK_HOURS_MARKER, 'explain') == (0, '')
    out, err = capsys.readouterr()
    assert f'- Today ({fix.TODAY}) is not a holiday' in out
    assert f'- At this hour ({at.the_hour()}) is work time' in out
    assert not err
