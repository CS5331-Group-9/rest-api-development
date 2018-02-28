#!/usr/bin/python

import json
import os
import uuid
import bcrypt
from flask_cors import CORS
from flask import Flask, jsonify
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import exc
from sqlalchemy.sql import func
from marshmallow import Schema, fields, pre_load, validate
import datetime
import dateutil.parser
import pytz
import cgi


app = Flask(__name__)
# Enable cross origin sharing for all endpoints
CORS(app)

#init app config
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    fullname = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    token = db.Column(db.String(36), unique=False, nullable=True)

    def __init__(self, username, password, fullname, age):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.age = age

    def as_dict(self):
        return {c.name: unicode(getattr(self, c.name)) for c in self.__table__.columns}

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    @staticmethod
    def generate_auth_token():
        return str(uuid.uuid4())


class UserSchema(ma.Schema):
    id = fields.Integer()
    username = fields.String(required=True, validate=[
        validate.Length(min=4, max=30, error="User name must have between {min} and {max} characters."),
        validate.Regexp(r"[a-zA-Z0-9_\-]*$",
                        error="User name must not contain special characters"
                              "(except _ und -)")
    ])
    password = fields.String(required=True, validate=[
        validate.Length(min=6, max=30, error="Password must have between {min} and {max} characters.")
    ])
    fullname = fields.String(required=True, validate=[
        validate.Length(min=1, error="Fullname cannot be empty")
    ])
    age = fields.Integer(required=True, validate=lambda n: n > 0, error_messages={
        "validator_failed": "Age must be a valid integer.",
        "null": "Age must be a valid integer.",
        "required": "Age must be a valid integer.",
        "type": "Age must be a valid integer.",
        "invalid": "Age must be a valid integer."
    })

    class Meta:
        # Fields to expose
        fields = ('id', 'username', 'fullname', 'age', 'password')


class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publish_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, title, author, public, text, publish_date):
        self.user_id = user_id
        self.title = title
        self.author = author
        self.public = public
        self.text = text
        self.publish_date = publish_date

    def as_dict(self):
        return {c.name: unicode(getattr(self, c.name)) for c in self.__table__.columns}


class DiarySchema(ma.Schema):
    id = fields.Integer()
    title = fields.String(required=True, validate=[
        validate.Length(min=1, max=255, error="Title must have between {min} and {max} characters.")
    ])
    author = fields.String(required=True, validate=[
        validate.Length(min=1, max=255, error="Author must have between {min} and {max} characters.")
    ])
    public = fields.Boolean(required=True)
    text = fields.String(required=True, validate=[
        validate.Length(min=1, error="Text cannot be empty")
    ])

    class Meta:
        # Fields to expose
        fields = ('id', 'title', 'author', 'publish_date', 'public', 'text')


class InsertDiarySchema(ma.Schema):
    title = fields.String(required=True, validate=[
        validate.Length(min=1, max=255, error="Title must have between {min} and {max} characters.")
    ])
    public = fields.Boolean(required=True)
    text = fields.String(required=True, validate=[
        validate.Length(min=1, error="Text cannot be empty")
    ])
    token = fields.String(required=True, validate=[
        validate.Length(min=36, error="Text cannot be empty")
    ])

    class Meta:
        # Fields to expose
        fields = ('id', 'title', 'author', 'publish_date', 'public', 'text', 'token')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
diary_schema = DiarySchema()
diaries_schema = DiarySchema(many=True)
insert_diary_schema = InsertDiarySchema()


# Endpoints of APIs
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members', '/users/register',
                 '/users/authenticate', '/users/expire', '/users', '/diary',
                 '/diary/create', '/diary/delete', '/diary/permission']


