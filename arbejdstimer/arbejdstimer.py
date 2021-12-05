# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Working hours (Danish arbejdstimer) or not? API."""
import json
import os
import pathlib
import sys
from typing import List, Optional, Tuple, Union

DEBUG_VAR = 'ARBEJDSTIMER_DEBUG'
DEBUG = os.getenv(DEBUG_VAR)

ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'


DEFAULT_CONFIG_NAME = '.arbejdstimer.json'


def verify_request(argv: Optional[List[str]]) -> Tuple[int, str, List[str]]:
    """Fail with grace."""
    if not argv or len(argv) != 2:
        return 2, 'received wrong number of arguments', ['']

    command, config = argv

    if command not in ('now'):
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

    print(f'configuration is ({configuration})')

    return 0
