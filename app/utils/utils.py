# Standard Library imports
import random
from bson import ObjectId

# Core Flask imports
from flask.json import JSONEncoder

# Third-party imports

# App imports
from app.models import User


class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            print(str(o))
            return str(o)
        else:
            return super().default(self, o)


def create_test_user(objectid: ObjectId, email: str) -> User:
    username = "test" + str(random.randint(10, 9999))  # for testing
    password = "A123sew!sw"
    new_test_user = User(id=objectid, username=username, password=password, email=email)

    return new_test_user

