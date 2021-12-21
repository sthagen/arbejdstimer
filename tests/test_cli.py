# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import click
import pytest

import arbejdstimer.cli as cli
import tests.conftest as fix


def test_main_legacy_ok(capsys):
    assert cli.main(['now', str(fix.CFG_FS_HOLIDAYS)]) == 0
    out, err = capsys.readouterr()
    assert 'read valid configuration from (' in out.lower()
    assert not err


def test_version_ok(capsys):
    with pytest.raises(click.exceptions.Exit) as exec_info:
        assert cli.app_version() == 0
    assert exec_info.value.exit_code == 0
    out, err = capsys.readouterr()
    assert 'version' in out.lower()
    assert not err


def test_now_ok(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.now(conf=fix.CFG_FS_EMPTY)  # type: ignore
    assert exec_info.value.code == 2
    out, err = capsys.readouterr()
    assert 'read valid configuration from (' in out.lower()
    assert 'configuration lacks holidays entry or list empty' in err.lower()


def test_non_existing_configuration_file(capsys):
    with pytest.raises(SystemExit) as exec_info:
        cli.now(conf=fix.CFG_FS_NOT_THERE)  # type: ignore
    assert exec_info.value.code == 1
    out, err = capsys.readouterr()
    assert 'config' in err.lower()
    assert 'is no file' in err.lower()
    assert not out


def test_callback_with_version_false():
    assert cli.callback(False) is None
