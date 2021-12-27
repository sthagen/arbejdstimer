# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Working hours (Danish arbejdstimer) or not? API."""
import datetime as dti
import json
import os
import pathlib
import sys
from typing import List, Optional, Tuple, Union, no_type_check

from pydantic.error_wrappers import ValidationError

import arbejdstimer.api as api

DEBUG_VAR = 'ARBEJDSTIMER_DEBUG'
DEBUG = os.getenv(DEBUG_VAR)

ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'

DEFAULT_CONFIG_NAME = '.arbejdstimer.json'
CFG_TYPE = dict[str, Union[dict[str, str], list[dict[str, Union[str, list[str]]]]]]
WORKING_HOURS_TYPE = Union[tuple[int, int], tuple[None, None]]
DATE_FMT = '%Y-%m-%d'


def weekday(date: dti.date) -> int:
    """Return current weekday."""
    return date.isoweekday()


def no_weekend(day_number: int) -> bool:
    """Return if day number is weekend."""
    return day_number < 6


@no_type_check
def apply(off_days: list[dti.date], working_hours: WORKING_HOURS_TYPE, cmd: str) -> Tuple[int, str]:
    """ddd"""
    working_hours = working_hours if working_hours != (None, None) else (7, 16)
    today = dti.date.today()
    if today not in off_days:
        if cmd == 'explain':
            print(f'- Today ({today}) is not a holiday')
    else:
        return 1, '- Today is a holiday.'

    week_day = weekday(today)
    work_day = no_weekend(week_day)
    if work_day:
        if cmd == 'explain':
            print(f'- Today ({today}) is not a weekend')
    else:
        return 1, '- Today is weekend.'

    hour = dti.datetime.now().hour
    if working_hours[0] <= hour <= working_hours[1]:
        if cmd == 'explain':
            print(f'- At this hour ({hour}) is work time')
    else:
        return 1, f'- No worktime at hour({hour}).'

    return 0, ''


@no_type_check
def load(cfg: CFG_TYPE) -> Tuple[int, str, list[dti.date], WORKING_HOURS_TYPE]:
    """Load the configuration and return error, message and holidays as well as working hours list."""
    holidays = cfg.get('holidays')
    if not isinstance(holidays, list) or not holidays:
        return 0, 'configuration lacks holidays entry or list empty', [], (None, None)

    holidays_date_list = []
    for nth, entry in enumerate(holidays, start=1):
        date_range = entry['at']
        if not isinstance(date_range, list) or not date_range:
            return 1, f'no. {nth} configuration holidays entry at value is no list or empty', [], (None, None)

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

    working_hours = cfg.get('working_hours', [None, None])

    return 0, '', sorted(holidays_date_list), tuple(working_hours)


@no_type_check
def verify(cfg: CFG_TYPE) -> Tuple[int, str]:
    """Fail on invalid configuration."""
    if not cfg:
        return 0, 'empty configuration, using default'

    try:
        _ = api.Arbejdstimer(**cfg)
        return 0, ''
    except ValidationError as err:
        return 2, str(err)


def verify_request(argv: Optional[List[str]]) -> Tuple[int, str, List[str]]:
    """Fail with grace."""
    if not argv or len(argv) != 2:
        return 2, 'received wrong number of arguments', ['']

    command, config = argv

    if command not in ('explain', 'now'):
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
        if command == 'explain':
            print(message, file=sys.stderr)
        return error

    if command == 'explain':
        print(f'read valid configuration from ({config})')
    error, message, holidays, working_hours = load(configuration)
    if error:
        if command == 'explain':
            print(message, file=sys.stderr)
        return error

    if command == 'explain':
        print(f'consider {len(holidays)} holidays:')
    error, message = apply(holidays, working_hours, command)
    if error:
        if command == 'explain':
            print(message, file=sys.stdout)
        return error

    return 0
