from flask import jsonify
import werkzeug
from flask_restful import abort
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename

import uuid
import os

from datetime import datetime, timedelta

from app import db
from app.models.receipt_model import Receipt, ReceiptImage

from ..serializer import ReceiptSchema, receipts_schema, receipt_images_schema


def get_total_receipts_in(room_id):
    total_num = Receipt.query.group_by(Receipt.room_id, Receipt.stuff_name).filter_by(room_id=room_id).\
        add_columns(func.sum(Receipt.stuff_num).label("stuff_num"), Receipt.stuff_name, Receipt.stuff_cost).all()

    total_price = Receipt.query.group_by(Receipt.room_id).filter_by(room_id=room_id).\
        add_columns(func.sum(Receipt.stuff_cost * Receipt.stuff_num).label("total_cost")).first()

    receipts = []
    for num in total_num:
        result={}
        result['stuff_cost'] = (num.stuff_cost)
        result['stuff_name'] = (num.stuff_name)
        result['stuff_num'] = (int(num.stuff_num))
        receipts.append(result)

    if total_price:
        total_cost = total_price.total_cost
    else:
        total_cost = 0
    return receipts, total_cost

def get_my_receipts_in(room_id, user_email):
    total_num = Receipt.query.group_by(Receipt.room_id, Receipt.stuff_name, Receipt.user_id).\
        filter_by(room_id=room_id, user_id=user_email).\
        add_columns(func.sum(Receipt.stuff_num).label("stuff_num"), Receipt.stuff_name, Receipt.stuff_cost).all()

    total_price = Receipt.query.group_by(Receipt.room_id).filter_by(room_id=room_id, user_id=user_email).\
        add_columns(func.sum(Receipt.stuff_cost * Receipt.stuff_num).label("total_cost")).first()

    receipts = []
    for num in total_num:
        result={}
        result['stuff_cost'] = (num.stuff_cost)
        result['stuff_name'] = (num.stuff_name)
        result['stuff_num'] = (int(num.stuff_num))
        receipts.append(result)

    if total_price:
        total_cost = total_price.total_cost
    else:
        total_cost = 0
    return receipts, total_cost

def save_new_receipts(datas):
    try:
        # print("SAVE NEW RECEIPTS:", datas)
        result_ids=[]
        for data in datas:
            new_receipt = Receipt(
                room_id=data['room_id'],
                user_id=data['user_email'],
                stuff_name = data['stuff_name'],
                stuff_cost = data['stuff_cost'],
                stuff_num = data['stuff_num'],
                stuff_img = data['stuff_img'],
                ref_cnt = data['stuff_num'],
                registered_on = datetime.utcnow() + timedelta(hours=9) # 한국 시간으로 조정
            )
            db.session.add(new_receipt)
            
            receipt = Receipt.query.\
                filter_by(room_id=data['room_id'], stuff_name=data['stuff_name']).first()
            
            if receipt:
                receipt.ref_cnt += data['stuff_num']

            db.session.commit()
            result_ids.append(new_receipt.id)
    except Exception as e:
            print(e)
            abort(500)
    return result_ids

def save_a_new_receipt(data):
    try:
        print("SAVE a NEW RECEIPT:", data)
        new_receipt = Receipt(
            room_id=data['room_id'],
            user_id=data['user_email'],
            stuff_name = data['stuff_name'],
            stuff_cost = data['stuff_cost'],
            stuff_num = data['stuff_num'],
            ref_cnt = data['stuff_num'],
            registered_on = datetime.utcnow() + timedelta(hours=9) # 한국 시간으로 조정
        )
        db.session.add(new_receipt)
        db.session.commit()
    except Exception as e:
            print(e)
            abort(500)
    return new_receipt

def edit_receipts(datas):
    delete_all_receipts(datas[0]['room_id'], datas[0]['user_email'])
    return save_new_receipts(datas)

def delete_all_receipts(room_id, user_email):
    try:
        result = Receipt.query.filter_by(room_id=room_id, user_id=user_email).delete()
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)

def get_total_receipt_imageurls_in(room_id):
    images = ReceiptImage.query.filter_by(room_id=room_id)\
        .with_entities(ReceiptImage.image_path, ReceiptImage.image_cost).all()
    images = receipt_images_schema.dump(images)
    

    # 이 부분 주석처리하고 return images 하면 각각 가격 같이 반환
    # filepaths = []
    # for image in images:
    #     filepaths.append(image['image_path'])

    total_price = ReceiptImage.query.group_by(ReceiptImage.room_id).filter_by(room_id=room_id).\
        add_columns(func.sum(ReceiptImage.image_cost).label("total_cost")).first()

    if total_price:
        total_cost = total_price.total_cost
    else:
        total_cost = 0

    return images, total_cost

def get_my_receipt_imageurls_in(room_id, user_email):
    images = ReceiptImage.query.filter_by(room_id=room_id, user_id=user_email)\
        .with_entities(ReceiptImage.image_path, ReceiptImage.image_cost).all()
    images = receipt_images_schema.dump(images)

    # 이 부분 주석처리하고 return images 하면 각각 가격 같이 반환
    # filepaths = []
    # for image in images:
    #     filepaths.append(image['image_path'])

    total_price = ReceiptImage.query.group_by(ReceiptImage.room_id).filter_by(room_id=room_id, user_id=user_email).\
        add_columns(func.sum(ReceiptImage.image_cost).label("total_cost")).first()

    if total_price:
        total_cost = total_price.total_cost
    else:
        total_cost = 0

    return images, total_cost

def save_receipt_image(imagefile, room_id, user_email, cost):
    DATE = datetime.utcnow()+timedelta(hours=9)
    DATE = DATE.strftime('%Y-%m-%d-%H-%M-%S')

    # FILENAME = DATE + '.jpg'
    FILENAME = str(uuid.uuid4())
    FILEPATH = os.getcwd() + '/app/static/receipts/' + room_id + '/'
    os.makedirs(FILEPATH, exist_ok=True) # 폴더 없으면 자동 생성
    
    #filename = werkzeug.utils.secure_filename(imagefile.filename)
    imagefile.save( FILEPATH + FILENAME )

    try:
        new_image = ReceiptImage(
            room_id=room_id,
            user_id=user_email,
            image_path=FILENAME,
            image_cost=cost,
            uploaded_on = datetime.utcnow() + timedelta(hours=9)
        )
        db.session.add(new_image)
        db.session.commit()
    except Exception as e:
            print(e)
            abort(500)
    return new_image

def delete_receipt_image(room_id, filename):
    ReceiptImage.query.filter_by(room_id=room_id, image_path=filename).delete()
    db.session.commit()
