from flask import Flask
import os

app = Flask(__name__, static_url_path='/static', instance_relative_config=True)

from app import views

app.config.from_object(os.environ.get('APP_SETTINGS','config.DevelopmentConfig'))