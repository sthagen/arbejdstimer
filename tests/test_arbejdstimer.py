# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import pathlib

import arbejdstimer.arbejdstimer as at


def test_ko_main():
    inp = str(pathlib.Path('tests', 'fixtures', 'basic', 'minimal-config.json'))
    assert at.main(['now', inp]) == 0


def test_ko_verify_request_too_few():
    assert at.verify_request([1]) == (2, 'received wrong number of arguments', [''])


def test_ko_verify_request_unknown_command():
    assert at.verify_request(['unknown', 'does not matter']) == (2, 'received unknown command', [''])


def test_ko_verify_request_falsy_input():
    argv = ['now', '']
    assert at.verify_request(argv) == (2, 'configuration missing', [''])
