from flask import jsonify
from flask_restful import abort

from datetime import datetime, timedelta

from app import db
from app.models.room_model import Room, RoomOG, RoomLog
from app.models.participant_model import Participant

from ..serializer import room_schema, rooms_schema, participants_schema, room_logs_schema

def get_all_rooms():
    all_rooms = Room.query.filter((Room.status=="모집중") | (Room.status=="신고접수"))\
        .order_by(Room.create_time.desc()).all()
    all_rooms = rooms_schema.dump(all_rooms)
    return all_rooms

def get_a_room(room_id):
    room = Room.query.filter_by(rid=room_id).first()
    room = room_schema.dump(room)
    return room

def save_new_room(data):
    try:
        new_room = Room(
            category=data['category'],
            title=data['title'],
            place=data['place'],
            status="모집중",
            num_user=0,
            creator_name=data['creator_name'],
            creator_email=data['creator_email'],
            order_date = data['order_date'],
            order_time = data['order_time'],
            stuff_link=data['stuff_link'],
            create_time=datetime.utcnow() + timedelta(hours=9)
        )
        db.session.add(new_room)
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)
    return new_room

def edit_room_info(data):
    try:
        room = Room.query.filter_by(rid=data['room_id']).first()
        room.title = data['title']
        room.place = data['place']
        room.order_date = data['date']
        room.order_time = data['time']
        room.stuff_link = data['link']
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)
    return room
    
def save_og_data(data):
    try:
        og_info = RoomOG(
            room_id=data['room_id'],
            image_url=data['image_url'],
            og_title=data['og_title'],
        )
        db.session.add(og_info)
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)
    return og_info

def get_my_room_list(user_email):
    print(user_email)
    room = Room.query\
        .join(Participant, Room.rid==Participant.room_id)\
        .add_columns(Room.rid, Room.category, Room.title, Room.place, Room.num_user,\
            Room.order_date, Room.order_time, Room.stuff_link, Room.creator_email)\
        .filter(Participant.user_email == user_email)\
        .order_by(Room.create_time.desc())\
    
    room = rooms_schema.dump(room)
    
    return room

def edit_num_users(diff, room_id):
    try:
        room = Room.query.filter_by(rid=room_id).first()
        room.num_user = room.num_user + diff
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)

def delete_a_room(data):
    try:
        print("DEBUG01:",data['room_id'])
        copy_room = Room.query.filter_by(rid=data['room_id']).first()
        if copy_room is None:
            msg = f"Delete Room Fail. No User {data['user_email']}"
            print(msg)
            return msg
        else:
            print("DEBUG02:",copy_room)
            new_log = RoomLog(
                rid=copy_room.rid,
                status=copy_room.status,
                category=copy_room.category,
                title=copy_room.title,
                place=copy_room.place,
                num_user=copy_room.num_user,
                creator_name=copy_room.creator_name,
                creator_email=copy_room.creator_email,
                order_date = copy_room.order_date,
                order_time = copy_room.order_time,
                stuff_link=copy_room.stuff_link,
                create_time=copy_room.create_time,
                update_time=copy_room.update_time,
                deleted_time=datetime.utcnow() + timedelta(hours=9)
            )
            db.session.add(new_log)
            db.session.delete(copy_room)
            db.session.commit()

    except Exception as e:
        print(e)
        abort(500)

def get_all_room_logs():
    all_room_logs = RoomLog.query.order_by(RoomLog.create_time.desc()).all()
    all_room_logs = room_logs_schema.dump(all_room_logs)
    return all_room_logs

def get_my_room_logs(email):
    print(email)
    my_room_logs = RoomLog.query\
        .join(Participant, RoomLog.rid==Participant.room_id)\
        .add_columns(RoomLog.rid, RoomLog.category, RoomLog.title, RoomLog.place, RoomLog.num_user,\
            RoomLog.order_date, RoomLog.order_time, RoomLog.stuff_link)\
        .filter(Participant.user_email == email)\
        .order_by(RoomLog.create_time.desc())\
    
    my_room_logs = room_logs_schema.dump(my_room_logs)
    return my_room_logs

def get_a_room_status(room_id):
    status = Room.query.filter_by(rid=room_id).with_entities(Room.status).first() # status만 select
    print(room_id, ":", status)
    return status

def room_change_auto(room_id):
    try:
        room = Room.query.filter_by(rid=room_id).first()
        if room.status == "생성중":
            change_the_room_status(room_id, "모집중")
        elif room.status == "모집중":
            change_the_room_status(room_id, "구매중")
        elif room.status == "구매중":
            change_the_room_status(room_id, "모집중")
    except Exception as e:
        print(e)
        abort(500)

def change_the_room_status(room_id, status):
    try:
        room = Room.query.filter_by(rid=room_id).first()
        room.status = status
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)

def delete_all_making_room():
    try:
        making_rooms = Room.query.filter_by(status="생성중").delete()
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)