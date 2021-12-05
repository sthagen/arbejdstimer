# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long,missing-module-docstring
import sys

from arbejdstimer.cli import app

if __name__ == '__main__':
    sys.exit(app(prog_name='arbejdstimer'))  # pragma: no cover
