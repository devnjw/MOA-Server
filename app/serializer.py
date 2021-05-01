# from datetime import datetime
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from .models.participant_model import Participant, ParticipantLog
from .models.room_model import Room, RoomLog
from .models.user_model import User, BlackList
from .models.receipt_model import Receipt, ReceiptImage


class UserSchema(ModelSchema):
    class Meta:
        model = User

users_schema = UserSchema(many=True)

class RoomSchema(ModelSchema):
    class Meta:
        model = Room

room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)

class RoomLogSchema(ModelSchema):
    class Meta:
        model = RoomLog

room_log_schema = RoomLogSchema()
room_logs_schema = RoomLogSchema(many=True)

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