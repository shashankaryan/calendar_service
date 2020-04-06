from flask import Blueprint, request, current_app
from dto.result import ResponseDto
from utils import get_page_items

calendar_blueprint = Blueprint('calendar_blueprint', __name__)


@calendar_blueprint.route('/', methods=['GET'])
def welcome():
    return ResponseDto(status=0, msg='Welcome to calendar Service.').to_json(), 200


@calendar_blueprint.route('/healthCheck', methods=['GET'])
def health_check():
    return ResponseDto(status=0, msg='All good').to_json(), 200
