# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import datetime as dti
import json
import pathlib

import arbejdstimer.arbejdstimer as at

CFG_FS_EMPTY = pathlib.Path('tests', 'fixtures', 'basic', 'minimal-config.json')
CFG_FS_META_ONLY = pathlib.Path('tests', 'fixtures', 'basic', 'meta-only-config.json')
CFG_FS_HOLIDAYS = pathlib.Path('tests', 'fixtures', 'basic', 'holidays-config.json')
CFG_FS_TRIPLET_HOLIDAYS = pathlib.Path('tests', 'fixtures', 'basic', 'triplet-holidays-config.json')
CFG_FS_NOT_THERE = pathlib.Path('does', 'not', 'exist', 'hypothetical.json')
CFG_FS_NO_JSON_EXTENSION = pathlib.Path('tests', 'fixtures', 'basic', 'this-has-no-json-extens.ion')
CFG_FS_INVALID_MINIMAL = pathlib.Path('tests', 'fixtures', 'basic', 'invalid-minimal-config.json')
CFG_PY_EMPTY = {
    'operator': 'or',
}

TODAY = dti.date.today()
CFG_PY_TODAY_HOLIDAY = {
    'api': 1,
    'application': 'arbejdstimer',
    'operator': 'or',
    'holidays': [{'at': [TODAY.strftime(at.DATE_FMT)]}],
    'working_hours': [8, 17],
}

ENCODING = 'utf-8'
with open(CFG_FS_HOLIDAYS, 'rt', encoding=ENCODING) as handle:
    CFG_PY_HOLIDAYS = json.load(handle)

with open(CFG_FS_TRIPLET_HOLIDAYS, 'rt', encoding=ENCODING) as handle:
    CFG_PY_TRIPLET_HOLIDAYS = json.load(handle)
