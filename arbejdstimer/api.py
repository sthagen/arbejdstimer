# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Working hours (Danish arbejdstimer) or not? API model."""
from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Annotated, List, Optional, no_type_check

from pydantic import BaseModel, Field, validator


class Application(Enum):
    arbejdstimer = 'arbejdstimer'


class Operator(Enum):
    and_ = 'and'
    or_ = 'or'
    xor = 'xor'


class Hour(BaseModel):
    __root__: Annotated[int, Field(ge=0.0, le=23.0)]


class WorkingHours(BaseModel):
    __root__: Annotated[
        List[Hour],
        Field(
            description='Inclusive range of 24 hour start and end integer values.',
            max_items=2,
            min_items=2,
            title='Working Hours',
        ),
    ]


class Dates(BaseModel):
    __root__: Annotated[
        List[date],
        Field(
            description='Two dates are an inclusive range and 1, 3, or more dates represent a set of dates.',
            min_items=1,
            title='Dates - Range or Set',
        ),
    ]

    @no_type_check
    @validator('__root__')
    @classmethod
    def is_unique(cls, v):
        if v and 1 < len(v) != len(set(v)):
            raise ValueError('dates must be unique')
        return v


class Holiday(BaseModel):
    label: Annotated[Optional[str], Field(examples=['public holiday'])] = ''
    at: Dates


class Holidays(BaseModel):
    __root__: Annotated[
        List[Holiday],
        Field(
            description='Optionally labeled dates of non-working days.',
            min_items=0,
            title='Holidays',
        ),
    ]


class Arbejdstimer(BaseModel):
    api: Annotated[
        Optional[int],
        Field(
            description='API version of the application this configuration targets.',
            title='API Version',
        ),
    ] = 1
    application: Annotated[
        Optional[Application],
        Field(
            description='Name of the application this configuration targets.',
            title='Application Name',
        ),
    ] = Application.arbejdstimer
    operator: Annotated[
        Operator,
        Field(
            description='Logic combining the given specific values with the application defaults.',
            title='Logic for Combination with Default Values',
        ),
    ]
    holidays: Optional[Holidays] = None
    working_hours: Optional[WorkingHours] = None
