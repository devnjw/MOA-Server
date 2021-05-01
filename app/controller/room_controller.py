from flask import request, jsonify
from flask_restful import Resource, abort

from ..service.room_service import get_all_rooms, get_a_room, save_new_room, get_my_room_list,\
    save_og_data, delete_a_room, get_all_room_logs, get_a_room_status, change_the_room_status,\
    get_my_room_logs, delete_all_making_room, room_change_auto, edit_room_info
from ..service.participant_service import is_new_participant, save_new_participant

class RoomList(Resource):
    def get(self):
        output = get_all_rooms()
        return jsonify({'data': output})

    def post(self):
        data = request.get_json()
        room_id = save_new_room(data).rid

        data['user_email'] = data['creator_email']
        data['room_id'] = room_id
        
        save_new_participant(data)

        return jsonify({'room_id': room_id})

    def put(self):
        data = request.get_json()
        room_id = edit_room_info(data).rid
        return jsonify({'result':'Change Succes'})

    def delete(self):
        data = request.get_json()
        delete_a_room(data)
        return jsonify({'result':'Delete Success'})

class Room(Resource):
    ''' 방 정보 반환 + 새로운 참여자일 경우 저장'''
    def get(self, room_id):
        room = get_a_room(room_id)
        return room

class RoomStatus(Resource):
    def get(self, room_id):
        status = get_a_room_status(room_id)
        return jsonify({'status':status})

    def put(self, room_id):
        # data = request.get_json()
        room_change_auto(room_id)
        return jsonify({'result':'Change Success'})

    def delete(self, room_id):
        delete_all_making_room()
        return jsonify({'result':'Delete All Making Room Success'})

class RoomOG(Resource):
    def post(self):
        data = request.get_json()
        save_og_data(data)

class MyRoomList(Resource):
    def get(self, email):
        room = get_my_room_list(email)
        return jsonify({'data': room})

class RoomLog(Resource):
    def get(self):
        output = get_all_room_logs()
        return jsonify({'data': output})

class MyRoomLog(Resource):
    def get(self, email):
        output = get_my_room_logs(email)
        return jsonify({'data': output})