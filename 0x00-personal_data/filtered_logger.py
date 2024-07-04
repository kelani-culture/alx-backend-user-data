#!/usr/bin/env python3
""" Using regex to replace occurrences of field values in ; separated fields"""
import re
from typing import List
import logging
import mysql.connector
import os


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """obfuscates log messages with regex"""
    for field in fields:
        message = re.sub(
            f"{field}=(.*?){separator}",
            f"{field}={redaction}{separator}",
            message,
        )
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Returns filtered values from log records"""
        return filter_datum(
            self.fields, self.REDACTION, super().format(record), self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object using a formatter created from
    the fields provided by the PII_FIELDS global constant"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    dest_handler = logging.StreamHandler()
    dest_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    dest_handler.setFormatter(formatter)

    logger.addHandler(dest_handler)
    return logger


def get_db() -> mysql.connector.connection.MYSQLConnection:
    """creates a mysql connection using provided credentials in the env"""
    db_connect = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
    )
    return db_connect


def main():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    row_headers = [field[0] for field in cursor.description]
    logger = get_logger()

    for row in cursor:
        info_answer = ""
        for f, p in zip(row, row_headers):
            info_answer += f"{p}={(f)}; "
        logger.info(info_answer.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
