# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Working hours (Danish arbejdstimer) or not? API."""
import copy
import datetime as dti
import json
import os
import pathlib
import sys
from typing import Tuple, Union, no_type_check

from pydantic.error_wrappers import ValidationError

import arbejdstimer.api as api

DEBUG_VAR = 'ARBEJDSTIMER_DEBUG'
DEBUG = os.getenv(DEBUG_VAR)

ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'

DEFAULT_CONFIG_NAME = '.arbejdstimer.json'
CfgType = dict[str, Union[dict[str, str], list[dict[str, Union[str, list[str]]]]]]
WorkingHoursType = Union[tuple[int, int], tuple[None, None]]
CmdType = Tuple[str, str, str, bool]
DATE_FMT = '%Y-%m-%d'
YEAR_MONTH_FORMAT = '%Y-%m'
DEFAULT_WORK_HOURS_MARKER = (None, None)
DEFAULT_WORK_HOURS_CLOSED_INTERVAL = (7, 16)


@no_type_check
def year_month_me(date) -> str:
    """DRY."""
    return date.strftime(YEAR_MONTH_FORMAT)


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
def workdays(off_days: list[dti.date], days=None) -> list[dti.date]:
    """Return all workdays of the year that contains the day."""
    if days is None:
        days = days_of_year(None)
    return [cand for cand in days if cand not in off_days and no_weekend(weekday(cand))]


@no_type_check
def workdays_of_month(work_days, month) -> list[dti.date]:
    """Return all workdays of the month."""
    return [work_day for work_day in work_days if year_month_me(work_day) == month]


@no_type_check
def workdays_count_per_month(work_days) -> dict[str, int]:
    """Return the workday count per month of the year that contains the day."""
    per = {}
    for work_day in work_days:
        month = year_month_me(work_day)
        if month not in per:
            per[month] = 0
        per[month] += 1
    return per


@no_type_check
def cumulative_workdays_count_per_month(work_days) -> dict[str, int]:
    """Return the cumulative workday count per month of the year that contains the day."""
    per = workdays_count_per_month(work_days)
    months = list(per)
    cum = copy.deepcopy(per)
    for slot, month in enumerate(months, start=1):
        cum[month] = sum(per[m] for m in months[:slot])
    return cum


@no_type_check
def workdays_count_of_month_in_between(work_days, month, day, first_month, last_month) -> int:
    """Return the workday count of month to date for day (incl.) given first and last month."""
    per = workdays_count_per_month(work_days)
    if month not in per or month < first_month or month > last_month:
        return 0

    wds = workdays_of_month(work_days, month)
    return sum(1 for d in wds if d.day <= day)


@no_type_check
def closed_interval_months(work_days) -> tuple[str, str]:
    """DRY."""
    return year_month_me(work_days[0]), year_month_me(work_days[-1])


@no_type_check
def workdays_count_of_year_in_between(work_days, month, day, first_month=None, last_month=None) -> int:
    """Return the workday count of year to date for day (incl.) given first and last month."""
    per = workdays_count_per_month(work_days)
    if any(
        (
            month not in per,
            first_month and first_month not in per,
            last_month and last_month not in per,
        )
    ):
        return 0

    initial, final = closed_interval_months(work_days)
    if first_month is None:
        first_month = initial
    if last_month is None:
        last_month = final

    count = 0
    for d in work_days:
        ds = year_month_me(d)
        if first_month <= ds <= last_month:
            if ds < month or ds == month and d.day <= day:
                count += 1

    return count


@no_type_check
def remaining_workdays_count_of_year_in_between(work_days, month, day, first_month=None, last_month=None) -> int:
    """Return the workday count of year from date for day (incl.) given first and last month."""
    per = workdays_count_per_month(work_days)
    if any(
        (
            month not in per,
            first_month and first_month not in per,
            last_month and last_month not in per,
        )
    ):
        return 0

    initial, final = closed_interval_months(work_days)
    if first_month is None:
        first_month = initial
    if last_month is None:
        last_month = final

    count = 0
    for d in work_days:
        ds = year_month_me(d)
        if first_month <= ds <= last_month:
            if ds == month and d.day > day or ds > month:
                count += 1

    return count


@no_type_check
def workday(off_days: list[dti.date], cmd: str, date: str = '', strict: bool = False) -> Tuple[int, str]:
    """Apply the effective rules to the given date (default today)."""
    day = dti.datetime.strptime(date, DATE_FMT).date() if date else dti.date.today()
    if strict:
        if not off_days:
            return 2, '- empty date range of configuration'
        if not (off_days[0].year <= day.year < off_days[-1].year):
            return 2, '- Day is not within year range of configuration'
        else:
            if cmd.startswith('explain'):
                print(f'- Day ({day}) is within date range of configuration')

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
def apply(
    off_days: list[dti.date], working_hours: WorkingHoursType, cmd: str, day: str, strict: bool
) -> Tuple[int, str]:
    """Apply the effective rules to the current date and time."""
    working_hours = working_hours if working_hours != (None, None) else DEFAULT_WORK_HOURS_CLOSED_INTERVAL
    code, message = workday(off_days, cmd, date=str(day), strict=strict)
    if code:
        return code, message
    hour = the_hour()
    if working_hours[0] <= hour <= working_hours[1]:
        if cmd.startswith('explain'):
            print(f'- At this hour ({hour}) is work time')
    else:
        return 1, f'- No worktime at hour({hour}).'

    return 0, ''


@no_type_check
def load(cfg: CfgType) -> Tuple[int, str, list[dti.date], WorkingHoursType]:
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


@no_type_check
def workdays_from_config(cfg: CfgType, day=None) -> list[dti.date]:
    """Ja, ja, ja."""
    error, _, holidays, _ = load(cfg)
    return [] if error else workdays(holidays, days=days_of_year(day))


def verify_request(argv: Union[CmdType, None]) -> Tuple[int, str, CmdType]:
    """Fail with grace."""
    err = ('', '', '', False)
    if not argv or len(argv) != 4:
        return 2, 'received wrong number of arguments', err

    command, date, config, strict = argv

    if command not in ('explain', 'explain_verbatim', 'now'):
        return 2, 'received unknown command', err

    if not config:
        return 2, 'configuration missing', err

    config_path = pathlib.Path(str(config))
    if not config_path.is_file():
        return 1, f'config ({config_path}) is no file', err
    if not ''.join(config_path.suffixes).lower().endswith('.json'):
        return 1, 'config has not .json extension', err

    return 0, '', argv


def main(argv: Union[CmdType, None] = None) -> int:
    """Drive the lookup."""
    error, message, strings = verify_request(argv)
    if error:
        print(message, file=sys.stderr)
        return error

    command, date, config, strict = strings

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
        if command == 'explain_verbatim':
            if strict:
                print('detected strict mode (queries outside of year frame from config will fail)')
            else:
                print('detected non-strict mode (no constraints on year frame from config)')

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

    if strict:
        print('detected strict mode (queries outside of year frame from config will fail)')

    error, message = apply(holidays, working_hours, command, date, strict)
    if error:
        if command.startswith('explain'):
            print(message, file=sys.stdout)
        return error

    return 0
