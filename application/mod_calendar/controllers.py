from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from application.mod_calendar.models import Event
from .forms import CreateEventForm
from application import db, app
import flask_login
from datetime import datetime


mod_calendar = Blueprint('mod_calendar', __name__, url_prefix='/calendar',\
     template_folder='templates/')


@mod_calendar.route('/create/', methods=['POST'])
@flask_login.login_required
def create_event():
    form = CreateEventForm(meta={'csrf_token':True})
    if form.validate_on_submit():
        title = form.title.data
        module_id = form.module_id.data

        dateNtime = datetime(year       = form.date.data.year,
                            month       = form.date.data.month,
                            day         = form.date.data.day,
                            hour        = form.time.data.hour,
                            minute      = form.time.data.minute,
                            microsecond = 0)

        e = Event(
            str(flask_login.current_user),
            title, 
            module_id, 
            dateNtime)
        db.session.add(e)
        db.session.commit()

        return redirect(f'/module/view/{form.module_id.data}')


@mod_calendar.route('/view/', methods=['GET'])
@flask_login.login_required
def view_calendar():
    section = request.args['section']
    
    #View module calendar
    if section == 'module':
        e = Event.query.filter_by(module_id=request.args['module_id'])
        data = []
        for i in e:
            data.append((i.event_id, i.title, i.date_n_time))
        return jsonify(data=data)
    #view personal calendar
    # pass 