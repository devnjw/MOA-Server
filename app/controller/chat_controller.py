from flask import request, jsonify
from flask_restful import Resource, abort

from ..service.chat_service import get_all_chats, get_a_chat, save_new_chat, get_my_chat_list,\
    save_og_data, delete_a_chat, get_all_chat_logs, get_a_chat_status, change_the_chat_status,\
    get_my_chat_logs, delete_all_making_chat, chat_change_auto, edit_chat_info
from ..service.participant_service import is_new_participant, save_new_participant

class ChatList(Resource):
    def get(self):
        output = get_all_chats()
        return jsonify({'data': output})

    def post(self):
        data = request.get_json()
        chat_id = save_new_chat(data).rid

        data['user_email'] = data['creator_email']
        data['chat_id'] = chat_id
        
        save_new_participant(data)

        return jsonify({'chat_id': chat_id})

    def put(self):
        data = request.get_json()
        chat_id = edit_chat_info(data).rid
        return jsonify({'result':'Change Succes'})

    def delete(self):
        data = request.get_json()
        delete_a_chat(data)
        return jsonify({'result':'Delete Success'})

class Chat(Resource):
    ''' 방 정보 반환 + 새로운 참여자일 경우 저장'''
    def get(self, chat_id):
        chat = get_a_chat(chat_id)
        return chat

class ChatStatus(Resource):
    def get(self, chat_id):
        status = get_a_chat_status(chat_id)
        return jsonify({'status':status})

    def put(self, chat_id):
        # data = request.get_json()
        chat_change_auto(chat_id)
        return jsonify({'result':'Change Success'})

    def delete(self, chat_id):
        delete_all_making_chat()
        return jsonify({'result':'Delete All Making chat Success'})

class ChatOG(Resource):
    def post(self):
        data = request.get_json()
        save_og_data(data)

class MyChatList(Resource):
    def get(self, email):
        chat = get_my_chat_list(email)
        return jsonify({'data': chat})

class ChatLog(Resource):
    def get(self):
        output = get_all_chat_logs()
        return jsonify({'data': output})

class MyChatLog(Resource):
    def get(self, email):
        output = get_my_chat_logs(email)
        return jsonify({'data': output})