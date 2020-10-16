from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from application.mod_whiteboard.models import *
from application.mod_auth.controllers import get_user_object
from .forms import CreateBoard
from application import db, app
import flask_login


mod_whiteboard = Blueprint('mod_whiteboard', __name__, url_prefix='/board',\
     template_folder='templates/')


@mod_whiteboard.route('/', methods=['GET'])
@flask_login.login_required
def index():
    u = get_user_object(str(flask_login.current_user))
    pb = PinBoard.query.filter_by(username=u.username)
    form = CreateBoard()

    return render_template(
        'board/index.html',
        form = form,
        pb = pb,
        current_user = str(flask_login.current_user))



@mod_whiteboard.route('/view/<board_id>', methods=['GET'])
@flask_login.login_required
def view(board_id):
    # checkk the board is valid
    if Board.query.filter_by(board_id=board_id).first() is not None:
        return render_template(
            'board/the_board.html',
            board_room = board_id,
            current_user = str(flask_login.current_user))
    else:
        return abort(404)


def save_draw_info(board_id, line):
    b = Board.query.filter_by(board_id=board_id).first()
    f = open(f'application/mod_whiteboard/boardfile/{b.file_name}', 'a')
    f.write(f'{line}\n')
    f.close()


@mod_whiteboard.route('/create/', methods=['POST'])
@flask_login.login_required
def create():
    form = CreateBoard(meta={'csrf_token' : True})
    if form.validate_on_submit():
        u = get_user_object(str(flask_login.current_user))
        b = Board(u.username, form.name.data)
        db.session.add(b)
        db.session.commit()
        return redirect(f'/board/view/{b.board_id}')
    else:
        return "Form is not valid"


@mod_whiteboard.route('/pin_a_board/<board_id>/', methods=['GET'])
@flask_login.login_required
def pin_a_board(board_id):
    u = get_user_object(str(flask_login.current_user))
    pb = PinBoard(username=u.username, board_id=board_id)
    db.session.add(pb)
    db.session.commit()
    return redirect(f'/board/')



@mod_whiteboard.route('/search/', methods=['GET'])
@flask_login.login_required
def search_board():
    board_id = request.args['board_id']
    pb = PinBoard.query.filter_by(board_id=board_id)
    db.session.add(pb)
    db.session.commit()
    return redirect(f'/board/')




@app.template_filter('board_info')
def get_board_info(board_id):
    u = Board.query.filter_by(board_id=board_id).first()
    return u.board_name
