from flask_mongoengine import MongoEngine
import datetime
import enum

db = MongoEngine()


class BaseDocument(db.Document):
    """A base document defining certain critical fields
    :param datetime created_at: The timestamp when the document was created
    :param datetime updated_at: The timestamp when the document was last updated
    """

    meta = {'abstract': True, 'strict': False}

    deleted = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        """Triggered when the document is saved, updates the fields"""
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(BaseDocument, self).save(*args, **kwargs)


class BaseEnum(enum.Enum):
    """Base class for all enum classes"""
    @classmethod
    def get_values(cls):
        """Method to get values of enum values"""
        values = []
        for key in cls:
            values.append(key.value)
        return values
