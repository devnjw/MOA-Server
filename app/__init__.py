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

    from .controller.chat_controller import ChatList, Chat, ChatStatus, MyChatList, \
        ChatOG, ChatLog, MyRoomLog
    api.add_resource(ChatList, '/chat')
    api.add_resource(Chat, '/chat/<chat_id>')
    api.add_resource(ChatStatus, '/chat/status/<chat_id>')
    api.add_resource(MyChatList, '/chat/my/<email>')
    api.add_resource(ChatOG, '/chat/og')
    api.add_resource(ChatLog, '/chat/log')
    api.add_resource(MyChatLog, '/chat/log/<email>')

    from .controller.participant_controller import ParticipantList, Participant
    api.add_resource(ParticipantList, '/participant/<chat_id>')
    api.add_resource(Participant, '/participant')

    from .controller.user_controller import UserList, UserPhone, UserAuth
    api.add_resource(UserList, '/user')
    api.add_resource(UserAuth, '/user/<email>')
    api.add_resource(UserPhone, '/user/phone')

    from .controller.bill_controller import Bill, BillList, BillImageList, \
        MyBillImage, NewBillImage
    api.add_resource(BillList, '/bill/<chat_id>')
    api.add_resource(Bill, '/bill/<chat_id>/<user_email>')
    api.add_resource(BillImageList, '/bill/image/<chat_id>')
    api.add_resource(MyBillImage, '/bill/image/<chat_id>/<user_email>')
    api.add_resource(NewBillImage, '/bill/image/<chat_id>/<user_email>/<cost>')

    return app