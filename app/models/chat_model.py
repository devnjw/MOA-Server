from app import db

class Chat(db.Model):
    __tablename__ = 'room'
    rid = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True, nullable=False)
    status = db.Column(db.VARCHAR(15))
    category = db.Column(db.VARCHAR(45))
    title = db.Column(db.VARCHAR(45))
    place = db.Column(db.VARCHAR(45))
    num_user = db.Column(db.Integer)
    creator_name = db.Column(db.VARCHAR(45))
    creator_email = db.Column(db.VARCHAR(45))
    order_date = db.Column(db.VARCHAR(15))
    order_time = db.Column(db.VARCHAR(15))
    stuff_link = db.Column(db.VARCHAR(255))
    create_time = db.Column(db.TIMESTAMP)
    update_time = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return "<Room(rid='{}', category='{}', title={}, place={}, creator_name={}, num_user={}, create_time={}, update_time={})>"\
            .format(self.rid, self.category, self.title, self.place, self.creator_name, self.num_user, self.create_time, self.update_time)

class ChatOG(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True, nullable=False)
    chat_id = db.Column(db.Integer, unique=True, nullable=False)
    image_url = db.Column(db.VARCHAR(255))
    og_title = db.Column(db.VARCHAR(45))

class ChatLog(db.Model):
    __tablename__ = 'room_log'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True, nullable=False)
    rid = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.VARCHAR(15))
    category = db.Column(db.VARCHAR(45))
    title = db.Column(db.VARCHAR(45))
    place = db.Column(db.VARCHAR(45))
    num_user = db.Column(db.Integer)
    creator_name = db.Column(db.VARCHAR(45))
    creator_email = db.Column(db.VARCHAR(45))
    order_date = db.Column(db.VARCHAR(15))
    order_time = db.Column(db.VARCHAR(15))
    stuff_link = db.Column(db.VARCHAR(255))
    create_time = db.Column(db.TIMESTAMP)
    update_time = db.Column(db.TIMESTAMP)
    deleted_time = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return "<ChatLog(rid='{}', category='{}', title={}, place={}, creator_name={}, num_user={}, create_time={}, update_time={}, deleted_time={})>"\
            .format(self.rid, self.category, self.title, self.place, self.creator_name, self.num_user, self.create_time, self.update_time, self.deleted_time)
