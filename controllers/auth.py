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


