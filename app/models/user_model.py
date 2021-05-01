from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.VARCHAR(255))
    email = db.Column(db.VARCHAR(45), unique=True, nullable=False)
    name = db.Column(db.VARCHAR(45), unique=True)
    phone = db.Column(db.VARCHAR(45))
    account = db.Column(db.VARCHAR(45))
    photo_url = db.Column(db.VARCHAR(255))
    registered_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime)
    cnt_login = db.Column(db.Integer)


    def __repr__(self):
        return "<User(email='{}', name='{}', phone={}, account={}, photo_url={}, registered_on={})>"\
            .format(self.email, self.name, self.phone, self.account, self.photo_url, self.registered_on)

# class UserLog(db.Model):
#     __tablename__ = 'user_log'
#     user_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True, nullable=False)
#     registered_on = db.Column(db.DateTime, nullable=False)
#     last_login = db.Column(db.DateTime, nullable=False)
#     cnt_login = db.Column(db.Integer)

class BlackList(db.Model):
    __tablename__ = 'blacklist'
    email = db.Column(db.VARCHAR(45), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.VARCHAR(45), unique=True)
    phone = db.Column(db.VARCHAR(45))
    account = db.Column(db.VARCHAR(45))
    photo_url = db.Column(db.VARCHAR(255))
    registered_on = db.Column(db.DateTime, nullable=False)
    listed_on = db.Column(db.DateTime, nullable=False)