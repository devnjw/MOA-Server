from flask import request, jsonify
from flask_restful import Resource, abort

from ..service.participant_service import get_all_participants, get_participants_in, save_new_participant,\
    delete_participant, is_new_participant, count_participants
from ..service.room_service import delete_a_room, change_the_room_status
from ..service.receipt_service import delete_all_receipts

class ParticipantList(Resource):
    ''' 지정 방에 참여 중인 유저 반환 '''
    def get(self, room_id):
        participants = get_participants_in(room_id)
        return jsonify({'data': participants})

    ''' 새로운 참여자인지 반환 '''
    def post(self, room_id):
        data = request.get_json()
        is_new = is_new_participant(data)
        return jsonify({'is_new': is_new})

class Participant(Resource):
    def get(self):
        all_participants = get_all_participants()
        return jsonify({'data': all_participants})

    ''' 새로운 참여자 저장 '''
    def post(self):
        data = request.get_json()
        print("new participant:", data)
        save_new_participant(data)
        if count_participants(data['room_id']) == 1: # == 방 생성중 -> 모집중으로 바뀌면
            change_the_room_status(data['room_id'], "모집중")

        return jsonify({'result': "Success"})

    def delete(self):
        data = request.get_json()
        rid = delete_participant(data) # return false if participant is not in room
        if rid:
            delete_all_receipts(rid, data['user_email'])
        if rid and count_participants(rid) == 0:
            data = {'room_id':rid}
            delete_a_room(data)
        return jsonify({'result': "Success"})
    