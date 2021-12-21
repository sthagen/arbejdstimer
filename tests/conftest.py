# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import json
import pathlib

CFG_FS_EMPTY = pathlib.Path('tests', 'fixtures', 'basic', 'minimal-config.json')
CFG_FS_HOLIDAYS = pathlib.Path('tests', 'fixtures', 'basic', 'holidays-config.json')
CFG_FS_NOT_THERE = pathlib.Path('does', 'not', 'exist', 'hypothetical.json')
CFG_PY_EMPTY = {}

ENCODING = 'utf-8'
with open(CFG_FS_HOLIDAYS, 'rt', encoding=ENCODING) as handle:
    CFG_PY_HOLIDAYS = json.load(handle)
