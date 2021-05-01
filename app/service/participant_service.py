from flask import jsonify
from flask_restful import abort

from datetime import datetime, timedelta

from app import db
from app.models.participant_model import Participant, ParticipantLog
from app.models.user_model import User

from ..serializer import ParticipantSchema, participants_schema, users_schema
from .room_service import edit_num_users

def get_all_participants():
    all_participants = Participant.query.all()
    all_participants = participants_schema.dump(all_participants)
    return all_participants

def get_participants_in(room_id):
    participants = Participant.query\
        .join(User, Participant.user_email==User.email)\
        .add_columns(Participant.room_id, User.name, User.email, User.phone, User.photo_url)\
        .filter(Participant.room_id==room_id)\
        .all()

    participants = users_schema.dump(participants)

    return participants

def save_new_participant(data):
    try:
        new_user = Participant(
            room_id=data['room_id'],
            user_email=data['user_email'],
            enter_time=datetime.utcnow() + timedelta(hours=9)
        )
        db.session.add(new_user)
        db.session.commit()
    
        edit_num_users(1, new_user.room_id) # db.session.commit 후에 실행
    except Exception as e:
            print(e)
            abort(500)

def delete_participant(data):
    try:
        user = Participant.query.filter_by(room_id=data['room_id'], user_email=data['user_email']).first()
        if user is None:
            msg = f"Delete Participant Fail. No User {data['user_email']}"
            print(msg)
            return False
        else:
            print("Delete: ", user)
            room_id = user.room_id
            edit_num_users(-1, user.room_id) # db.session.commit 전에 실행
            new_log = ParticipantLog(
                room_id=user.room_id,
                user_email=user.user_email,
                enter_time=user.enter_time,
                exit_time=datetime.utcnow() + timedelta(hours=9)
            )
            db.session.add(new_log)
            db.session.delete(user)
            db.session.commit()
            return room_id
    except Exception as e:
        print(e)
        abort(500)

def is_new_participant(data):
    try:
        user = Participant.query.filter_by(room_id=data['room_id'], user_email=data['user_email']).first()
        return True if not user else False
    except Exception as e:
            print(e)
            abort(500)

def count_participants(room_id):
    try:
        num_user = Participant.query.filter_by(room_id=room_id).count()
        return num_user
    except Exception as e:
        print(e)
        abort(500)