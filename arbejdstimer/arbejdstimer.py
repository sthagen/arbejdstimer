# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Working hours (Danish arbejdstimer) or not? API."""
import datetime as dti
import json
import os
import pathlib
import sys
from typing import List, Optional, Tuple, Union, no_type_check

DEBUG_VAR = 'ARBEJDSTIMER_DEBUG'
DEBUG = os.getenv(DEBUG_VAR)

ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'


DEFAULT_CONFIG_NAME = '.arbejdstimer.json'
CFG_TYPE = dict[str, Union[dict[str, str], list[dict[str, Union[str, list[str]]]]]]
DATE_FMT = '%Y-%m-%d'


def weekday(date: dti.date) -> int:
    """Return current weekday."""
    return date.isoweekday()


def no_weekend(day_number: int) -> bool:
    """Return if day number is weekend."""
    return day_number < 6


@no_type_check
def load(cfg: CFG_TYPE) -> Tuple[int, str, list[dti.date]]:
    """Load the configuration and return error, message and holidays list."""
    holidays = cfg.get('holidays')
    if not isinstance(holidays, list) or not holidays:
        return 2, 'configuration lacks holidays entry or list empty', []

    holidays_date_list = []
    for nth, entry in enumerate(holidays, start=1):
        date_range = entry['date_range']
        if not isinstance(date_range, list) or not date_range:
            return 1, f'no. {nth} configuration holidays entry date_range value is no list or empty', []

        if len(date_range) == 1:
            holidays_date_list.append(dti.datetime.strptime(date_range[0], DATE_FMT).date())
        elif len(date_range) == 2:
            data = sorted(date_range)
            start, end = [dti.datetime.strptime(data[n], DATE_FMT).date() for n in (0, 1)]
            current = start
            holidays_date_list.append(current)
            while current < end:
                current += dti.timedelta(days=1)
                holidays_date_list.append(current)
        else:
            for text in date_range:
                holidays_date_list.append(dti.datetime.strptime(text, DATE_FMT).date())

    return 0, '', sorted(holidays_date_list)


@no_type_check
def verify(cfg: CFG_TYPE) -> Tuple[int, str]:
    """Fail on invalid configuration."""
    if not cfg:
        return 0, 'empty configuration, using default'

    if not cfg.get('_meta') or not isinstance(cfg['_meta'], dict):
        return 2, 'configuration lacks required _meta (object) section'

    meta = cfg['_meta']
    if not meta.get('combination_with_defaults'):
        return 2, 'configuration lacks required rule for combination with defaults (expected value "or")'

    if meta.get('application', 'NOT_PRESENT') != 'arbejdstimer':
        return 2, 'configuration offers wrong application (name) value (expected arbejdstimer)'

    api_version = meta.get('configuration_api_version', '0')
    try:
        api_version = int(api_version)
        if api_version != 1:
            return 2, 'configuration offers wrong or no api version (expected value "1")'
    except ValueError:
        return 1, 'configuration offers wrong api version value (expected value "1")'

    if not cfg.get('holidays'):
        return 2, 'configuration lacks holidays entry or list empty'

    holidays = cfg['holidays']
    if not isinstance(holidays, list):
        return 2, 'configuration holidays entry is not a list'

    for nth, entry in enumerate(holidays, start=1):
        if not entry.get('date_range'):
            return 2, f'no. {nth} configuration holidays entry has no date_range value (not present or list empty)'

    return 0, ''


def verify_request(argv: Optional[List[str]]) -> Tuple[int, str, List[str]]:
    """Fail with grace."""
    if not argv or len(argv) != 2:
        return 2, 'received wrong number of arguments', ['']

    command, config = argv

    if command not in ('now',):
        return 2, 'received unknown command', ['']

    if not config:
        return 2, 'configuration missing', ['']

    config_path = pathlib.Path(str(config))
    if not config_path.is_file():
        return 1, f'config ({config_path}) is no file', ['']
    if not ''.join(config_path.suffixes).lower().endswith('.json'):
        return 1, 'config has not .json extension', ['']

    return 0, '', argv


def main(argv: Union[List[str], None] = None) -> int:
    """Drive the lookup."""
    error, message, strings = verify_request(argv)
    if error:
        print(message, file=sys.stderr)
        return error

    command, config = strings

    with open(config, 'rt', encoding=ENCODING) as handle:
        configuration = json.load(handle)

    error, message = verify(configuration)
    if error:
        print(message, file=sys.stderr)
        return error

    print(f'read valid configuration from ({config})')
    error, message, holidays = load(configuration)
    if error:
        print(message, file=sys.stderr)
        return error

    print(f'consider {len(holidays)} holidays:')
    today = dti.date.today()
    week_day = weekday(today)
    work_day = no_weekend(week_day)
    if work_day:
        print(f'- Today ({today}) is not a weekend')
    else:
        print('- Today is weekend.')
        return 1

    if today not in holidays:
        print(f'- Today ({today}) is not a holiday')
    else:
        print('- Today is a holiday.')
        return 1

    hour = dti.datetime.now().hour
    if 6 < hour < 17:
        print(f'- At this hour ({hour}) is work time')
    else:
        print(f'- No worktime at hour({hour}).')
        return 1

    return 0
