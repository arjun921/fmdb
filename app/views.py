import logging
import logging.config
import os
from math import floor

from flask import render_template, render_template_string, request
from flask_user import (UserManager, UserMixin, current_user, login_required,
                        roles_required)

from app import app
from utils.database import (insert_record, create_connection, delete_by_id,
                            select_all, select_all_where_value_matches,
                            select_all_with_similar_value,update_record)
from utils.decorators import timeit
from utils.helpers import log_line,str_special_char_strip

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
    # select all for search autocomplete.
    movie_list = select_all(db='movie_data')
    searched = False

    # search
    # regex used to remove special characters for db sanity
    if 'name' in request_query:
        clean_search_string = str_special_char_strip(request_query['name'])
        search_results = select_all_with_similar_value(
            db='movie_data', field='name', matches=clean_search_string)
        searched = True
    elif 'director' in request_query:
        clean_search_string = str_special_char_strip(request_query['director'])
        search_results = select_all_with_similar_value(
            db='movie_data', field='director', matches=clean_search_string)
        searched = True
    elif 'genre' in request_query:
        clean_search_string = str_special_char_strip(request_query['genre'])
        search_results = select_all_with_similar_value(
            db='movie_data', field='genre', matches=clean_search_string)
        searched = True

    # pagination
    page = int(request_query.get('p', "0"))
    default_num_items = app.config.get('MAX_LISTING_ITEMS', '30')
    num_items = int(request_query.get('items', default_num_items))
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

    # select all for search autocomplete.
    full_movie_list = select_all(db='movie_data')
    return render_template('admin.html', full_movie_list=full_movie_list)


@app.route('/manage/delete/<int:id>', methods=['DELETE'])
@roles_required('Admin')
def delete_entry(id):
    """DESTRUCTIVE FUNCTION AHEAD. Function in app.views"""
    returned = delete_by_id(db='movie_data',id=id)
    if returned == 'Success':
        return 'Success'


@app.route('/manage/add', methods=['POST'])
@roles_required('Admin')
def add_movie_entry():
    """Add new movie using the following JSON body.
    ---
    {
        'movie_name': 'STR',
        'director': 'STR',
        'popularity': 'FLOAT',
        'genres': 'STR',
        'imdb_score': 'FLOAT'
    }
    ---
     Function in app.views"""
    req_body = request.get_json(silent=True, force=True)
    # removing special characters for db sanity
    req_body_clean = {
        'movie_name': str_special_char_strip(req_body['movie_name']),
        'director': str_special_char_strip(req_body['director']),
        'popularity': str_special_char_strip(req_body['popularity']),
        'genres': str_special_char_strip(req_body['genres']),
        'imdb_score': str_special_char_strip(req_body['imdb_score'])
    }
    returned = insert_record(db='movie_data',params=req_body_clean)
    if returned == 'Success':
        return 'Success'

@app.route('/manage/update', methods=['POST'])
@roles_required('Admin')
def update_movie_entry():
    """Update movie using the following JSON body.
    ---
    {   
        'id': 'INT'
        'movie_name': 'STR',
        'director': 'STR',
        'popularity': 'FLOAT',
        'genres': 'STR',
        'imdb_score': 'FLOAT'
    }
    ---
    Function in app.views"""
    req_body = request.get_json(silent=True, force=True)
    # removing special characters for db sanity
    req_body_clean = {
        'id': str_special_char_strip(req_body['id']),
        'movie_name': str_special_char_strip(req_body['movie_name']),
        'director': str_special_char_strip(req_body['director']),
        'popularity': str_special_char_strip(req_body['popularity']),
        'genres': str_special_char_strip(req_body['genres']),
        'imdb_score': str_special_char_strip(req_body['imdb_score'])
    }
    returned = update_record(db='movie_data',params=req_body_clean)
    if returned == 'Success':
        return 'Success'

