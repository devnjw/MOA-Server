from flask import request, jsonify, send_file, make_response, url_for
from flask_restful import Resource, abort

import zipfile, os

from ..service.receipt_service import get_total_receipts_in, get_my_receipts_in, \
    save_new_receipts, save_a_new_receipt, save_receipt_image, \
    get_my_receipt_imageurls_in, get_total_receipt_imageurls_in, edit_receipts, \
    delete_receipt_image

class ReceiptList(Resource):
    def get(self, room_id):
        receipts, total_cost = get_total_receipts_in(room_id)
        return jsonify({'receipts': receipts, 'total_cost': int(total_cost)})

    def post(self, room_id):
        datas = request.get_json()
        receipts_id = save_new_receipts(datas['data'])
        return jsonify({'ids':receipts_id})

    def put(self, room_id):
        datas = request.get_json()
        receipts_id = edit_receipts(datas['data'])
        return jsonify({'ids':receipts_id})

class Receipt(Resource):
    def get(self, room_id, user_email):
        receipts, total_cost = get_my_receipts_in(room_id, user_email)
        return jsonify({'receipts': receipts, 'total_cost': int(total_cost)})

    def post(self, room_id, user_email):
        data = request.get_json()
        save_a_new_receipt(data)
        return jsonify({'result': "Success"})

class MyReceiptImage(Resource):
    def get(self, room_id, user_email):
        image_uris, total_cost = get_my_receipt_imageurls_in(room_id, user_email)
        return jsonify({'receipts':image_uris, 'total_cost': int(total_cost)})

    
    
class NewReceiptImage(Resource):
    def post(self, room_id, user_email, cost):
        imagefile = request.files['file']
        save_receipt_image(imagefile, room_id, user_email, cost)
        return jsonify({'result': "Image Uploaded Successfully"})


class ReceiptImageList(Resource):
    def get(self, room_id):
        image_uris, total_cost = get_total_receipt_imageurls_in(room_id)
        return jsonify({'receipts':image_uris, 'total_cost': int(total_cost)})

    def delete(self, room_id):
        data = request.get_json()
        delete_receipt_image(room_id, data['filename'])
        return jsonify({'result': "Image Deleted Successfully"})

    