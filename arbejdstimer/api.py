# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Working hours (Danish arbejdstimer) or not? API model."""
from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional, no_type_check

from pydantic import BaseModel, Extra, Field, conint, validator


class AppName(Enum):
    arbejdstimer = 'arbejdstimer'


class ConfigurationApiVersion(Enum):
    wun = '1'


class CombinationLogicMode(Enum):
    and_logic = 'and'
    or_logic = 'or'
    xor_logic = 'xor'


class Meta(BaseModel):
    class Config:
        extra = Extra.forbid

    application: AppName = Field(
        ...,
        description='Name of the application this configuration targets.',
        title='Application Name',
    )
    configuration_api_version: ConfigurationApiVersion = Field(
        ...,
        description='API version of the application this configuration targets.',
        title='Application API Version',
    )
    combination_with_defaults: Optional[CombinationLogicMode] = Field(
        'or',
        description='Logical operation to use when combining the given specific values with the application defaults.',
        title='Logic for Combination with Default Values',
    )


class Hour(BaseModel):
    __root__: conint(ge=0, le=23)  # type: ignore


class WorkingHours(BaseModel):
    __root__: List[Hour] = Field(
        ...,
        description=(
            'The mandatory two entries are interpreted as inclusive range of 24 hour start and end integer values.'
        ),
        max_items=2,
        min_items=2,
        title='Working Hours',
    )


class DateRange(BaseModel):
    __root__: List[date] = Field(
        ...,
        description=(
            'Two dates are interpreted as inclusive range and 1, 3, or more dates are interpreted as a set of dates.'
        ),
        min_items=1,
        title='Date Ranges',
    )

    @no_type_check
    @validator('__root__')
    def is_unique(cls, v):
        if v and 1 < len(v) != len(set(v)):
            raise ValueError('dates in a date range must be unique')
        return v


class Holiday(BaseModel):
    class Config:
        extra = Extra.forbid

    label: Optional[str] = Field('', examples=['public holiday'])
    date_range: DateRange


class Holidays(BaseModel):
    __root__: List[Holiday] = Field(
        ...,
        description=(
            'The optional labels shall aid editing of the configuration but only the date_range members impact'
            ' the run time.'
        ),
        min_items=0,
        title='Holidays',
    )


class Arbejdstimer(BaseModel):
    _meta: Optional[Meta]
    holidays: Optional[Holidays]
    working_hours: Optional[WorkingHours]
