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

