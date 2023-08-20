"""Module providing database functionality used by NetClam OSS."""

import os
from time import sleep
from mysql.connector import errorcode
from netclam_common.exception import MySQLConnectionException, RequestNotFoundException
import mysql.connector

MAX_FETCH_RETRIES = 3
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_ENDPOINT = os.environ.get("MYSQL_ENDPOINT")

def get_mysql_conn(username: str, password: str, database: str, hostname: str = "localhost") -> tuple:
    """_summary_

    :param username: MySQL Username
    :type username: str
    :param password: MySQL Password
    :type password: str
    :param database: MySQL Database
    :type database: str
    :param hostname: MySQL Server Hostname, defaults to "localhost"
    :type hostname: str, optional
    :raises Exception: Invalid username/password
    :raises Exception: Invalid database
    :raises Exception: Unknown error
    :return: MySQL Connection, MySQL Cursor
    :rtype: tuple
    """
    try:
        conn = mysql.connector.connect(
            host = hostname,
            user = username,
            password = password,
            database = database
        )
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise MySQLConnectionException(
                "MySQL Error: Invalid username/password or permissions."
            ) from err
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise MySQLConnectionException(
                "MySQL Error: Invalid database."
            ) from err
        else:
            raise MySQLConnectionException(
                "MySQL Error: Unknown error occurred."
            ) from err
    return conn, cursor

def dispose_mysql(conn, cursor):
    """Cleanly disposes of mysql cursor and connection

    :param conn: MySQL connection being disposed
    :type conn: connection.MySQLConnection
    :param cursor: MySQL cursor being disposed
    :type cursor: cursor.MySQLCursor
    """
    cursor.close()
    conn.close()

def fetch_one_mysql(query: str):
    """Fetches the first row of data returned by a MySQL query

    :param query: MySQL query to be executed
    :type query: str
    :return: First row from query result set
    :rtype: tuple
    """
    conn, cursor = get_mysql_conn(mysql_user, mysql_password, mysql_database, mysql_endpoint)
    attempt = 0
    data = None
    while data is None and attempt < max_fetch_retries:
        if attempt > 0:
            sleep(0.10)
        cursor.execute(query)
        data = cursor.fetchone()
        attempt += 1
    dispose_mysql(conn, cursor)
    return data
