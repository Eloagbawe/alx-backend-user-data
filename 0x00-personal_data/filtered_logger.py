#!/usr/bin/env python3
"""This file contains the filter_datum function"""
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """This function returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """The init method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """the format method"""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields,
                            RedactingFormatter.REDACTION,
                            message, RedactingFormatter.SEPARATOR)


def get_logger() -> logging.Logger:
    """creates a logger"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


# start of task 3
def get_db() -> mysql.connector.connection.MySQLConnection:
    """ A function that gets the database credentials and
    returns mysql connection"""
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_passwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=db_user,
        passwd=db_passwd,
        host=db_host,
        database=db_name
    )


# Start of task 4
def main() -> None:
    """
    A function that retrieves all roes in the users table and
    displays each row under a filtered format.
    """
    connection = get_db()
    logger = get_logger()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        str_row = ''.join(
            f"{field}={val}; " for field, val in zip(cursor.column_names, row)
        )
        logger.info(str_row)
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
