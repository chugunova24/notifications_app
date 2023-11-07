# Standard Library imports

# Core Flask imports

# Third-party imports
from marshmallow import Schema, fields, validate
from marshmallow.validate import Range

# App imports
from app.models import Status
from app.utils.validators import validate_objectid, username_validator, password_validator


STATUS = [elem.value for elem in Status]


class UserSchema(Schema):
    username = fields.Str(validate=username_validator)
    password = fields.Str(validate=password_validator)
    email = fields.Email()


class BaseSchema(Schema):
    user_id = fields.Str(required=True, validate=validate_objectid)


class CreateNotifySchema(BaseSchema):
    target_id = fields.Str(validate=validate_objectid)
    key = fields.Str(required=True, validate=validate.OneOf(STATUS))
    data = fields.Dict()
    email = fields.Email()


class ReadNotifySchema(BaseSchema):
    notification_id = fields.Int(required=True, strict=False, validate=Range(min=1, error="id starts from 1."))


class ListNotifySchema(BaseSchema):
    skip = fields.Int(validate=Range(min=0, error="the skip must be greater than zero."))
    limit = fields.Int(required=True, validate=Range(min=0, error="the limit must be greater than zero."))