from app import db

class Receipt(db.Model):
    __tablename__ = 'receipt'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.VARCHAR(45), nullable=False)
    stuff_name = db.Column(db.VARCHAR(45))
    stuff_img = db.Column(db.VARCHAR(225))
    stuff_cost = db.Column(db.Integer)
    stuff_num = db.Column(db.Integer)
    ref_cnt = db.Column(db.Integer)
    registered_on = db.Column(db.TIMESTAMP)

class ReceiptImage(db.Model):
    __tablename__ = 'receipt_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.VARCHAR(45), nullable=False)
    image_path = db.Column(db.VARCHAR(225))
    image_cost = db.Column(db.Integer)
    uploaded_on = db.Column(db.TIMESTAMP)
