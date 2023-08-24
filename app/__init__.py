from flask import Flask
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT + "/static"
app = Flask(__name__)
app.secret_key = "qpwoeiruty"

from app import views
from app import admin_views


