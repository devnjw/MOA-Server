from flask import jsonify
import werkzeug
from flask_restful import abort
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename

import uuid
import os

from datetime import datetime, timedelta

from app import db
from app.models.bill_model import Bill, BillImage

from ..serializer import billSchema, bills_schema, bill_images_schema


def get_total_bills_in(chat_id):
    total_num = Bill.query.group_by(Bill.chat_id, Bill.stuff_name).filter_by(chat_id=chat_id).\
        add_columns(func.sum(Bill.stuff_num).label("stuff_num"), Bill.stuff_name, Bill.stuff_cost).all()

    total_price = Bill.query.group_by(Bill.chat_id).filter_by(chat_id=chat_id).\
        add_columns(func.sum(Bill.stuff_cost * Bill.stuff_num).label("total_cost")).first()

    bills = []
    for num in total_num:
        result={}
        result['stuff_cost'] = (num.stuff_cost)
        result['stuff_name'] = (num.stuff_name)
        result['stuff_num'] = (int(num.stuff_num))
        bills.append(result)

    if total_price:
        total_cost = total_price.total_cost
    else:
        total_cost = 0
    return Bills, total_cost

def get_my_bills_in(chat_id, user_email):
    total_num = Bill.query.group_by(Bill.chat_id, Bill.stuff_name, Bill.user_id).\
        filter_by(chat_id=chat_id, user_id=user_email).\
        add_columns(func.sum(Bill.stuff_num).label("stuff_num"), Bill.stuff_name, Bill.stuff_cost).all()

    total_price = Bill.query.group_by(Bill.chat_id).filter_by(chat_id=chat_id, user_id=user_email).\
        add_columns(func.sum(Bill.stuff_cost * Bill.stuff_num).label("total_cost")).first()

    bills = []
    for num in total_num:
        result={}
        result['stuff_cost'] = (num.stuff_cost)
        result['stuff_name'] = (num.stuff_name)
        result['stuff_num'] = (int(num.stuff_num))
        bills.append(result)

    if total_price:
        total_cost = total_price.total_cost
    else:
        total_cost = 0
    return bills, total_cost

def save_new_bills(datas):
    try:
        # print("SAVE NEW BillS:", datas)
        result_ids=[]
        for data in datas:
            new_Bill = Bill(
                chat_id=data['chat_id'],
                user_id=data['user_email'],
                stuff_name = data['stuff_name'],
                stuff_cost = data['stuff_cost'],
                stuff_num = data['stuff_num'],
                stuff_img = data['stuff_img'],
                ref_cnt = data['stuff_num'],
                registered_on = datetime.utcnow() + timedelta(hours=9) # 한국 시간으로 조정
            )
            db.session.add(new_Bill)
            
            bill = Bill.query.\
                filter_by(chat_id=data['chat_id'], stuff_name=data['stuff_name']).first()
            
            if bill:
                bill.ref_cnt += data['stuff_num']

            db.session.commit()
            result_ids.append(new_Bill.id)
    except Exception as e:
            print(e)
            abort(500)
    return result_ids

def save_a_new_bill(data):
    try:
        print("SAVE a NEW Bill:", data)
        new_bill = Bill(
            chat_id=data['chat_id'],
            user_id=data['user_email'],
            stuff_name = data['stuff_name'],
            stuff_cost = data['stuff_cost'],
            stuff_num = data['stuff_num'],
            ref_cnt = data['stuff_num'],
            registered_on = datetime.utcnow() + timedelta(hours=9) # 한국 시간으로 조정
        )
        db.session.add(new_bill)
        db.session.commit()
    except Exception as e:
            print(e)
            abort(500)
    return new_bill

def edit_bills(datas):
    delete_all_bills(datas[0]['chat_id'], datas[0]['user_email'])
    return save_new_bills(datas)

def delete_all_bills(chat_id, user_email):
    try:
        result = Bill.query.filter_by(chat_id=chat_id, user_id=user_email).delete()
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)

def get_total_bill_imageurls_in(chat_id):
    images = BillImage.query.filter_by(chat_id=chat_id)\
        .with_entities(BillImage.image_path, BillImage.image_cost).all()
    images = bill_images_schema.dump(images)
    

    # 이 부분 주석처리하고 return images 하면 각각 가격 같이 반환
    # filepaths = []
    # for image in images:
    #     filepaths.append(image['image_path'])

    total_price = BillImage.query.group_by(BillImage.chat_id).filter_by(chat_id=chat_id).\
        add_columns(func.sum(BillImage.image_cost).label("total_cost")).first()

    if total_price:
        total_cost = total_price.total_cost
    else:
        total_cost = 0

    return images, total_cost

def get_my_bill_imageurls_in(chat_id, user_email):
    images = BillImage.query.filter_by(chat_id=chat_id, user_id=user_email)\
        .with_entities(BillImage.image_path, BillImage.image_cost).all()
    images = bill_images_schema.dump(images)

    # 이 부분 주석처리하고 return images 하면 각각 가격 같이 반환
    # filepaths = []
    # for image in images:
    #     filepaths.append(image['image_path'])

    total_price = BillImage.query.group_by(BillImage.chat_id).filter_by(chat_id=chat_id, user_id=user_email).\
        add_columns(func.sum(BillImage.image_cost).label("total_cost")).first()

    if total_price:
        total_cost = total_price.total_cost
    else:
        total_cost = 0

    return images, total_cost

def save_bill_image(imagefile, chat_id, user_email, cost):
    DATE = datetime.utcnow()+timedelta(hours=9)
    DATE = DATE.strftime('%Y-%m-%d-%H-%M-%S')

    # FILENAME = DATE + '.jpg'
    FILENAME = str(uuid.uuid4())
    FILEPATH = os.getcwd() + '/app/static/Bills/' + chat_id + '/'
    os.makedirs(FILEPATH, exist_ok=True) # 폴더 없으면 자동 생성
    
    #filename = werkzeug.utils.secure_filename(imagefile.filename)
    imagefile.save( FILEPATH + FILENAME )

    try:
        new_image = BillImage(
            chat_id=chat_id,
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

def delete_bill_image(chat_id, filename):
    BillImage.query.filter_by(chat_id=chat_id, image_path=filename).delete()
    db.session.commit()
