from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from application import db, app
import flask_login
from datetime import datetime
from .models import *
from .forms import *
from application.mod_file.controllers import *


mod_assessment = Blueprint('mod_assessment', __name__, url_prefix='/assessment',\
     template_folder='templates/')


@mod_assessment.route('/create/<module_id>/', methods=['POST'])
@flask_login.login_required
def create(module_id):
    form = AssessmentForm(meta={'csrf_token':True})
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        file = request.files['file']
        status, file_id = upload_file(file)
        if status is False:
            return abort(500)
        dateNtime = datetime(year       = form.due_date.data.year,
                            month       = form.due_date.data.month,
                            day         = form.due_date.data.day,
                            hour        = form.due_time.data.hour,
                            minute      = form.due_time.data.minute,
                            microsecond = 0)
        
        aq = AssessmentQuestion(title, file_id, module_id, description, dateNtime)
        db.session.add(aq)
        db.session.commit()
        flash('Assessment Created Successfully')
    else:
        flash('Assessment Created Successfully')

    return redirect(f'/module/view/{module_id}/')



@mod_assessment.route('/list/<module_id>/', methods=['GET'])
@flask_login.login_required
def get_assessments(module_id):
    data = []
    for i in AssessmentQuestion.query.filter_by(module_id = module_id):
        data.append((i.aq_id, i.title, i.due_date))
        print(data)
    
    return jsonify(data=data)












# for i in FileSystem.query.all():
#     db.session.delete(i)
#     db.session.commit()



# for i in AssessmentQuestion.query.all():
#     db.session.delete(i)
#     db.session.commit()