import os
import logging

from flask import Flask, redirect
from flask_login import current_user, LoginManager
from flask_mongoengine import MongoEngine

from dto.result import ResponseDto
from logutils import init_logging
from services.auth import AuthService
from utils import ObjectIDConverter, run, ist_tmz_formatter
from controllers.calendar import calendar_blueprint
from controllers.auth import auth_blueprint
from controllers.user import user_blueprint

init_logging()
application = Flask(__name__)
application.config.from_pyfile('config/dev.cfg', silent=True)
application.url_map.strict_slashes = False
application.url_map.converters['objectid'] = ObjectIDConverter
application.jinja_env.filters['ist_tmz_formatter'] = ist_tmz_formatter

for i in application.config:
    os.environ[i] = str(application.config[i])
db = MongoEngine(application)

# login user
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "auth_blueprint.login"

application.register_blueprint(calendar_blueprint)
application.register_blueprint(auth_blueprint)
application.register_blueprint(user_blueprint)


@login_manager.unauthorized_handler
def unauthorized():
    if not current_user.is_authenticated:
        return ResponseDto(status=-1, msg="Unauthorized User").to_json()
    else:
        return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    return AuthService.get_session_user_by_email(user_id)


@application.after_request
def add_security_headers(resp):
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp


@application.errorhandler(401)
def handle_error(error):
    logging.exception(error)
    return ResponseDto(status=-1, msg="Unauthorized User").to_json()


@application.errorhandler(404)
def page_not_found(e):
    logging.exception(e)
    return ResponseDto(status=-1, msg="Page Not Found").to_json()


@application.errorhandler(500)
def service_unavailable(e):
    logging.exception(e)
    return ResponseDto(status=-1, msg="Something went bad.")


@application.errorhandler(Exception)
def handle_error(error):
    logging.exception(error)
    return 'Internal Server Error', 503


if __name__ == "__main__":
    run(application)
