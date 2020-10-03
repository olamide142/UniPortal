from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from werkzeug.security import check_password_hash
from application.mod_auth.models import User
from application import db, app
import flask_login


mod_main = Blueprint('mod_main', __name__, url_prefix='/',\
     template_folder='templates/')

@mod_main.route('/', methods=['GET'])
def index():
    # return "Main Page"
    return render_template('index.html')


