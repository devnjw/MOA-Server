from app import db

class Participant(db.Model):
    __tablename__ = 'participant'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True, nullable=False)
    room_id = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.VARCHAR(255), nullable=False)
    enter_time = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return "<Participant(id='{}', room_id='{}', user_email={}, enter_time={})>"\
            .format(self.id, self.room_id, self.user_email, self.enter_time)


class ParticipantLog(db.Model):
    __tablename__ = 'participant_log'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True, nullable=False)
    room_id = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.VARCHAR(255), nullable=False)
    enter_time = db.Column(db.TIMESTAMP)
    exit_time = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return "<Participant(id='{}', room_id='{}', user_email={}, exit_time={})>"\
            .format(self.id, self.room_id, self.user_email, self.exit_time)