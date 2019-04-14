import logging
import logging.config
import os
from math import floor

from flask import render_template, render_template_string, request
from flask_user import (UserManager, UserMixin, current_user, login_required,
                        roles_required)

from app import app
from utils.database import (create_connection, select_all,
                            select_all_where_value_matches,
                            select_all_with_similar_value, create_by_id)
from utils.decorators import timeit
from utils.helpers import log_line

logger = logging.getLogger(__name__)


# web page routes
@app.route('/')
def home_page():
    """The Home page is accessible to anyone. Function in app.views"""
    return render_template('index.html')


@app.route('/listing')
@login_required
def member_page():
    """The listing page is only accessible to authenticated users.  Function in app.views"""
    request_query = dict(request.args)
    DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
    DB_URI = DB_URI.split('///')[1]
    db_conn = create_connection(DB_URI)

    # select all for search autocomplete.
    movie_list = select_all(db_conn, 'movie_data')
    searched = False

    # search
    if 'name' in request_query:
        search_results = select_all_with_similar_value(
            db_conn, db='movie_data', field='name', matches=request_query['name'])
        searched = True
    elif 'director' in request_query:
        search_results = select_all_with_similar_value(
            db_conn, db='movie_data', field='director', matches=request_query['director'])
        searched = True
    elif 'genre' in request_query:
        search_results = select_all_with_similar_value(
            db_conn, db='movie_data', field='genre', matches=request_query['genre'])
        searched = True

    # pagination
    page = int(request_query.get('p', "0"))
    num_items = int(request_query.get(
        'items', app.config.get('MAX_LISTING_ITEMS', '50')))
    start = page*num_items

    if start == 0:
        # if start zero, set slice end with number of items per page
        end = num_items
    else:
        # add number of items to start position
        end = start+(num_items)

    # assign to common variable for reducing duplicate code
    if searched:
        render_movies = search_results
    else:
        render_movies = movie_list

    max_pages = floor(len(render_movies)/num_items)
    return render_template("listing.html", movie_list=render_movies[start:end], current_page=page, max_pages=max_pages, full_movie_list=movie_list)


@app.route('/admin')
@roles_required('Admin')    # Use of @roles_required decorator
def admin_page():
    """The Admin page requires an 'Admin' role. Function in app.views"""
    DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
    DB_URI = DB_URI.split('///')[1]
    db_conn = create_connection(DB_URI)

    # select all for search autocomplete.
    full_movie_list = select_all(db_conn, 'movie_data')
    return render_template('admin.html', full_movie_list=full_movie_list)


@app.route('/manage/delete/<int:id>', methods=['DELETE'])
@roles_required('Admin')
def delete_entry(id):
    """DESTRUCTIVE FUNCTION AHEAD. Function in app.views"""
    DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
    DB_URI = DB_URI.split('///')[1]
    db_conn = create_connection(DB_URI)
    returned = delete_by_id(db_conn, 'movie_data', id)
    if returned == 'Success':
        return 'Success'


@app.route('/manage/add', methods=['POST'])
@roles_required('Admin')
def add_movie_entry():
    """DESTRUCTIVE FUNCTION AHEAD. Function in app.views"""
    req_body = request.get_json(silent=True, force=True)
    DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
    DB_URI = DB_URI.split('///')[1]
    db_conn = create_connection(DB_URI)
    returned = create_by_id(db_conn, 'movie_data', req_body)
    if returned == 'Success':
        return 'Success'
