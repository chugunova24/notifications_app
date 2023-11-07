# Standard Library imports
from bson import ObjectId

# Core Flask imports
from flask import (request, jsonify)
from flask_restful import Resource

# Third-party imports
from mongoengine import ValidationError, Q

# App imports
from app.models import User
from app.serializers import UserSchema


class UserView(Resource):
    def post(self):
        """
        :param:
            username: username for public use. str, required and unique.
            password: user's password. str, required.
            email: user's email. str, required and unique.
        :return:
            success: success message.
            user: info about created User object.
        """
        question = request.form

        # validating data from request
        try:
            question = UserSchema().load(data=question)
        except Exception as err:
            return jsonify(success=False, errors=err.args[0])

        username = question['username']
        password = question['password']
        email = question['email']

        # check exist user
        obj = User.objects(Q(username=username) | Q(email=email)).first()

        if bool(obj) is True:
            if obj.username == username:
                return jsonify(success=False, errors={"username": "This username already exists."})
            if obj.username == email:
                return jsonify(success=False, errors={"email": "A user with this email already exists."})

        # create new user
        new_user = User(username=username, password=password, email=email)

        try:
            new_user.validate()
        except ValidationError as ve:
            return jsonify(success=False, errors=ve.to_dict())

        obj = new_user.save(sender=new_user)

        return jsonify(success=True, user={"id": str(obj.id),
                                           "username": obj.username,
                                           "email": obj.email,
                                           })
