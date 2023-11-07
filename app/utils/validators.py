import re

from bson import ObjectId

from config import Config

from mongoengine import ValidationError as meValidationError
from marshmallow import ValidationError as maValidationError


pattern_username = re.compile(r"^[a-z0-9]+$", re.I)
pattern_password = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{6,20}$")


# mongoengine validators
def username_validator(username):
    if bool(pattern_username.match(username)) is False:
        raise meValidationError \
            ("The username can only contain letters or numbers (letters A to Z, numbers 0 to 9), and underscores.")


def id_notification_validator(value):
    if value > Config.MAX_SIZE_NOTIFICATIONS:
        raise meValidationError(f"The number of notifications exceeds {Config.MAX_SIZE_NOTIFICATIONS}")


# marshmallow validators
def validate_objectid(value):
    if len(value) != 24:
        raise maValidationError("id must be 24 hex characters.")
    try:
        ObjectId(value)
    # except bson.errors.InvalidId as err_id:
    except Exception as err_id:
        raise maValidationError(str(err_id))


def password_validator(password):
    if bool(pattern_password.fullmatch(password)) is False:
        raise maValidationError \
            ("The password must contain from 6 to 20 characters, it can use numbers, symbols and letters of the Latin "
             "alphabet. In this case, the password must contain at least one number, one lowercase letter and one "
             "uppercase letter.")

