from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from application.mod_calendar.models import Calendar, Event
from application import db, app
import flask_login


mod_calendar = Blueprint('mod_calendar', __name__, url_prefix='/calendar',\
     template_folder='templates/')

@mod_calendar.route('/', methods=['GET'])
@flask_login.login_required
def index():
    return render_template('calendar/index.html')

def create_event():
    pass


def view_calendar():
    #view personal calendar
    #View module calendar
    pass


def add_event_to_calendar():
    pass

def remove_event_from_calendar():
    pass


def create_event_under_module():
    pass