# endpoint to create new user
@app.route("/users/register", methods=["POST"])
def add_user():
    if not request.is_json:
        return make_json_response("Invalid request", False)

    # Validate and deserialize input
    data, errors = user_schema.load(request.json)
    if errors:
        return make_json_response(errors, False)

    password_hash = bcrypt.hashpw(data['password'].encode("utf-8"), bcrypt.gensalt())
    new_user = User(data['username'], password_hash, data['fullname'], data['age'])

    db.session.add(new_user)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as err:
        db.session.rollback()
        if "UNIQUE constraint failed: user.username" in str(err):
            return make_json_response("User already exists!", False, 200)
        else:
            return make_json_response("unknown error adding user", False, 200)

    return make_json_response(None, True, 201)


# endpoint to show all users
@app.route("/users", methods=["POST"])
def get_user():
    if not request.is_json:
        return make_json_response("Invalid request", False)

    if 'token' not in request.json.keys():
        return make_json_response("Invalid authentication token.", False)

    token_string = request.json['token']
    user = User.query.filter_by(token=token_string).first()

    if user is None:
        return make_json_response("Invalid authentication token.", False)

    user_info = {"username": user.username, "fullname": user.fullname, "age": user.age}
    return make_json_response(user_info)


# endpoint to authenticate user
@app.route("/users/authenticate", methods=["POST"])
def user_authenticate():
    if not request.is_json:
        return make_json_response("Invalid request", False)

    if 'username' not in request.json.keys() and 'password' not in request.json.keys():
        return make_json_response(None, False)
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if not user or not user.verify_password(password):
        return make_json_response(None, False)

    token_string = user.generate_auth_token()
    user.token = token_string
    db.session.commit()

    return make_json_response({"token": token_string})


# endpoint to expire user token
@app.route("/users/expire", methods=["POST"])
def user_expire():
    if not request.is_json:
        return make_json_response("Invalid request", False)

    if 'token' not in request.json.keys():
        return make_json_response(None, False)

    token_string = request.json['token']

    user = User.query.filter_by(token=token_string).first()

    if not user:
        return make_json_response(None, False)

    token_string = user.generate_auth_token()
    user.token = token_string
    db.session.commit()

    return make_json_response(None, True)


# endpoint to show all users
@app.route("/users/validate", methods=["POST"])
def validate_user():
    if not request.is_json:
        return make_json_response("Invalid request", False)

    if 'token' not in request.json.keys():
        return make_json_response("Invalid authentication token.", False)

    token_string = request.json['token']
    user = User.query.filter_by(token=token_string).first()

    if user is None:
        return make_json_response("Invalid authentication token.", False)

    user_info = {"username": user.username, "fullname": user.fullname, "age": user.age}
    return make_json_response(user_info, True, 200, None, True)


# endpoint to show all diaries
@app.route("/diary", methods=["GET"])
def get_all_diary():
    all_diaries = Diary.query.filter_by(public=True).all()

    records = []
    for diary in all_diaries:
        diary.publish_date = pytz.utc.localize(diary.publish_date)
        diary.publish_date = diary.publish_date.replace(microsecond=0).isoformat()
        diary.publish_date = str(diary.publish_date)
        records.append(diary)

    result = diaries_schema.dump(records)
    return make_json_response(result.data)


# endpoint to delete user
@app.route("/diary", methods=["POST"])
def get_user_diary():
    if not request.is_json:
        return make_json_response("Invalid request", False)

    if 'token' not in request.json.keys():
        return make_json_response("Invalid authentication token.", False)

    user = User.query.filter_by(token=request.json['token']).first()

    if user is None:
        return make_json_response("Invalid authentication token.", False)

    diaries = Diary.query.filter_by(user_id=user.id).all()
    records = []
    for diary in diaries:
        diary.publish_date = pytz.utc.localize(diary.publish_date)
        diary.publish_date = diary.publish_date.replace(microsecond=0).isoformat()
        diary.publish_date = str(diary.publish_date)
        records.append(diary)

    result = diaries_schema.dump(records)

    return make_json_response(result.data, True)


