# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import test.conftest as fix

import click
import pytest

import arbejdstimer.cli as cli


def test_version_ok(capsys):
    with pytest.raises(click.exceptions.Exit) as exec_info:
        assert cli.app_version() == 0
    assert exec_info.value.exit_code == 0
    out, err = capsys.readouterr()
    assert 'version' in out.lower()
    assert not err


def test_now_ok(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.now(conf=fix.CFG_FS_EMPTY, strict=False)  # type: ignore
    assert exec_info.value.code == 0
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_explain_ok(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.explain(conf=fix.CFG_FS_EMPTY, day='', verbose=False, strict=False)  # type: ignore
    assert exec_info.value.code == 0
    out, err = capsys.readouterr()
    assert 'read valid configuration from (' in out.lower()
    assert 'consider 0 holidays' in out.lower()
    assert not err


def test_explain_enforce_defaults_ok(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.explain_enforce_defaults(conf=fix.CFG_FS_EMPTY, strict=False)  # type: ignore
    assert exec_info.value.code == 0
    out, err = capsys.readouterr()
    assert 'read valid configuration from (' in out.lower()
    assert 'consider 0 holidays' in out.lower()
    assert not err


def test_template_ok(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.app_template()
    assert exec_info.value.code == 0
    out, err = capsys.readouterr()
    assert 'some holidays 2022/2023' in out.lower()
    assert not err


def test_at_main_explain_meta_only(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.explain(conf=fix.CFG_FS_META_ONLY, day='', verbose=False, strict=True)
    assert exec_info.value.code == 2
    out, err = capsys.readouterr()
    message_part = (
        'read valid configuration from (test/fixtures/basic/meta-only-config.json)\n'
        'consider 0 holidays:\n'
        'detected strict mode (queries outside of year frame from config will fail)\n'
        '- empty date range of configuration'
    )
    assert message_part in out.lower()
    assert not err


def test_at_main_explain_verbatim_meta_only(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.explain(conf=fix.CFG_FS_META_ONLY, day='', verbose=True, strict=False)
    assert exec_info.value.code == 0
    out, err = capsys.readouterr()
    message_parts = (
        'read valid configuration from (test/fixtures/basic/meta-only-config.json)',
        'configuration has 5 lines of (indented) JSON content:',
        '   1 | {',
        '   2 |   "api": 1,',
        '   3 |   "application": "arbejdstimer",',
        '   4 |   "operator": "or"',
        '   5 | }',
        'detected non-strict mode (no constraints on year frame from config)',
        'effective configuration:',
        '- no holidays defined in (test/fixtures/basic/meta-only-config.json):',
        '- working hours:',
        '  + [7, 16] (application default)',
        'evaluation:',
    )
    for message_part in message_parts:
        assert message_part in out
    assert not err


def test_at_main_explain_verbatim_triplet_holidays_default(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.explain(conf=fix.CFG_FS_TRIPLET_HOLIDAYS, day='', verbose=True, strict=False)
    assert exec_info.value.code == 0
    out, err = capsys.readouterr()
    message_parts = (
        'read valid configuration from (test/fixtures/basic/triplet-holidays-config.json)',
        'configuration has 19 lines of (indented) JSON content:',
        '    1 | {',
        '    2 |   "api": 1,',
        '    3 |   "application": "arbejdstimer",',
        '    4 |   "operator": "or",',
        '    5 |   "holidays": [',
        '    6 |     {',
        '    7 |       "label": "triplet holiday",',
        '    8 |       "at": [',
        '    9 |         "2021-12-29",',
        '   10 |         "2021-12-30",',
        '   11 |         "2021-12-31"',
        '   12 |       ]',
        '   13 |     }',
        '   14 |   ],',
        '   15 |   "working_hours": [',
        '   16 |     8,',
        '   17 |     17',
        '   18 |   ]',
        '   19 | }',
        'detected non-strict mode (no constraints on year frame from config)',
        'effective configuration:',
        '- given 3 holidays within [2021-12-29, 2021-12-31]:',
        '  + 2021-12-29',
        '  + 2021-12-30',
        '  + 2021-12-31',
        '- working hours:',
        '  + [8, 17] (from configuration)',
        'evaluation:',
    )
    for message_part in message_parts:
        assert message_part in out
    assert not err


def test_at_main_explain_verbatim_triplet_holidays_strict(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.explain(conf=fix.CFG_FS_TRIPLET_HOLIDAYS, day='', verbose=True, strict=True)
    assert exec_info.value.code == 2
    out, err = capsys.readouterr()
    message_parts = (
        'read valid configuration from (test/fixtures/basic/triplet-holidays-config.json)',
        'configuration has 19 lines of (indented) JSON content:',
        '    1 | {',
        '    2 |   "api": 1,',
        '    3 |   "application": "arbejdstimer",',
        '    4 |   "operator": "or",',
        '    5 |   "holidays": [',
        '    6 |     {',
        '    7 |       "label": "triplet holiday",',
        '    8 |       "at": [',
        '    9 |         "2021-12-29",',
        '   10 |         "2021-12-30",',
        '   11 |         "2021-12-31"',
        '   12 |       ]',
        '   13 |     }',
        '   14 |   ],',
        '   15 |   "working_hours": [',
        '   16 |     8,',
        '   17 |     17',
        '   18 |   ]',
        '   19 | }',
        'detected strict mode (queries outside of year frame from config will fail)',
        'effective configuration:',
        '- given 3 holidays within [2021-12-29, 2021-12-31]:',
        '  + 2021-12-29',
        '  + 2021-12-30',
        '  + 2021-12-31',
        '- working hours:',
        '  + [8, 17] (from configuration)',
        'evaluation:',
        '- Day is not within year range of configuration',
    )
    for message_part in message_parts:
        assert message_part in out
    assert not err


def test_non_existing_configuration_file(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.now(conf=fix.CFG_FS_NOT_THERE, strict=False)  # type: ignore
    assert exec_info.value.code == 1
    out, err = capsys.readouterr()
    assert 'config' in err.lower()
    assert 'is no file' in err.lower()
    assert not out


def test_existing_configuration_file_with_non_json_extension(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.now(conf=fix.CFG_FS_NO_JSON_EXTENSION, strict=False)  # type: ignore
    assert exec_info.value.code == 1
    out, err = capsys.readouterr()
    assert 'config' in err.lower()
    assert 'config has not .json extension' in err.lower()
    assert not out


def test_callback_with_version_false():
    assert cli.callback(False) is None
