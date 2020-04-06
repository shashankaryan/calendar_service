from flask import Blueprint, request, current_app
from services.auth import AuthService
from dto.result import ResponseDto

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/login/', methods=["POST"])
def login():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    remember = True if request.form.get('remember') else False
    if not email.strip() or not password.strip() or not AuthService.validate_email(email):
        return ResponseDto(status=-1, msg='Data Incomplete/Invalid.').to_json()

    response = AuthService.login(email=email, password=password, remember=remember)
    if not response['value']:
        return ResponseDto(status=-1, msg=response['error']).to_json()
    return ResponseDto(status=0, msg=response['msg'], result=response['data']).to_json()


@auth_blueprint.route('/register/', methods=["POST"])
def register():
    email = request.form.get('email', '')
    name = request.form.get('name', '')
    password = request.form.get('password', '')
    confirm = request.form.get('confirmPassword', '')
    if not email.strip() or not password.strip() or not name.strip() or not confirm.strip() or password != confirm\
            or not AuthService.validate_email(email):
        return ResponseDto(status=-1, msg='Data Incomplete/Invalid or Password Mismatch').to_json()

    response = AuthService.create_user(email=email, name=name, password=password)
    if not response['value']:
        return ResponseDto(status=-1, msg=response['error']).to_json()
    return ResponseDto(status=0, msg=response['msg'], result=response['data']).to_json()


@auth_blueprint.route('/logout/', methods=["GET"])
def logout():
    AuthService.logout()
    return ResponseDto(status=0, msg='Logout Successful').to_json()
