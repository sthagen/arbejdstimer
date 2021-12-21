# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import arbejdstimer.arbejdstimer as at
import tests.conftest as fix


def test_at_main():
    assert at.main(['now', str(fix.CFG_FS_EMPTY)]) == 0


def test_at_verify_request_too_few():
    assert at.verify_request([1]) == (2, 'received wrong number of arguments', [''])  # type: ignore


def test_at_verify_request_unknown_command():
    assert at.verify_request(['unknown', 'does not matter']) == (2, 'received unknown command', [''])


def test_at_verify_request_falsy_input():
    assert at.verify_request(['now', '']) == (2, 'configuration missing', [''])


def test_at_main_holidays(capsys):
    assert at.main(['now', str(fix.CFG_FS_HOLIDAYS)]) == 0
    out, err = capsys.readouterr()
    assert "'label': 'company holidays 2021/2022'" in out.lower()
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
