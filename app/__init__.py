from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from .config import BaseConfig

db = SQLAlchemy()
migrate = Migrate(compare_type=True)

def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    api = Api(app)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from .controller.room_controller import RoomList, Room, RoomStatus, MyRoomList, \
        RoomOG, RoomLog, MyRoomLog
    api.add_resource(RoomList, '/room')
    api.add_resource(Room, '/room/<room_id>')
    api.add_resource(RoomStatus, '/room/status/<room_id>')
    api.add_resource(MyRoomList, '/room/my/<email>')
    api.add_resource(RoomOG, '/room/og')
    api.add_resource(RoomLog, '/room/log')
    api.add_resource(MyRoomLog, '/room/log/<email>')

    from .controller.participant_controller import ParticipantList, Participant
    api.add_resource(ParticipantList, '/participant/<room_id>')
    api.add_resource(Participant, '/participant')

    from .controller.user_controller import UserList, UserPhone, UserAuth
    api.add_resource(UserList, '/user')
    api.add_resource(UserAuth, '/user/<email>')
    api.add_resource(UserPhone, '/user/phone')

    from .controller.receipt_controller import Receipt, ReceiptList, ReceiptImageList, \
        MyReceiptImage, NewReceiptImage
    api.add_resource(ReceiptList, '/receipt/<room_id>')
    api.add_resource(Receipt, '/receipt/<room_id>/<user_email>')
    api.add_resource(ReceiptImageList, '/receipt/image/<room_id>')
    api.add_resource(MyReceiptImage, '/receipt/image/<room_id>/<user_email>')
    api.add_resource(NewReceiptImage, '/receipt/image/<room_id>/<user_email>/<cost>')

    return app