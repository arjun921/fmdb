import logging
import sqlite3
from sqlite3 import Error

from utils.decorators import timeit
from utils.helpers import log_line

logger = logging.getLogger(__name__)

from app import app

@timeit
def create_connection():
    """Creating db connection in utils.database"""
    DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
    DB_URI = DB_URI.split('///')[1]
    log_line(logger, msg=DB_URI)
    try:
        conn = sqlite3.connect(DB_URI)
        return conn
    except Error as e:
        log_line(logger, level='critical', msg=str(e), trace=False, exit=True)


@timeit
def select_all(db):
    """Select all from db in utils.database"""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(db))
    rows = cur.fetchall()
    conn.close()
    return rows


@timeit
def select_all_where_value_matches(db, field, match_string):
    """Select all by condition in utils.database"""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM {} WHERE {}="{}"'.format(db,field,match_string))
    rows = cur.fetchall()
    conn.close()
    return rows


@timeit
def select_all_with_similar_value(db, field, matches):
    """Select all where similar value matches in utils.database"""
    conn = create_connection()
    cur = conn.cursor()
    matches = matches.lower()
    matches = '%'+'%'.join(matches.split(' '))+'%'
    query = 'SELECT * FROM {} WHERE {} like "{}"'.format(db,field,matches)
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows


@timeit
def delete_by_id(db, id):
    """Delete row by id in utils.database"""
    conn = create_connection()
    cur = conn.cursor()
    query = 'DELETE FROM {} WHERE id=?'.format(db)
    cur.execute(query, (id,))
    conn.commit()
    conn.close()
    return 'Success'


@timeit
def insert_record(db, params):
    """Insert in db in utils.database"""
    conn = create_connection()
    cur = conn.cursor()
    query = "INSERT INTO movie_data(popularity,director,genre,imdb_score,name) VALUES ({}, '{}','{}',{},'{}')".format(float(params['popularity']),params['director'],params['genres'],float(params['imdb_score']),params['movie_name'])
    cur.execute(query)
    conn.commit()
    conn.close()
    return 'Success'


@timeit
def update_record(db, params):
    """Insert in db in utils.database"""
    conn = create_connection()
    cur = conn.cursor()
    query = "UPDATE movie_data SET popularity = {},director='{}',genre='{}',imdb_score={},name='{}' WHERE ID = {};".format(float(params['popularity']),params['director'],params['genres'],float(params['imdb_score']),params['movie_name'],params['id'])
    cur.execute(query)
    conn.commit()
    conn.close()
    return 'Success'
