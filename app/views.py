import logging
import logging.config
import os
from math import floor

from flask import render_template, render_template_string, request
from flask_user import (UserManager, UserMixin, current_user, login_required,
                        roles_required)

from app import app
from utils.database import create_connection, select_all, select_all_where_value_matches, select_all_with_similar_value
from utils.decorators import timeit
from utils.helpers import log_line

logger = logging.getLogger(__name__)


# @app.before_first_request
# def initialize():
#     DB_URI = app.config['SQLALCHEMY_DATABASE_URI']


# # Webservices
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     req = request.get_json(silent=True, force=True)
#     print("Request:")
#     print(json.dumps(req, indent=4))
#     res = makeWebhookResult(req)
#     res = json.dumps(res, indent=4)
#     r = make_response(res)
#     r.headers['Content-Type'] = 'application/json'
#     return r


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
    movie_list = select_all(db_conn,'movie_data')
    # for pagination
    page = int(request_query.get('p',"0"))
    num_items = int(request_query.get('items',app.config.get('MAX_LISTING_ITEMS','50')))
    start = page*num_items
    if start==0:
        # if start zero, set slice end to number of items per page
        end = num_items
    else:
        # increment end by page number
        end = start+(num_items)
    max_pages = floor(len(movie_list)/num_items)
    # if name in request_query or director in request_query or genre in request_query:

    return render_template("listing.html",movie_list=movie_list[start:end],current_page=page,max_pages=max_pages,full_movie_list=movie_list)


@app.route('/admin')
@roles_required('Admin')    # Use of @roles_required decorator
def admin_page():
    """The Admin page requires an 'Admin' role. Function in app.views"""
    return render_template('admin.html')
