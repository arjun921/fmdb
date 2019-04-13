import logging
import logging.config
import os

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
#     global DB_URI
#     DB_URI = app.config['SQLALCHEMY_DATABASE_URI']

# def db_connection():
#     global connection
#     global cur

#     cur = connection.cursor()
#     print("DB Connection successful.")

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
@timeit
@app.route('/')
def home_page():
    """The Home page is accessible to anyone. Function in app.views"""
    return render_template('index.html')


@timeit
@app.route('/listing')
@login_required
def member_page():
    """The listing page is only accessible to authenticated users.  Function in app.views"""
    DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
    DB_URI = DB_URI.split('///')[1]
    db_conn = create_connection(DB_URI)
    movie_list = select_all(db_conn,'movie_data')
    return render_template("listing.html",movie_list=movie_list)


@timeit
@app.route('/admin')
@roles_required('Admin')    # Use of @roles_required decorator
def admin_page():
    """The Admin page requires an 'Admin' role. Function in app.views"""
    return render_template('admin.html')
