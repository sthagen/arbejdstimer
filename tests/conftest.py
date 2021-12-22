# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import datetime as dti
import json
import pathlib

import arbejdstimer.arbejdstimer as at

CFG_FS_EMPTY = pathlib.Path('tests', 'fixtures', 'basic', 'minimal-config.json')
CFG_FS_HOLIDAYS = pathlib.Path('tests', 'fixtures', 'basic', 'holidays-config.json')
CFG_FS_NOT_THERE = pathlib.Path('does', 'not', 'exist', 'hypothetical.json')
CFG_PY_EMPTY = {}

TODAY = dti.date.today()
CFG_PY_TODAY_HOLIDAY = {
    '_meta': {
        'combination_with_defaults': 'or',
        'application': 'arbejdstimer',
        'configuration_api_version': '1',
    },
    'holidays': [{'date_range': [TODAY.strftime(at.DATE_FMT)]}],
    'working_hours': [8, 17],
}

ENCODING = 'utf-8'
with open(CFG_FS_HOLIDAYS, 'rt', encoding=ENCODING) as handle:
    CFG_PY_HOLIDAYS = json.load(handle)
