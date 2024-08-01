#!/usr/bin/env python3
"""
Module for handling personal data with a focus on privacy
"""
from typing import List
import re
import logging
from os import environ
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Redacts specified fields in a log entry"""
    regex_pattern = '|'.join(
        [f'{re.escape(f)}=.*?{re.escape(separator)}' for f in fields]
    )
    return re.sub(
        regex_pattern,
        lambda m: f'{m.group(0).split("=")[0]}={redaction}{separator}',
        message
    )


def get_logger() -> logging.Logger:
    """Configures and returns a Logger instance"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Establishes a connection to a MySQL database"""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(user=username, password=password,
                                   host=host, database=db_name)


def main():
    """
    Establishes a database connection, retrieves user data,
    and logs each entry with sensitive information redacted
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = '; '.join(f'{f}={str(r)}' for f, r in zip(field_names, row))
        logger.info(str_row)

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """Custom formatter for obfuscating sensitive fields"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Redacts sensitive fields in log messages"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


if __name__ == '__main__':
    main()
