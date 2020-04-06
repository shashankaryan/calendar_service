import logging
from models.base import BaseDocument
from mongoengine import StringField, EmailField

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class User(BaseDocument):
    """ A User Model which will act as the User for defining slots and bokking slots."""
    email = EmailField(unique=True)
    name = StringField(max_length=100)
    password = StringField()

    def __repr__(self):
        return '<User: %r>' % str(self.email)

    def to_dict(self):
        return {"id": str(self.id), "email": self.email, "name": self.name}


class SessionUser:
    """ Creating Session for Logged in user """
    def __init__(self, email=None, name=None):
        self.id = email
        self.name = name
        self.email = email

    def get_id(self):
        return str(self.email)

    def get_email(self):
        return str(self.email)

    def __repr__(self):
        return '<User %r>' % self.email

    def check_email(self,email):
        return email == self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def to_dict(self):
        return {"id": self.id, "email": self.email, "name": self.name}
