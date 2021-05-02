from flask import request, jsonify, send_file, make_response, url_for
from flask_restful import Resource, abort

import zipfile, os

from ..service.bill_service import get_total_bills_in, get_my_bills_in, \
    save_new_bills, save_a_new_bill, save_bill_image, \
    get_my_bill_imageurls_in, get_total_bill_imageurls_in, edit_bills, \
    delete_bill_image

class BillList(Resource):
    def get(self, chat_id):
        bills, total_cost = get_total_bills_in(chat_id)
        return jsonify({'bills': bills, 'total_cost': int(total_cost)})

    def post(self, chat_id):
        datas = request.get_json()
        bills_id = save_new_bills(datas['data'])
        return jsonify({'ids':bills_id})

    def put(self, chat_id):
        datas = request.get_json()
        bills_id = edit_bills(datas['data'])
        return jsonify({'ids':bills_id})

class Bill(Resource):
    def get(self, chat_id, user_email):
        bills, total_cost = get_my_bills_in(chat_id, user_email)
        return jsonify({'bills': bills, 'total_cost': int(total_cost)})

    def post(self, chat_id, user_email):
        data = request.get_json()
        save_a_new_bill(data)
        return jsonify({'result': "Success"})

class MyBillImage(Resource):
    def get(self, chat_id, user_email):
        image_uris, total_cost = get_my_bill_imageurls_in(chat_id, user_email)
        return jsonify({'bills':image_uris, 'total_cost': int(total_cost)})

    
    
class NewBillImage(Resource):
    def post(self, chat_id, user_email, cost):
        imagefile = request.files['file']
        save_bill_image(imagefile, chat_id, user_email, cost)
        return jsonify({'result': "Image Uploaded Successfully"})


class BillImageList(Resource):
    def get(self, chat_id):
        image_uris, total_cost = get_total_bill_imageurls_in(chat_id)
        return jsonify({'bills':image_uris, 'total_cost': int(total_cost)})

    def delete(self, chat_id):
        data = request.get_json()
        delete_bill_image(chat_id, data['filename'])
        return jsonify({'result': "Image Deleted Successfully"})

    