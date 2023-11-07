# Standard Library imports
from bson.objectid import ObjectId
from collections import Counter

# Core Flask imports
from flask import (request, jsonify, Blueprint)

# Third-party imports
from mongoengine import ValidationError, Q

# App imports
from app.models import User, Notifications, Status
from app.serializers import ReadNotifySchema, ListNotifySchema, CreateNotifySchema, UserSchema
from app.tasks import send_email
from app.utils.utils import create_test_user
from config import environs

notifications_bp = Blueprint('notifications', __name__)
MAIL_USERNAME = environs.get('MAIL_USERNAME')
FLASK_TEST_NOTIFICATIONS = bool(int(environs.get('FLASK_TEST_NOTIFICATIONS')))


@notifications_bp.route('/create', methods=['POST'])
def create_notify():
    """
    Creates a notification in the user's document.
    If user does not exist and FLASK_TEST_NOTIFICATIONS=True,
    then creates a user if email is specified.
    :param:
        user_id: ObjectId from bson as a string.
        key: notification type. Must have one of the values ["registration", "new_message",
            "new_post", "new_login"].
        email: not required. Needed to implicitly register a test user in test mode. Works only
            if FLASK_TEST_NOTIFICATIONS=1.
    :return:
        success: success message
    """

    question = request.json

    # validating data from request
    try:
        question = CreateNotifySchema().load(data=question)
    except Exception as err:
        return jsonify(success=False, errors=err.args[0])

    user_id = ObjectId(question['user_id'])
    email = question.get('email', None)

    # get user, check exist
    user = User.objects(Q(id=user_id) | Q(email=email)).first()

    if bool(user) is False:
        if FLASK_TEST_NOTIFICATIONS:
            if email:
                user = create_test_user(objectid=user_id, email=email)
            else:
                return jsonify(success=False, errors={"email": f"user_id {str(user_id)} does not exist. Enter email to create a test user."})
        else:
            return jsonify(success=False, errors={"user_id": f"user_id {str(user_id)} does not exist."})

    if email:
        question.pop('email')

    # get rules of status
    key = question['key']
    status = Status(value=key)
    rules_key = status.get_rules_key()

    # define behavior: creating a notification, sending an email
    if rules_key['create_notify']:
        question['user_id'] = user_id
        new_notify = Notifications(**question)

        last_id = len(user.notifications)
        new_notify.id = last_id + 1 if bool(last_id) else 1

        try:
            new_notify.validate()
        except ValidationError as ve:
            return jsonify(success=False, errors=ve.to_dict())

        # obj = User.objects(id=obj.id).update(push__notifications=new_notify)
        user.notifications.append(new_notify)
        user.save()

    if rules_key['send_email']:
        email_msg = key
        send_email.delay(subject=email_msg, sender=MAIL_USERNAME, recipients=[user.email])

    return jsonify(success=True)


@notifications_bp.route('/list', methods=['GET'])
def list_notify():
    """
    Displays user's notifications list, number of notifications,
    number of new notifications and request details.
    :param:
        user_id: ObjectId from bson as a string
        skip: number of messages to skip
        limit: maximum number of messages to show
    :return:
        success: success message
        answer: info about user's notifications
    """

    question = None
    answer = dict()

    # validating data from request
    try:
        question = ListNotifySchema().load(data=request.args.to_dict())
    except Exception as err:
        return jsonify(success=False, errors=err.args[0])

    user_id = ObjectId(question['user_id'])
    skip = question['skip']
    limit = question['limit']

    # get data about notifications
    q_set = User.objects(id=user_id).first()

    if q_set is None:
        return jsonify(success=False, errors={'user_id': f'{user_id} does not exist.'})

    q_set = q_set.to_mongo().to_dict()['notifications']
    q_set = q_set[skip: skip + limit]

    count_new = Counter(elem['is_new'] for elem in q_set)

    answer['data'] = dict()
    answer['data']['elements'] = len(q_set)
    answer['data']['new'] = count_new[True]
    answer['data']['request'] = question
    answer['data']['list'] = q_set

    return jsonify(success=True, **answer)


@notifications_bp.route('/read', methods=['POST'])
def read_notify():
    """
    Changes the "is_new" property in the notification to "True".
    :param:
        user_id: ObjectId from bson as a string.
        notification_id: an integer value that starts at 1.
    :return:
        success: success message
    """

    question = None

    # validating data from request
    try:
        question = ReadNotifySchema().load(data=request.form)
    except Exception as err:
        return jsonify(success=False, errors=err.args[0])

    user_id = ObjectId(question['user_id'])
    notification_id = question['notification_id']

    # get data about notifications
    user = User.objects(id=user_id).first()

    if bool(user) is False:
        return jsonify(success=False, errors={'user_id': f'{user_id} does not exist.'})
    try:
        notification = user.notifications[notification_id - 1]
    except IndexError:
        return jsonify(success=False, errors={'notification_id': f'{notification_id} does not exist.'})

    # update notification
    updated = User.objects(id=user_id, notifications__id=notification_id).update(set__notifications__S__is_new=False)

    return jsonify(success=True)




