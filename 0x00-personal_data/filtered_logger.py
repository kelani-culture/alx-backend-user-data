#!/usr/bin/env python3
"""
the filter datum function
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: List[str], separator: str) -> str:
    """ filter datum """
    pattern = "|".join(f"{field}=[^{separator}]*" for field in fields)
    return re.sub(
        pattern, lambda match: match.group(0).split("=")[0] + f"={redaction}", message,
    )
