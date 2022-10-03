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
DEFAULT_WORK_HOURS_CLOSED_INTERVAL = (7, 16)


@no_type_check
def load_config(path_or_str):
    """DRY."""
    with open(path_or_str, 'rt', encoding=ENCODING) as handle:
        return json.load(handle)


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
def days_of_year(day=None) -> list[dti.date]:
    """Return all days of the year that contains the day."""
    year = dti.date.today().year if day is None else day.year
    d_start = dti.date(year, 1, 1)
    d_end = dti.date(year, 12, 31)
    return [d_start + dti.timedelta(days=x) for x in range((d_end - d_start).days + 1)]


@no_type_check
def workdays(off_days: list[dti.date], days=days_of_year(None)) -> list[dti.date]:
    """Return all workdays of the year that contains the day."""
    return [cand for cand in days if cand not in off_days and no_weekend(weekday(cand))]


@no_type_check
def workday(off_days: list[dti.date], cmd: str, day=None) -> Tuple[int, str]:
    """Apply the effective rules to the given date (default today)."""
    if day is None:
        day = dti.date.today()
    if day not in off_days:
        if cmd.startswith('explain'):
            print(f'- Day ({day}) is not a holiday')
    else:
        return 1, '- Day is a holiday.'

    work_day = no_weekend(weekday(day))
    if work_day:
        if cmd.startswith('explain'):
            print(f'- Day ({day}) is not a weekend')
    else:
        return 1, '- Day is weekend.'

    return 0, ''


@no_type_check
def apply(off_days: list[dti.date], working_hours: WORKING_HOURS_TYPE, cmd: str) -> Tuple[int, str]:
    """Apply the effective rules to the current date and time."""
    working_hours = working_hours if working_hours != (None, None) else DEFAULT_WORK_HOURS_CLOSED_INTERVAL
    code, message = workday(off_days, cmd, day=None)
    if code:
        return code, message
    hour = the_hour()
    if working_hours[0] <= hour <= working_hours[1]:  # type: ignore
        if cmd.startswith('explain'):
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
        model = api.Arbejdstimer(**cfg)  # type: ignore
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
        working_hours = tuple(sorted(model.working_hours.dict().get('__root__', [None, None])))  # type: ignore
    return 0, '', sorted(holidays_date_list), working_hours


@no_type_check
def workdays_from_config(cfg: CFG_TYPE, day=None) -> list[dti.date]:
    """Ja, ja, ja."""
    error, _, holidays, _ = load(cfg)
    return [] if error else workdays(holidays, days=days_of_year(day))


def verify_request(argv: Optional[List[str]]) -> Tuple[int, str, List[str]]:
    """Fail with grace."""
    if not argv or len(argv) != 2:
        return 2, 'received wrong number of arguments', ['']

    command, config = argv

    if command not in ('explain', 'explain_verbatim', 'now'):
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

    configuration = load_config(config)
    error, message, holidays, working_hours = load(configuration)
    if error:
        if command.startswith('explain'):
            print('Configuration file failed to parse (INVALID)')
            print(message, file=sys.stderr)
        return error

    if command.startswith('explain'):
        print(f'read valid configuration from ({config})')
        if command == 'explain_verbatim':
            lines = json.dumps(configuration, indent=2).split('\n')
            line_count = len(lines)
            counter_width = len(str(line_count))
            print(f'configuration has {line_count} line{"" if line_count == 1 else "s"} of (indented) JSON content:')
            for line, content in enumerate(lines, start=1):
                print(f'  {line:>{counter_width + 1}} | {content}')

    if command == 'explain':
        print(f'consider {len(holidays)} holidays:')
    elif command == 'explain_verbatim':
        print('effective configuration:')
        if holidays:
            print(f'- given {len(holidays)} holidays within [{holidays[0]}, {holidays[-1]}]:')
            for holiday in holidays:
                print(f'  + {holiday}')
        else:
            print(f'- no holidays defined in ({config}):')
        print('- working hours:')
        if working_hours != DEFAULT_WORK_HOURS_MARKER:
            print(f'  + [{working_hours[0]}, {working_hours[1]}] (from configuration)')
        else:
            effective_range = DEFAULT_WORK_HOURS_CLOSED_INTERVAL
            print(f'  + [{effective_range[0]}, {effective_range[1]}] (application default)')
        print('evaluation:')

    error, message = apply(holidays, working_hours, command)
    if error:
        if command.startswith('explain'):
            print(message, file=sys.stdout)
        return error

    return 0
