from bson import ObjectId
from flask import Blueprint, request, current_app
from flask_login import login_required

from dto.result import ResponseDto
from services.calendar import CalendarService
from services.user import UserService
from utils import get_page_items

calendar_blueprint = Blueprint('calendar_blueprint', __name__)


@calendar_blueprint.route('/slot/', methods=['GET'])
@login_required
def get_slot():
    page, per_page, offset = get_page_items()
    paginate = request.args.get('paginate', 'true').lower()
    paginate = False if paginate == 'false' else True
    slot_ids = request.args.get('slotIds', None)
    order_by = request.args.get('orderBy', '-created_at')
    if slot_ids:
        slot_ids = [slot_id for slot_id in slot_ids.split(',') if ObjectId.is_valid(slot_id)]
        slots = CalendarService.get_slots(slot_ids=slot_ids, paginate=False, order_by=order_by)
    else:
        start_ts = request.args.get('startTimestamp', None)
        end_ts = request.args.get('endTimestamp', None)
        user = request.args.get('userEmail', None)
        if user:
            user = UserService.get_users(emails=[user], data_objects=True, paginate=False).first()
            if user is None:
                return ResponseDto(status=-1, msg="User is not present with this email.").to_json()

        booked_by = request.args.get('bookedBy', None)
        if booked_by:
            booked_by = UserService.get_users(emails=[booked_by], data_objects=True, paginate=False).first()
            if booked_by is None:
                return ResponseDto(status=-1, msg="Booking user is not present with this email.").to_json()

        slots = CalendarService.get_slots(page=page, limit=per_page, user=user, booked_by=booked_by,
                                          end_ts=end_ts, order_by=order_by, start_ts=start_ts, paginate=paginate)

    if slots.get('data'):
        return ResponseDto(status=0, result=slots).to_json()
    return ResponseDto(status=-1, msg='No Slot Found.').to_json()


@calendar_blueprint.route('/slot/', methods=['POST'])
@login_required
def create_slot():
    slot_data = request.json.get('slotData')
    if not slot_data:
        return ResponseDto(status=-1, msg="Slot Data missing").to_json()

    necessary_fields = ["userEmail", "startTimestamp", "endTimestamp"]
    error, msg = False, ''
    for field in necessary_fields:
        if field not in slot_data:
            error = True
            msg = field + " not provided"
    if error:
        return ResponseDto(status=-1, msg=msg).to_json()
    validated = CalendarService.check_data_validations(slot_data)
    if not validated['value']:
        return ResponseDto(status=-1, msg=validated['error']).to_json()

    response = CalendarService.create_slot(slot_data)
    if response:
        return ResponseDto(status=0, msg='Create operation successful', result=response).to_json()
    return ResponseDto(status=-1, msg='Slot create operation failed').to_json()




@calendar_blueprint.route('/healthCheck', methods=['GET'])
def health_check():
    return ResponseDto(status=0, msg='All good').to_json(), 200
