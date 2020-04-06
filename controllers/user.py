from flask import Blueprint, request, current_app
from dto.result import ResponseDto
from utils import get_page_items

user_blueprint = Blueprint('user_blueprint', __name__)
