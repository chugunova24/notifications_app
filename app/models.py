# Standard Library imports
from enum import Enum
import datetime as dt
from collections import OrderedDict

# Core Flask imports

# Third-party imports
import mongoengine as me
import bcrypt

# App imports
from config import Config
from app.utils.validators import username_validator, id_notification_validator


class Status(Enum):
    REGISTRATION = 'registration'
    NEW_MESSAGE = 'new_message'
    NEW_POST = 'new_post'
    NEW_LOGIN = 'new_login'

    def get_status_rules(self):
        rules = OrderedDict()
        rules['send_email'] = [self.REGISTRATION.value, self.NEW_LOGIN.value]
        rules['create_notify'] = [self.NEW_MESSAGE.value, self.NEW_POST.value, self.NEW_LOGIN.value]
        return rules

    def get_rules_key(self):
        status_rules = self.get_status_rules()
        return {rule: True if self.value in status_rules[rule] else False for rule in status_rules}


class Notifications(me.EmbeddedDocument):
    id = me.IntField(max_value=Config.MAX_SIZE_NOTIFICATIONS, validation=id_notification_validator)
    timestamp = me.IntField()
    is_new = me.BooleanField(default=True)
    user_id = me.ObjectIdField(primary_key=False)
    key = me.EnumField(Status)
    target_id = me.ObjectIdField(primary_key=False)
    data = me.DictField(default=None)

    def clean(self) -> None:
        if self.timestamp is None:
            self.timestamp = int(dt.datetime.today().timestamp())

    def __str__(self) -> str:
        return f"{self.id}|{self.user_id}|{self.timestamp}|{self.is_new}|{self.key}|{self.data}"


class User(me.Document):
    username = me.StringField(min_length=4, max_length=30, unique=True, required=True, validation=username_validator)
    password = me.StringField(required=True)
    email = me.EmailField(unique=True, required=True)
    notifications = me.EmbeddedDocumentListField('Notifications', required=False)
    meta = {'collection': 'users'}

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        password = document.password
        hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(14))
        document.password = hashed.decode('utf-8')

    def __str__(self) -> str:
        return f"{self.username}|{self.email}"



