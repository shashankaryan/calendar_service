from flask import Blueprint, request, current_app
from dto.result import ResponseDto
from utils import get_page_items

auth_blueprint = Blueprint('auth_blueprint', __name__)
