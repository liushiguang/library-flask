from libraryms import db


class Administrator(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    admin_name = db.Column(db.String(50))
    admin_password = db.Column(db.String(255))
    gender = db.Column(db.String(2))
    phone = db.Column(db.String(11))


class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    category = db.Column(db.String(50))
    press = db.Column(db.String(50))
    introduction = db.Column(db.Text)
    stars = db.Column(db.Integer)
    number = db.Column(db.Integer)
    cover = db.Column(db.String(255))


class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(50))
    book_id = db.Column(db.Integer)
    book_name = db.Column(db.String(50))
    borrow_date = db.Column(db.Date)
    expired_date = db.Column(db.Date)
    is_agree = db.Column(db.Integer)  # 是否同意 -1 拒绝 0 未操作 1 已同意
    is_return = db.Column(db.Boolean)  # 是否归还 0 未归还 1 已归还

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(50))
    book_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    comment_date = db.Column(db.Date)


class ULibrary(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer)
    book_name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    category = db.Column(db.String(50))
    press = db.Column(db.String(50))
    introduction = db.Column(db.Text)


class UBorrow(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    borrower_id = db.Column(db.Integer)
    lender_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    book_name = db.Column(db.String(50))
    borrow_date = db.Column(db.Date)
    is_agree = db.Column(db.Integer)    # 是否同意 -1 拒绝 0 未操作 1 已同意
    is_return = db.Column(db.Boolean)   # 是否归还 0 未归还 1 已归还

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_account = db.Column(db.String(20))
    user_name = db.Column(db.String(50))
    user_password = db.Column(db.String(255))
    gender = db.Column(db.String(2))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(20))
    profile = db.Column(db.Text)
    cover = db.Column(db.String(255))

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    publish_time = db.Column(db.DateTime)

class Consult(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(50))
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    consult_time = db.Column(db.DateTime)

class TTS_Info:
    def __init__(self, book_name, text):
        self.book_name = book_name
        self.text = text
