# from datetime import datetime
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from .models.participant_model import Participant, ParticipantLog
from .models.chat_model import Chat, ChatLog
from .models.user_model import User, BlackList
from .models.receipt_model import Receipt, ReceiptImage


class UserSchema(ModelSchema):
    class Meta:
        model = User

users_schema = UserSchema(many=True)

class ChatSchema(ModelSchema):
    class Meta:
        model = Chat

chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)

class ChatLogSchema(ModelSchema):
    class Meta:
        model = ChatLog

chat_log_schema = ChatLogSchema()
chat_logs_schema = ChatLogSchema(many=True)

class ParticipantSchema(ModelSchema):
    class Meta:
        model = Participant

participants_schema = ParticipantSchema(many=True)

class ReceiptSchema(ModelSchema):
    class Meta:
        model = Receipt

receipts_schema = ReceiptSchema(many=True)

class ReceiptImageSchema(ModelSchema):
    class Meta:
        model = ReceiptImage

receipt_images_schema = ReceiptImageSchema(many=True)