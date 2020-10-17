from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from application import db, app
import flask_login
from .forms import *


mod_chat = Blueprint('mod_chat', __name__, url_prefix='/chat',\
     template_folder='templates/')



@mod_chat.route('/', methods=['GET'])
@flask_login.login_required
def index():
    return render_template('chat/index.html')