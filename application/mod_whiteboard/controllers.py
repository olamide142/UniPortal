from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
# from application.mod_whiteboard.models import Whiteboard
from application import db, app
import flask_login


mod_whiteboard = Blueprint('mod_whiteboard', __name__, url_prefix='/whiteboard',\
     template_folder='templates/')

@mod_whiteboard.route('/', methods=['GET'])
@flask_login.login_required
def index():
    return render_template('whiteboard/index.html')

@mod_whiteboard.route('/view/<board_id>', methods=['GET'])
@flask_login.login_required
def view(board_id):
    return render_template('whiteboard/the_board.html')