import calendar
import datetime as dti

# [[[fill git_describe()]]]
__version__ = '2022.10.13+parent.b910ed2d'
# [[[end]]] (checksum: 07a80c9698071b6c1ddafb806396926b)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__: list[str] = []


def day_count(year: int) -> int:
    """Number of days in year."""
    return 365 + calendar.isleap(year)


def day_count_from_date(date: dti.date) -> int:
    """Number of days in year of date-"""
    return day_count(date.year)


def date_from_fractional_year(date: float) -> dti.date:
    """Going back ..."""
    y_int = int(date)
    rest_y_float = date - y_int
    rest_d_float = round(rest_y_float * day_count(y_int), 1)
    if rest_d_float:
        day_counts = [c for _, c in (calendar.monthrange(y_int, m) for m in range(1, 12 + 1))]
        day_cum = [day_counts[0]] + [0] * 11
        for m, c in enumerate(day_counts[1:], start=2):
            day_cum[m - 1] = day_cum[m - 2] + c
        m_int = 1  # Well, not really, but, ... happy linter
        for m, c in enumerate(day_cum, start=1):
            if c < rest_d_float:
                continue
            m_int = m
            break

        d_int = int(rest_d_float - day_cum[m_int - 2])
    else:
        m_int, d_int = 1, 1
    return dti.date(y_int, m_int, d_int)


def fractional_year_from_date(date: dti.date) -> float:
    """... and forth."""
    return date.year + ((date - dti.date(date.year, 1, 1)).days / day_count(date.year))
