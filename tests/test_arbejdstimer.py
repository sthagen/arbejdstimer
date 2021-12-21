# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import arbejdstimer.arbejdstimer as at
import tests.conftest as fix


def test_at_main():
    assert at.main(['now', str(fix.CFG_FS_HOLIDAYS)]) == 0


def test_at_verify_request_too_few():
    assert at.verify_request([1]) == (2, 'received wrong number of arguments', [''])  # type: ignore


def test_at_verify_request_unknown_command():
    assert at.verify_request(['unknown', 'does not matter']) == (2, 'received unknown command', [''])


def test_at_verify_request_falsy_input():
    assert at.verify_request(['now', '']) == (2, 'configuration missing', [''])


def test_at_main_holidays(capsys):
    assert at.main(['now', str(fix.CFG_FS_HOLIDAYS)]) == 0
    out, err = capsys.readouterr()
    assert 'consider 11 holidays' in out.lower()
    assert not err


def test_at_verify_no_meta():
    assert at.verify({'a': 'b'}) == (2, 'configuration lacks required _meta (object) section')  # type: ignore


def test_at_verify_alien_meta():
    assert at.verify({'_meta': 'b'}) == (2, 'configuration lacks required _meta (object) section')  # type: ignore
    expect = (2, 'configuration lacks required rule for combination with defaults (expected value "or")')
    assert at.verify({'_meta': {'a': 'b'}}) == expect  # type: ignore


def test_at_verify_alien_application():
    expect = (2, 'configuration offers wrong application (name) value (expected arbejdstimer)')
    cfg = {'_meta': {'combination_with_defaults': 'or'}}
    assert at.verify(cfg) == expect  # type: ignore
    cfg = {'_meta': {'combination_with_defaults': 'or', 'application': 'alien'}}
    assert at.verify(cfg) == expect  # type: ignore


def test_at_verify_alien_api_version():
    expect = (2, 'configuration offers wrong or no api version (expected value "1")')
    cfg = {'_meta': {'combination_with_defaults': 'or', 'application': 'arbejdstimer'}}
    assert at.verify(cfg) == expect  # type: ignore
    cfg = {'_meta': {'combination_with_defaults': 'x', 'application': 'arbejdstimer', 'configuration_api_version': '2'}}
    assert at.verify(cfg) == expect  # type: ignore
    expect = (1, 'configuration offers wrong api version value (expected value "1")')
    cfg = {'_meta': {'combination_with_defaults': 'y', 'application': 'arbejdstimer', 'configuration_api_version': '_'}}
    assert at.verify(cfg) == expect  # type: ignore


def test_at_verify_no_holidays_alien_or_empty():
    cfg = {'_meta': {'combination_with_defaults': 'y', 'application': 'arbejdstimer', 'configuration_api_version': '1'}}
    expect = (2, 'configuration lacks holidays entry or list empty')
    assert at.verify(cfg) == expect  # type: ignore
    cfg = {**cfg, 'holidays': None}
    assert at.verify(cfg) == expect  # type: ignore
    cfg = {**cfg, 'holidays': []}
    assert at.verify(cfg) == expect  # type: ignore


def test_at_verify_holidays_alien():
    cfg = {'_meta': {'combination_with_defaults': 'y', 'application': 'arbejdstimer', 'configuration_api_version': '1'}}
    expect = (2, 'configuration holidays entry is not a list')
    cfg = {**cfg, 'holidays': {'holi': 'days'}}
    assert at.verify(cfg) == expect  # type: ignore
    cfg = {**cfg, 'holidays': 42}
    assert at.verify(cfg) == expect  # type: ignore


def test_at_verify_holidays_missing_date_range():
    cfg = {'_meta': {'combination_with_defaults': 'y', 'application': 'arbejdstimer', 'configuration_api_version': '1'}}
    expect = (2, 'no. 2 configuration holidays entry has no date_range value (not present or list empty)')
    cfg = {**cfg, 'holidays': [{'date_range': ['ignore']}, {}]}
    assert at.verify(cfg) == expect  # type: ignore
