import logging
from datetime import datetime

from mongoengine import ReferenceField, DateTimeField

from models.base import BaseDocument
from models.user import User
from services.user import UserService

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Slot(BaseDocument):
    """ Slot which a user will define to show their availability.
    User: Reference to User who has defined the slot.
    Start & End Time: Timeline of the slot
    Booked by: Reference to User who has booked the slot
    """
    user = ReferenceField(User)
    start_ts = DateTimeField()
    end_ts = DateTimeField()
    booked_by = ReferenceField(User)

    def to_dict(self):
        return {"id": str(self.id), "user": self.user.to_dict(), 'bookedBy': self.booked_by.to_dict(),
                "startTimestamp": self.start_ts.timestamp(), "endTimestamp": self.end_ts.timestamp()}

    def update(self, slot_data):
        if "startTimestamp" in slot_data:
            self.start_ts = datetime.fromtimestamp(slot_data.get("startTimestamp"))
        if "endTimestamp" in slot_data:
            self.start_ts = datetime.fromtimestamp(slot_data.get("startTimestamp"))
        if "bookedBy" in slot_data:
            self.booked_by = UserService.get_users(emails=[slot_data.get('bookedBy')], data_objects=True,
                                                   paginate=False).first()
        self.save()
        return {'status': True, 'data': self.to_dict()}
