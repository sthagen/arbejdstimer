# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import arbejdstimer.api as api


def test_api_hour_noon():
    twelve = api.Hour(__root__='12')  # type: ignore
    assert twelve.__root__ == 12
