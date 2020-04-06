from bson import ObjectId
from flask import Blueprint, request
from flask_login import login_required

from dto.result import ResponseDto
from services.auth import AuthService
from services.user import UserService
from utils import get_page_items

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/user/', methods=['GET'])
@login_required
def get_user():
    page, per_page, offset = get_page_items()
    paginate = request.args.get('paginate', 'true').lower()
    paginate = False if paginate == 'false' else True
    user_ids = request.args.get('userIds', None)
    if user_ids:
        user_ids = [user_id for user_id in user_ids.split(',') if ObjectId.is_valid(user_id)]
        users = UserService.get_users(user_ids=user_ids, paginate=False)
    else:
        q = request.args.get('q', '')
        emails = [email for email in request.args.get('emails', '').split(',') if AuthService.validate_email(email)]
        users = UserService.get_users(query=q, page=page, limit=per_page, emails=emails, paginate=paginate)

    if users.get('data'):
        return ResponseDto(status=0, result=users).to_json()
    return ResponseDto(status=-1, msg='No User Found.').to_json()
