#!/usr/bin/env python3
"""filter logger"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    this method filters the personal data
    """
    regex = fr'({"|".join(re.escape(field) for field in fields)})=[^{separator}]+'
    return re.sub(regex, fr'\1={redaction}', message)
