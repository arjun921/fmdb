import sqlite3
from sqlite3 import Error
import logging
from utils.helpers import log_line
from utils.decorators import timeit

logger = logging.getLogger(__name__)


@timeit
def create_connection(db_uri):
    """Creating db connection in utils.database"""
    log_line(logger, msg=db_uri)
    try:
        conn = sqlite3.connect(db_uri)
        return conn
    except Error as e:
        log_line(logger, level='critical', msg=str(e), trace=False, exit=True)


@timeit
def select_all(conn, db):
    """Creating db connection in utils.database"""
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {db}")
    rows = cur.fetchall()
    conn.close()
    return rows


@timeit
def select_all_where_value_matches(conn, db, field, match_string):
    """Creating db connection in utils.database"""
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM {db} WHERE {field}="{match_string}"')
    rows = cur.fetchall()
    conn.close()
    return rows


@timeit
def select_all_with_similar_value(conn, db, field, matches):
    """Creating db connection in utils.database"""
    cur = conn.cursor()
    matches = matches.lower()
    matches = '%'+'%'.join(matches.split(' '))+'%'
    query = f'SELECT * FROM {db} WHERE {field} like "{matches}"'
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_by_id(conn, db, id):
    cur = conn.cursor()
    query = f'DELETE FROM {db} WHERE id=?'
    cur.execute(query, (id,))
    conn.commit()
    conn.close()
    return 'Success'


def create_by_id(conn, db, params):
    cur = conn.cursor()
    query = f"INSERT INTO movie_data(popularity,director,genre,imdb_score,name) VALUES ({float(params['popularity'])}, '{params['director']}','{params['chip_genres']}',{float(params['imdb_score'])},'{params['movie_name']}')"
    print(query)
    cur.execute(query)
    conn.commit()
    conn.close()
    return 'Success'
