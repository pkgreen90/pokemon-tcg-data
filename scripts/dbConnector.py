import argparse
import configparser
import csv
import logging
import sqlite3
from sqlite3 import Error
from typing import TypeVar

# Global variables
T = TypeVar('T')

def get_logger(name: str) -> T:
    """ Get a handle to a pre-configured logger object

    :param name: The name of the logger

    :returns: The logger
    :rtype: Logger
    """
    handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt='%(asctime)s %(lineno)s %(name)s.%(funcName)s() %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

def create_connection(db_file: str) -> T:
    """ Create a database connection to an SQLite database
    
    :param db_file: The file path to the database
    
    :returns: A conection to the database
    :rtype: Connection
    """

    logger = get_logger('main')
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        logger.error(e)

def parse_args() -> tuple:
    """ Parser function to extract and process command line args
    
    :return: The configuration data
    :rtype: tuple
    """

    logger = get_logger('main')

    parser = argparse.ArgumentParser(
        description='Connection to database manager'
    )
    parser.add_argument(
        '-d', '--db-file', type=str, required=True,
        help='A file path to the database file including database'
    )
    parser.add_argument(
        '-l', '--log-level', type=str, required=False, 
        default='INFO', help='Sets the log level (default=INFO',
        choices=['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']
    )
    parser.add_argument(
        '-f', '--file-path', type=str, required=True, 
        help='The path and file to load data from'
    )
    parser.add_argument(
        '-t', '--table', type=str, required=True,
        help='The table name to insert data into'
    )

    args = parser.parse_args()

    logging.getLogger().setLevel(args.log_level)
    logger.debug(f'Set log level to {args.log_level}')

    args_valid = True
    
    if args.db_file == None or args.db_file == '':
        logger.error(f'No database File parameter found')
        args_valid = False

    if args.file_path == None or args.file_path == '':
        logger.error(f'No file path found')
        args_valid = False

    if args.table == None or args.table == '':
        logger.error(f'No table name provided')
        args_valid = False

    if not args_valid:
        logger.warning('Command line args not valid')
        quit()
    
    return (args.db_file, args.file_path, args.table)

def get_tables(conn: T) -> list:
    """Gets a list of all the tables within the database

    :param conn: A connection to allow execution on the DB

    :returns: A list of tuples for all tables in the database
    :rtype: list
    """
    logger = get_logger('main')
    conn_cursor = conn.cursor()
    conn_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = conn_cursor.fetchall()
    table_list = list()
    for item in tables:
        table_list.append(item[0])
    logger.debug(f'Tables in database: {table_list}')

    return table_list

def insert_table_row(sql_line: str, conn_cursor: T, data: list) -> None:
    """Inserts a singe row of data into the database

    :param sql_line: The sql line to be used for command execution
    :param conn_cursor: A connection to allow execution on the DB
    :param data: A list of data to be insert into a single row
    """
    logger = get_logger('main')
    logger.debug(f'SQL Command ({sql_line})')
    logger.debug(f'Data to be inserted ({data})')
    conn_cursor.execute(sql_line, data)

def load_table_data(file_name: str, table_name: str, conn: T) -> None:
    """Inserts a set of data into a chosen table

    :param file_name: The name of the file including path to load
    :param table_name: The name of the table to insert the data into
    :param conn: A connection to allow execution on the DB
    """
    logger = get_logger('main')
    conn_cursor = conn.cursor()
    with open(file_name) as f:
        logger.debug(f'Opening file {file_name} to extract data and insert into table {table_name}')
        headers = str()
        val_str = str()
        sql_line = f'INSERT INTO {table_name}(HEADERS) VALUES(VALS)'
        headers_extracted = False

        rd = csv.reader(f, delimiter='\t')
        for row in rd:
            # Extract the header from the first line read in
            if headers_extracted == False:
                # Construct the header
                headers = ','.join(row)
                logger.debug(f'Headers extracted as ({headers})')
                headers_extracted = True
                sql_line = sql_line.replace('HEADERS', headers, 1)

                # Construct the value string
                val_list = list()
                for n in range(len(row)):
                    val_list.append('?')
                val_str = ','.join(val_list)
                logger.debug(f'Value string will be used as ({val_str})')
                sql_line = sql_line.replace('VALS', val_str, 1)

                continue

            logger.debug(f'Row data extracted: {row}')

            # Process the row and replace empty values with NULLS
            valid_row = list()
            for row_item in row:
                if row_item == None or row_item == "":
                    valid_row.append(None)
                else:
                    valid_row.append(row_item)
            
            logger.debug(f'Row data converted into {valid_row}')

            insert_table_row(sql_line, conn_cursor, tuple(valid_row))
        conn.commit()

def main() -> None:
    """ Main entry point into program"""
    logging.getLogger().setLevel(logging.INFO)
    logger = get_logger('main')
    logger.info("Program starting...")
    db_file, file_path, table_name = parse_args()

    conn = create_connection(db_file)
    conn.execute("PRAGMA foreign_keys = 0")

    table_list = get_tables(conn)

    if table_name in table_list:
        logger.debug(f'Table {table_name} found in tablle listing')
    else:
        logger.error(f'Table {table_name} not found, quiting...')
        quit()
    load_table_data(
        file_path,
        table_name,
        conn
    )

    conn.close()
    logger.info("Closed database connection, program complete")


if __name__ == '__main__':
    main()
    