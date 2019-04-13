import logging
import logging.config
import os
import sqlite3
from sqlite3 import Error

from flask import render_template, render_template_string, request
from flask_user import (UserManager, UserMixin, current_user, login_required,
                        roles_required)

from app import app
from utils.database import create_connection
from utils.decorators import timeit
from utils.helpers import log_line

logger = logging.getLogger(__name__)



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
    """The Home page is accessible to anyone"""
    return render_template('index.html')

@timeit
@app.route('/listing')
@login_required
def member_page():
    """The listing page is only accessible to authenticated users"""
    return render_template("listing.html")


@timeit
@app.route('/admin')
@roles_required('Admin')    # Use of @roles_required decorator
def admin_page():
    """The Admin page requires an 'Admin' role."""
    return render_template('admin.html')