def getDateTimeFromISO8601String(s):
    d = dateutil.parser.parse(s)
    return d


def html_encode_input(input):
    new_input = {}
    for key in input:
        new_input[key] = input[key] if input[key] is True or input[key] is False or isinstance(input[key], (int, long)) else cgi.escape(input[key])

    return new_input


# endpoint to create diary
@app.route("/diary/create", methods=["POST"])
def add_diary():
    if not request.is_json:
        return make_json_response("Invalid request", False)

    # Validate and deserialize input
    data, errors = insert_diary_schema.load(request.json)
    if errors:
        return make_json_response(errors, False)

    user = User.query.filter_by(token=data['token']).first()

    if user is None:
        return make_json_response("Invalid authentication token.", False)

    author = user.fullname
    user_id = user.id
    publish_date = datetime.datetime.now().replace(microsecond=0).isoformat()
    publish_date = getDateTimeFromISO8601String(publish_date)

    new_diary = Diary(user_id, data['title'], author, data['public'], data['text'], publish_date)

    db.session.add(new_diary)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as err:
        db.session.rollback()
        return make_json_response(err, False, 200)

    return make_json_response({"id": new_diary.id}, True, 201)


# endpoint to delete diary
@app.route("/diary/delete", methods=["POST"])
def delete_diary():
    if not request.is_json:
        return make_json_response("Invalid request", False)

    if 'token' not in request.json.keys():
        return make_json_response("Invalid authentication token.", False)

    if 'id' not in request.json.keys():
        return make_json_response("Missing parameters.", False)

    user = User.query.filter_by(token=request.json['token']).first()

    if user is None:
        return make_json_response("Invalid authentication token.", False)

    diary = Diary.query.filter_by(user_id=user.id, id=request.json['id']).first()

    if diary is None:
        return make_json_response("Invalid diary ID or authentication token.", False)

    db.session.delete(diary)
    db.session.commit()

    return make_json_response(None, True)


# endpoint to adjust diary permission
@app.route("/diary/permission", methods=["POST"])
def update_diary_permission():
    if not request.is_json:
        return make_json_response("Invalid request", False)

    if 'token' not in request.json.keys():
        return make_json_response("Invalid authentication token.", False)

    if 'id' not in request.json.keys() or 'public' not in request.json.keys():
        return make_json_response("Missing parameters.", False)

    user = User.query.filter_by(token=request.json['token']).first()

    if user is None:
        return make_json_response("Invalid authentication token.", False)

    permission = True if request.json['public'] == 'true' or request.json['public'] is True else False

    diary = Diary.query.filter_by(user_id=user.id, id=request.json['id']).first()

    if diary is None:
        return make_json_response("Invalid diary ID or authentication token.", False)

    diary.public = permission
    db.session.commit()

    return make_json_response(None)


def make_json_response(data, status=True, code=200, key=None, raw=False):
    """Utility function to create the JSON responses."""

    to_serialize = {}
    if status:
        if data is not None:
            if raw:
                to_serialize = data
            else:
                if key is not None:
                    to_serialize[key] = data
                else:
                    to_serialize['result'] = data
        to_serialize['status'] = True
    else:
        if data is not None:
            if raw:
                to_serialize = data
            else:
                if key is not None:
                    to_serialize[key] = data
                else:
                    to_serialize['error'] = data
        to_serialize['status'] = False
    response = app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response


@app.route("/")
def index():
    """Returns a list of implemented endpoints."""
    return make_json_response(ENDPOINT_LIST)


@app.route("/meta/heartbeat")
def meta_heartbeat():
    """Returns true"""
    return make_json_response(None)


@app.route("/meta/members")
def meta_members():
    """Returns a list of team members"""
    with open("./team_members.txt") as f:
        team_members = f.read().strip().split("\n")
    return make_json_response(team_members)


if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Run the application
    app.run(debug=True, port=8080, host="0.0.0.0")
