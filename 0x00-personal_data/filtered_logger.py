#!/usr/bin/env python3
"""This file contains the filter_datum function"""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str,
                 separator: str) -> str:
    """This function returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message
