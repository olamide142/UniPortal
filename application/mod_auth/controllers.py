from flask import Blueprint, request, render_template,flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from werkzeug.security import check_password_hash
from application.mod_auth.models import User
from application import db, app
import flask_login
from .forms import SignupForm

# Login manger setup
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('mod_auth', __name__, url_prefix='/auth',\
     template_folder='templates/mod_auth')
login_manager.login_view = "mod_auth.login"


@mod_auth.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


# Set the route and accepted methods
@mod_auth.route('/signup/', methods=['POST', 'GET'])
def signup():
    '''
    Register a user onto the platform
    returns: flask.jsonify()
    '''
    form = SignupForm(meta={'csrf': False})
    if form.validate_on_submit():
        try:
            user = User(form.username.data, form.email.data, form.password.data, \
                form.first_name.data, form.last_name.data)
            db.session.add(user)
            db.session.commit()
        except Exception:
            return jsonify(status=False, error="Account Creation was Unsuccessfull")
        return jsonify(status=True, msg="Account Created Successfully")
    else:
        return jsonify(status=False, error="Form submitted was invalid")

@mod_auth.route('/see/', methods=['GET'])
def see():
    '''
    Register a user onto the platform
    returns: flask.jsonify()
    '''
    db.drop_all(bind=None)
    return ""