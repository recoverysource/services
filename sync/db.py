'''
Internal Database
'''
import logging
import os
import pathlib
import sqlite3

# Container for loaded database
open_database = None


def open(dbpath):
    '''
    Open a sqlite3 database, initializing it if not present
    '''
    global open_database

    # Close any open handler
    if open_database:
        open_database.close()

    # Ensure parent directory exists
    parent = pathlib.Path(os.path.dirname(dbpath))
    parent.mkdir(parents=True, exist_ok=True)

    # Open sqlite3 database
    logging.debug(f'Connecting to database at {dbpath}')
    open_database = sqlite3.connect(dbpath)

    # Initialize schema
    cursor = open_database.cursor()
    cursor.executescript('''
        BEGIN;
        CREATE TABLE IF NOT EXISTS store (
            key TEXT PRIMARY KEY,
            value BLOB NOT NULL);
        CREATE TABLE IF NOT EXISTS geostore (
            key TEXT PRIMARY KEY,
            lon REAL NOT NULL,
            lat REAL NOT NULL,
            value BLOB NOT NULL,
            CONSTRAINT unique_geostore_key_lon_lat UNIQUE (key, lon, lat));
        CREATE INDEX IF NOT EXISTS idx_geostore_lon ON geostore (lon);
        CREATE INDEX IF NOT EXISTS idx_geostore_lat ON geostore (lat);
        COMMIT;
        ''')


def exists(key, table='store'):
    '''
    Return True if a key exists in data store
    '''
    global open_database
    cursor = open_database.cursor()
    cursor.execute(
            f'SELECT COUNT(key) FROM {table} WHERE key=?;',
            (key,))
    rowcount = cursor.fetchall()[0][0]
    if rowcount == 0:
        return False
    elif rowcount == 1:
        return True
    raise Exception('Duplicate keys detected in data store')


def geo_exists(key):
    '''
    Return True if a key exists in geo store
    '''
    return exists(key, 'geostore')


def get(key, default=None, table='store'):
    '''
    Return stored value for a given key
    '''
    global open_database
    cursor = open_database.cursor()
    # logging.debug(f'fetching key:{key}')
    cursor.execute(
            f'SELECT value FROM {table} WHERE key=?;',
            (key,))
    rows = cursor.fetchall()
    if len(rows) == 0:
        return default
    elif len(rows) == 1:
        return rows[0][0]
    raise Exception('Duplicate keys detected in data store')


def geo_get(key, default=None):
    '''
    Return stored geo data for a given key
    '''
    return get(key, default, 'geostore')


def geo_search(minlon=None, maxlon=None, minlat=None, maxlat=None):
    '''
    Return results for a given geo search
    '''
    global open_database
    cursor = open_database.cursor()

    # Base SQL query
    sql_query = 'SELECT key, lon, lat, value FROM geostore WHERE 1=1'

    # Append conditions based on provided parameters
    if minlon is not None:
        sql_query += ' AND lon >= ?'
    if maxlon is not None:
        sql_query += ' AND lon <= ?'
    if minlat is not None:
        sql_query += ' AND lat >= ?'
    if maxlat is not None:
        sql_query += ' AND lat <= ?'

    # Add appropriate arguments to query
    params = []
    if minlon is not None:
        params.append(minlon)
    if maxlon is not None:
        params.append(maxlon)
    if minlat is not None:
        params.append(minlat)
    if maxlat is not None:
        params.append(maxlat)

    # Fetch search results
    logging.debug(f'geo search: {sql_query}')
    cursor.execute(sql_query, tuple(params))
    return cursor.fetchall()


def set(key, value):
    '''
    Add key/value into storage
    '''
    global open_database
    cursor = open_database.cursor()
    # logging.debug(f'setting key:{key}')
    cursor.execute(
            'INSERT OR REPLACE INTO store (key, value)'
            'VALUES (?, ?);',
            (key, value,))
    open_database.commit()


def geo_set(key, lon, lat, value):
    '''
    Add key/value into geo storage
    '''
    global open_database
    cursor = open_database.cursor()
    # logging.debug(f'setting geo key:{key}')
    cursor.execute(
            'INSERT OR REPLACE INTO geostore (key, lon, lat, value)'
            'VALUES (?, ?, ?, ?);',
            (key, lon, lat, value,))
    open_database.commit()
