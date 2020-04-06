from bson import ObjectId

from models.calendar import Slot
from datetime import datetime, timedelta

from mongoengine import Q
from mongoengine.queryset.visitor import QCombination

from services.user import UserService


class CalendarService:
    @staticmethod
    def get_slots(page=None, limit=None, slot_ids=[], paginate=True, user=None, booked_by=None,
                  end_ts=None, order_by='-created_by', start_ts=None, data_objects=False):
        """
        :param page: page number
        :param limit: no of results per page
        :param slot_ids: List of ad IDs
        :param user: User who defined the slot
        :param booked_by: User who booked the slot
        :param paginate: Boolean, to return paginated results if true
        :param data_objects: Boolean, to return queryset
        :param start_ts: start timestamp
        :param end_ts: end timestamp
        :param paginate: Boolean, to return paginated results if true
        :param data_objects: Boolean, to return queryset
        :param order_by: Sorting Key
        :return: Returns users filtered on the requirement in the specified format
        """
        if slot_ids:
            slots = Slot.objects.filter(id__in=slot_ids, deleted=False).order_by(order_by)
        else:
            match_case_query = [Q(deleted=False)]
            if user:
                match_case_query.append(Q(user=user))
            if end_ts and start_ts:
                match_case_query.append(Q(end_date__gt=datetime.fromtimestamp(int(start_ts)),
                                          start_date__lt=datetime.fromtimestamp(int(end_ts))))
            if booked_by:
                match_case_query.append(Q(booked_by=booked_by))
            match_query = QCombination(QCombination.AND, match_case_query)
            slots = Slot.objects.filter(match_query).order_by(order_by)

        if data_objects:
            return slots    # Returns QuerySet
        if not paginate:
            return {"data": [instance.to_dict() for instance in list(slots)]}
        else:
            slots = slots.paginate(page=page, per_page=limit)
            return {"data": [instance.to_dict() for instance in slots.items],
                    "current_page": slots.page,
                    "total_pages_for_query": slots.pages,
                    "item_per_page": slots.per_page,
                    "total_records": slots.total,
                    "next_num": slots.next_num,
                    "prev_num": slots.prev_num,
                    "has_next": slots.has_next,
                    "has_prev": slots.has_prev}

    @staticmethod
    def validate_slot_id_and_get_instance(slot_id):
        """ Validates slot id and returns instance, if present"""
        if not ObjectId.is_valid(slot_id):
            return {"err": 'Invalid Slot ID.'}
        slot = CalendarService.get_slots(slot_ids=[slot_id], paginate=False, data_objects=True).first()
        if not slot:
            return {"err": 'No Slot exists.'}
        return {"err": None, "instance": slot}

    @staticmethod
    def create_slot(slot_data):
        """Creates new slot using user, start time and end time."""
        user = UserService.get_users(emails=[slot_data.get('userEmail')], data_objects=True, paginate=False).first()
        slot = Slot(user=user, start_ts=datetime.fromtimestamp(slot_data.get('startTimestamp')),
                    end_ts=datetime.fromtimestamp(slot_data.get('endTimestamp'))).save()
        return {"data": slot.to_dict()}

    @staticmethod
    def validate_user(value):
        user = UserService.get_users(emails=[value], data_objects=True, paginate=False).first()
        if not user:
            return "User with this email not found"
        return None

    @staticmethod
    def validate_conflict_for_slot(start_date, end_date, user, exempted_slot_ids):
        """
        :param start_date: Epoch value, start_date for which the check has to be applied
        :param end_date: Epoch value, end date for which the check has to be applied
        :param user: User Instance
        :param exempted_slot_ids: list of ids, Slot not to consider, used in UPDATE case.
        :return:
        """
        existing_slots = Slot.objects.filter(user=user, deleted=False,
                                             start_date__lt=datetime.fromtimestamp(end_date),
                                             end_date__gt=datetime.fromtimestamp(start_date))
        if existing_slots and exempted_slot_ids:
            existing_slots = existing_slots.filter(id__not__in=exempted_slot_ids)
        if existing_slots:
            return False
        return True

    @staticmethod
    def validate_start_date(start):
        """
        :param start: Start time Epoch value, will be coming from the request
        """
        try:
            if not datetime.fromtimestamp(int(start)) <= datetime.now()+timedelta(minutes=15):
                return "Slot start time must be 15 minutes from current timestamp"
        except ValueError:
            return "Invalid Start Date"
        return None

    @staticmethod
    def validate_end_date(start, end):
        """
        :param start: Start time Epoch value, will be coming from the request
        :param end: End time Epoch value, will be coming from the request
        """
        try:
            if not datetime.fromtimestamp(int(start)) < datetime.fromtimestamp(int(end)):
                return "Slot start time must be less than end time"
            elif not datetime.now()+timedelta(minutes=60) == datetime.fromtimestamp(int(start)):
                return "Slot must be of 1 hour."
        except ValueError:
            return "Invalid End Date."
        return None

    @staticmethod
    def check_data_validations(data, exempted_slot=[]):
        """
        :param data: data object with create or update data, will be coming from request.
        :param exempted_slot: will be list of slot instances which is not required to be included
        :return:
        """
        master_error, user = [], None
        if exempted_slot:
            if exempted_slot[0].booked_by:
                master_error.append("Changes not allowed")
            else:
                user = exempted_slot[0].user

        if not master_error:
            for field in data:
                if field == "userEmail":
                    error = CalendarService.validate_user(data.get("userEmail"))
                    if error:
                        master_error.append(error)

                if field == "startTimestamp":
                    error = CalendarService.validate_start_date(data.get("startTimestamp"))
                    if error:
                        master_error.append(error)

                if field == "endTimestamp":
                    error = CalendarService.validate_end_date(data.get("startTimestamp"), data.get("endTimestamp"))
                    if error:
                        master_error.append(error)

                if field == "bookedBy":
                    error = CalendarService.validate_user(data.get("bookedBy"))
                    if error:
                        master_error.append(error)

        if not master_error and ("endTimestamp" in data or "startTimestamp"):
            user = exempted_slot[0].user if exempted_slot else UserService.get_users(
                emails=[data.get("userEmail")], data_objects=True, paginate=False).first()
            if not CalendarService.validate_conflict_for_slot(data.get("startTimestamp"), data.get("endTimestamp"),
                                                              user, [str(slot.id) for slot in exempted_slot]):
                master_error.append("Conflicting Slot Found.")

        if master_error:
            return {'value': False, 'error': '|'.join(master_error)}
        return {'value': True, 'error': None}

    @staticmethod
    def validate_remove_slot(slot):
        """Validate if a slot can be removed"""
        if not slot.booked_by:
            return {'value': False, 'error': 'Slot is booked'}
        return {'value': True, 'error': None}

    @staticmethod
    def remove_slot(slot):
        """Removes slot."""
        slot.deleted = True
        slot.save()
        return {"status": True}
