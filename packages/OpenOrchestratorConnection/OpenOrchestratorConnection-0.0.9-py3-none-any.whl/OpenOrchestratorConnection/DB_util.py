"""This module is used internally to handle database actions.
It can be used as a stand-alone module with all static function.
That said the module has some internal state that doesn't work well in parallel threads."""

import pyodbc
from pypika import MSSQLQuery, Table
from OpenOrchestratorConnection import crypto_util

_connection_string = None
_connection = None

def connect(conn_string: str) -> bool:
    """Connect to the database using the given connection string.
    This function saves the connection to be used in a subsequent function calls
    in this module.

    Args:
        conn_string: The connection string.

    Returns:
        bool: True if the connection was successful.
    """
    global _connection, _connection_string # pylint: disable=global-statement

    try:
        conn = pyodbc.connect(conn_string)
        _connection = conn
        _connection_string = conn_string
        return True
    except pyodbc.InterfaceError:
        _connection = None
        _connection_string = None
    
    return False

def catch_db_error(func):
    """A decorator that catches errors in SQL queries"""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pyodbc.DatabaseError as e:
            print(f"Query failed:\n{e}")
            return None
    return inner

def _get_connection() -> pyodbc.Connection:
    """A private function to get the connection created in db_util.connect.

    Raises:
        ValueError: If a connection string has not been set using db_util.connect.
        Exception: Any uncaught exception raised when connecting to the database.

    Returns:
        pyodbc.Connection: The connection object.
    """
    global _connection # pylint: disable=global-statement

    if _connection_string is None:
        raise ValueError("No connection string has been set. Use db_util.connect before calling this function.")
    
    if _connection:
        try:
            _connection.cursor()
            return _connection
        except pyodbc.ProgrammingError as e:
            if str(e) != 'Attempt to use a closed connection.':
                raise e
    
    _connection = pyodbc.connect(_connection_string)
    return _connection

@catch_db_error
def create_log(process_name:str, level:int, message:str) -> None:
    """Create a log in the logs table in the database.

    Args:
        process_name: The name of the process generating the log.
        level: The level of the log (0,1,2).
        message: The message of the log.
    """
    conn = _get_connection()

    logs = Table('Logs')
    command = (
        MSSQLQuery.into(logs)
        .columns(logs.log_level, logs.process_name, logs.log_message)
        .insert(level, process_name, message)
        .get_sql()
    )

    conn.execute(command)
    conn.commit()

@catch_db_error
def get_constant(constant_name:str) -> str:
    """Gets a constants from the constants table in the database.

    Args:
        constant_name: The name of the constant.

    Raises:
        ValueError: If no constant of the given name was found.

    Returns:
        str: The value of the constant.
    """
    conn = _get_connection()

    constants = Table('Constants')
    command = (
        MSSQLQuery.from_(constants)
        .select(constants.constant_value)
        .where(constants.constant_name == constant_name)
        .get_sql()
    )

    result = conn.execute(command).fetchone()
    if result is None:
        raise ValueError(f"No constant with name '{constant_name}' found.")
    
    return result[0]
        

@catch_db_error
def get_credential(credential_name:str) -> tuple[str, str]:
    """Get the username and password of a credential from 
    the credentials table in the database.

    Args:
        credential_name: The name of the credential.

    Raises:
        ValueError: If no credential of the given name was found.

    Returns:
        tuple[str, str]: username, password
    """
    conn = _get_connection()

    credentials = Table('Credentials')
    command = (
        MSSQLQuery.from_(credentials)
        .select(credentials.cred_username, credentials.cred_password)
        .where(credentials.cred_name == credential_name)
        .get_sql()
    )

    result = conn.execute(command).fetchone()
    if result is None:
        raise ValueError(f"No credential with name '{credential_name}' found.")
    
    username, password = result
    password = crypto_util.decrypt_string(password)
    return username, password
    
        

@catch_db_error
def update_constant(constant_name:str, new_value:str) -> None:
    """Update the value of a constant in the constants table in the database.

    Args:
        constant_name: The name of the constant to update.
        new_value: The new value of the constant.

    Raises:
        ValueError: If no constant of the given name was found.
    """
    conn = _get_connection()

    constants = Table('Constants')
    command = (
        MSSQLQuery.update(constants)
        .set(constants.constant_value, new_value)
        .where(constants.constant_name == constant_name)
        .get_sql()
    )

    cursor = conn.execute(command)
    if cursor.rowcount == 0:
        raise ValueError(f"No constant with the name '{constant_name}' was found.")
    conn.commit()

@catch_db_error
def update_credential(credential_name:str, username:str, password:str):
    """Update the username and passwrod of a credential in the credentials
    table in the database. The password is automatically encrypted using AES.
    Remember to use crypto_util.set_key before calling this function.

    Args:
        ccredential_name: The name of the credential to update.
        username: The new username of the credential.
        password: The new password of the credential.

    Raises:
        ValueError: If no credential of the given name was found.
    """
    conn = _get_connection()

    password = crypto_util.encrypt_string(password)

    credentials = Table('Credentials')
    command = (
        MSSQLQuery.update(credentials)
        .set(credentials.cred_username, username)
        .set(credentials.cred_password, password)
        .where(credentials.cred_name == credential_name)
        .get_sql()
    )

    cursor = conn.execute(command)
    if cursor.rowcount == 0:
        raise ValueError(f"No credential with the name '{credential_name}' was found.")
    conn.commit()
