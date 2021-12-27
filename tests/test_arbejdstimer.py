# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import arbejdstimer.arbejdstimer as at
import tests.conftest as fix


def _subs(count: int, what: str) -> str:
    """DRY."""
    return f'{count} validation error{"" if count == 1 else "s"} for {what}'


def test_at_main():
    assert at.main(['now', str(fix.CFG_FS_HOLIDAYS)]) in (0, 1)


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


def test_at_verify_no_meta():
    message = '1 validation error for Arbejdstimer\noperator\n  field required (type=value_error.missing)'
    assert at.verify({'a': 'b'}) == (2, message)  # type: ignore


def test_at_verify_alien_meta():
    assert at.verify({'operator': 'or', 'application': None}) == (0, '')  # type: ignore


def test_at_verify_alien_application():
    code, message = at.verify({'operator': 'or', 'application': 'b'})  # type: ignore
    assert code == 2
    expected_part = (
        '1 validation error for Arbejdstimer\napplication\n  value is not a valid enumeration member;'
        " permitted: 'arbejdstimer'"
    )
    assert expected_part in message


def test_at_verify_alien_api_version():
    cfg = {'operator': 'or', 'application': 'b', 'api': None}
    code, message = at.verify(cfg)  # type: ignore
    assert code == 2
    expected_part = (
        '1 validation error for Arbejdstimer\napplication\n  value is not a valid enumeration member;'
        " permitted: 'arbejdstimer'"
    )
    assert expected_part in message

    cfg = {'operator': 'dirac', 'application': 'arbejdstimer', 'api': 1}
    code, message = at.verify(cfg)  # type: ignore
    assert code == 2
    expected_part = (
        '1 validation error for Arbejdstimer\noperator\n  value is not a valid enumeration member;'
        " permitted: 'and', 'or', 'xor'"
    )
    assert expected_part in message

    cfg = {'operator': 42, 'application': 'arbejdstimer', 'api': 1}
    code, message = at.verify(cfg)  # type: ignore
    expected_part = (
        '1 validation error for Arbejdstimer\noperator\n  value is not a valid enumeration member;'
        " permitted: 'and', 'or', 'xor'"
    )
    assert expected_part in message


def test_at_verify_no_holidays_alien_or_empty():
    expect = (0, '')
    cfg = {'operator': 'or', 'application': 'arbejdstimer', 'api': 1}
    assert at.verify(cfg) == expect  # type: ignore
    cfg = {**cfg, 'holidays': None}
    assert at.verify(cfg) == expect  # type: ignore
    cfg = {**cfg, 'holidays': []}
    assert at.verify(cfg) == expect  # type: ignore


def test_at_verify_holidays_alien():
    cfg = {'operator': 'or', 'application': 'arbejdstimer', 'api': 1}
    expect = (2, 'configuration holidays entry is not a list')
    cfg = {**cfg, 'holidays': {'holi': 'days'}}
    assert at.verify(cfg) == expect  # type: ignore
    cfg = {**cfg, 'holidays': 42}
    assert at.verify(cfg) == expect  # type: ignore


def test_at_verify_holidays_missing_date_range():
    cfg = {'operator': 'or', 'application': 'arbejdstimer', 'api': 1}
    cfg = {**cfg, 'holidays': [{'at': ['ignore']}, {}]}
    code, message = at.verify(cfg)  # type: ignore
    expected_parts = (
        '2 validation errors for Arbejdstimer',
        'holidays -> __root__ -> 0 -> at -> __root__ -> 0',
        'invalid date format',
        'holidays -> __root__ -> 1 -> at',
        'field required',
    )
    for part in expected_parts:
        assert part in message


def test_at_load_and_apply_today_holiday(capsys):
    error, message, holidays, _ = at.load(fix.CFG_PY_TODAY_HOLIDAY)
    assert not error
    assert not message
    assert at.apply(holidays, (None, None), 'explain') == (1, '- Today is a holiday.')
    out, err = capsys.readouterr()
    assert not out
    assert not err
