from flask import jsonify
from flask_restful import abort

from datetime import datetime, timedelta

from app import db
from app.models.chat_model import Chat, ChatOG, ChatLog
from app.models.participant_model import Participant

from ..serializer import chat_schema, chats_schema, participants_schema, chat_logs_schema

def get_all_chats():
    all_chats = Chat.query.filter((Chat.status=="모집중") | (Chat.status=="신고접수"))\
        .order_by(Chat.create_time.desc()).all()
    all_chats = chats_schema.dump(all_chats)
    return all_chats

def get_a_chat(chat_id):
    chat = Chat.query.filter_by(rid=chat_id).first()
    chat = chat_schema.dump(chat)
    return chat

def save_new_chat(data):
    try:
        new_chat = Chat(
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
        db.session.add(new_chat)
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)
    return new_chat

def edit_chat_info(data):
    try:
        chat = Chat.query.filter_by(rid=data['chat_id']).first()
        chat.title = data['title']
        chat.place = data['place']
        chat.order_date = data['date']
        chat.order_time = data['time']
        chat.stuff_link = data['link']
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)
    return chat
    
def save_og_data(data):
    try:
        og_info = ChatOG(
            chat_id=data['chat_id'],
            image_url=data['image_url'],
            og_title=data['og_title'],
        )
        db.session.add(og_info)
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)
    return og_info

def get_my_chat_list(user_email):
    print(user_email)
    chat = Chat.query\
        .join(Participant, Chat.rid==Participant.chat_id)\
        .add_columns(chat.rid, chat.category, chat.title, chat.place, chat.num_user,\
            chat.order_date, chat.order_time, chat.stuff_link, chat.creator_email)\
        .filter(Participant.user_email == user_email)\
        .order_by(chat.create_time.desc())\
    
    chat = chats_schema.dump(chat)
    
    return chat

def edit_num_users(diff, chat_id):
    try:
        chat = Chat.query.filter_by(rid=chat_id).first()
        chat.num_user = chat.num_user + diff
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)

def delete_a_chat(data):
    try:
        print("DEBUG01:",data['chat_id'])
        copy_chat = Chat.query.filter_by(rid=data['chat_id']).first()
        if copy_chat is None:
            msg = f"Delete chat Fail. No User {data['user_email']}"
            print(msg)
            return msg
        else:
            print("DEBUG02:",copy_chat)
            new_log =ChatLog(
                rid=copy_chat.rid,
                status=copy_chat.status,
                category=copy_chat.category,
                title=copy_chat.title,
                place=copy_chat.place,
                num_user=copy_chat.num_user,
                creator_name=copy_chat.creator_name,
                creator_email=copy_chat.creator_email,
                order_date = copy_chat.order_date,
                order_time = copy_chat.order_time,
                stuff_link=copy_chat.stuff_link,
                create_time=copy_chat.create_time,
                update_time=copy_chat.update_time,
                deleted_time=datetime.utcnow() + timedelta(hours=9)
            )
            db.session.add(new_log)
            db.session.delete(copy_chat)
            db.session.commit()

    except Exception as e:
        print(e)
        abort(500)

def get_all_chat_logs():
    all_chat_logs = ChatLog.query.order_by(ChatLog.create_time.desc()).all()
    all_chat_logs = chat_logs_schema.dump(all_chat_logs)
    return all_chat_logs

def get_my_chat_logs(email):
    print(email)
    my_chat_logs = ChatLog.query\
        .join(Participant, ChatLog.rid==Participant.chat_id)\
        .add_columns(ChatLog.rid, ChatLog.category, ChatLog.title, ChatLog.place, ChatLog.num_user,\
            ChatLog.order_date, ChatLog.order_time, ChatLog.stuff_link)\
        .filter(Participant.user_email == email)\
        .order_by(ChatLog.create_time.desc())\
    
    my_chat_logs = chat_logs_schema.dump(my_chat_logs)
    return my_chat_logs

def get_a_chat_status(chat_id):
    status = Chat.query.filter_by(rid=chat_id).with_entities(Chat.status).first() # status만 select
    print(chat_id, ":", status)
    return status

def chat_change_auto(chat_id):
    try:
        chat = Chat.query.filter_by(rid=chat_id).first()
        if chat.status == "생성중":
            change_the_chat_status(chat_id, "모집중")
        elif chat.status == "모집중":
            change_the_chat_status(chat_id, "구매중")
        elif Chat.status == "구매중":
            change_the_chat_status(chat_id, "모집중")
    except Exception as e:
        print(e)
        abort(500)

def change_the_chat_status(chat_id, status):
    try:
        chat = Chat.query.filter_by(rid=chat_id).first()
        chat.status = status
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)

def delete_all_making_chat():
    try:
        making_chats = Chat.query.filter_by(status="생성중").delete()
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)