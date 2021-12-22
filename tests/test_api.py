# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import pytest
from pydantic.error_wrappers import ValidationError

import arbejdstimer.api as api


def _subs(count: int, what: str) -> str:
    """DRY."""
    return f'{count} validation error{"" if count == 1 else "s"} for {what}'


def test_api_hour_noon():
    twelve = api.Hour(__root__='12')  # type: ignore
    assert twelve.__root__ == 12


def test_api_hour_42():
    with pytest.raises(ValidationError, match=_subs(1, 'Hour')) as err:
        _ = api.Hour(__root__='42')  # type: ignore
    assert '\n__root__\n  ensure this value is less than or equal to 23' in str(err.value)
