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
DEFAULT_WORK_HOURS_MARKER = (None, None)


def weekday(date: dti.date) -> int:
    """Return current weekday."""
    return date.isoweekday()


def no_weekend(day_number: int) -> bool:
    """Return if day number is weekend."""
    return day_number < 6


def the_hour() -> int:
    """Return the hour of day as integer within [0, 23]."""
    return dti.datetime.now().hour


@no_type_check
def apply(off_days: list[dti.date], working_hours: WORKING_HOURS_TYPE, cmd: str) -> Tuple[int, str]:
    """Apply the effective rules to the current date and time."""
    working_hours = working_hours if working_hours != (None, None) else (7, 16)
    today = dti.date.today()
    if today not in off_days:
        if cmd == 'explain':
            print(f'- Today ({today}) is not a holiday')
    else:
        return 1, '- Today is a holiday.'

    work_day = no_weekend(weekday(today))
    if work_day:
        if cmd == 'explain':
            print(f'- Today ({today}) is not a weekend')
    else:
        return 1, '- Today is weekend.'

    hour = the_hour()
    if working_hours[0] <= hour <= working_hours[1]:
        if cmd == 'explain':
            print(f'- At this hour ({hour}) is work time')
    else:
        return 1, f'- No worktime at hour({hour}).'

    return 0, ''


@no_type_check
def load(cfg: CFG_TYPE) -> Tuple[int, str, list[dti.date], WORKING_HOURS_TYPE]:
    """Load the configuration and return error, message and holidays as well as working hours list.

    The holidays as well as non-default working hours will be ordered.
    """
    if not cfg:
        return 0, 'empty configuration, using default', [], DEFAULT_WORK_HOURS_MARKER

    try:
        model = api.Arbejdstimer(**cfg)
    except ValidationError as err:
        return 2, str(err), [], (None, None)

    holidays_date_list = []
    if model.holidays:
        holidays = model.dict()['holidays']
        for nth, holiday in enumerate(holidays, start=1):
            dates = holiday['at']
            if len(dates) == 1:
                holidays_date_list.append(dates[0])
            elif len(dates) == 2:
                data = sorted(dates)
                start, end = [data[n] for n in (0, 1)]
                current = start
                holidays_date_list.append(current)
                while current < end:
                    current += dti.timedelta(days=1)
                    holidays_date_list.append(current)
            else:
                for a_date in dates:
                    holidays_date_list.append(a_date)

    working_hours = DEFAULT_WORK_HOURS_MARKER
    if model.working_hours:
        working_hours = tuple(sorted(model.working_hours.dict().get('__root__', [None, None])))
    return 0, '', sorted(holidays_date_list), working_hours


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

    error, message, holidays, working_hours = load(configuration)
    if error:
        if command == 'explain':
            print(message, file=sys.stderr)
        return error
    if command == 'explain':
        print(f'read valid configuration from ({config})')

    if command == 'explain':
        print(f'consider {len(holidays)} holidays:')
    error, message = apply(holidays, working_hours, command)
    if error:
        if command == 'explain':
            print(message, file=sys.stdout)
        return error

    return 0
