from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from application import db, app
import flask_login
from datetime import datetime
from .models import *
from .forms import *
from application.mod_module.controllers import *
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



@mod_assessment.route('/view/<aq_id>/', methods=['GET'])
@flask_login.login_required
def view(aq_id):
    ass = AssessmentQuestion.query.filter_by(aq_id=aq_id).first()
    username = str(flask_login.current_user)
    # can submit
    # if the user has submitted 
    # they can't submit agian except they delete previous one
    aaa = Assessment.query.filter_by(username=username,\
         module_id=ass.module_id, aq_id = aq_id).first()
    can_submit = False

    if (datetime.now() < ass.due_date) and (aaa is None):
        can_submit = True
    # is current user the owner of this module
    owner = False
    m = get_module_object(ass.module_id)
    bbb = Assessment.query.filter_by(module_id=ass.module_id, aq_id = aq_id)
    if m.module_tutor_id == username:
        owner = True

    return render_template('assessment/view.html',
    title = ass.title,
    form = AssessmentForm2(),
    due_date = ass.due_date,
    description = ass.description,
    can_submit = can_submit,
    module_id = ass.module_id,
    aq_id = aq_id,
    aaa = aaa,
    bbb = bbb,
    owner = owner)



@mod_assessment.route('/upload_assessment/<aq_id>/', methods=['POST'])
@flask_login.login_required
def upload_assessment(aq_id):
    form = AssessmentForm2(meta={'csrf_token':True})
    file = request.files['file']
    status, file_id = upload_file(file)
    if status:
        module_id = form.module_id.data
        username = str(flask_login.current_user)
        ass = Assessment(aq_id, username, file_id, module_id)
        db.session.add(ass)
        db.session.commit()
        flash('You have Successfully Submitted this Assessment')
    else:
        flash('Something went wrong while you were trying to submit Assessment')

    return redirect(f'/assessment/view/{aq_id}/')
    


@mod_assessment.route('/<assessment_id>/update_score/', methods=['GET'])
@flask_login.login_required
def update_score(assessment_id):
    score = request.args['score']
    remark = request.args['remark']
    a = Assessment.query.filter_by(assessment_id=assessment_id).first()
    a.score = score
    a.remark = remark
    db.session.add(a)
    db.session.commit()
    return redirect(f'/assessment/view/{a.aq_id}/')



