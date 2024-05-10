from flask import Flask, request, jsonify, render_template
from datetime import datetime
from libraryms import app, db
from libraryms.models import Administrator, Book, Borrow, Comment, ULibrary, User, UBorrow, Announcement, Consult
from libraryms.util import APIResponse, ResposeCode, book_to_dict, user_to_dict
import json

# TODO 处理异常操作
# @app.errorhandler(404, 500, )


# Restful API设计
'''
    Books 模块
    增:
        POST /books
    删:
        DELETE /books/id
    改:
        PUT /books/id
    查:
        GET /books
            /books/id
'''


# 增 POST
@app.route('/books', methods=['POST'])
def add_book():
    # 接受前端传来的json格式的数据
    data = request.get_json(force=True)
    # 创建一个新的Book对象
    new_book = Book(**data)
    # 添加到数据库
    db.session.add(new_book)
    db.session.commit()

    # 响应消息
    msg = f"添加图书{new_book.book_name}成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.ADD_BOOK_SUCCESS.value, data=None, msg=msg).__dict__)


# 删 DELETE
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    # 通过id找到对应的Book对象
    book = Book.query.get(id)
    # 删除这个对象,并提交到数据库
    db.session.delete(book)
    db.session.commit()

    # 响应消息
    msg = f"删除图书{book.book_name}成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.DELETE_BOOK_SUCCESS.value, data=None, msg=msg).__dict__)


# 改 PUT
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    # 通过id找到对应的Book对象
    book = Book.query.get(id)

    # 接受前端传来的json格式的数据
    data = request.get_json(force=True)

    for key, value in data.items():
        # 如果这个属性存在并且值不相等，就修改这个属性的值
        if hasattr(book, key) and getattr(book, key) != value:
            setattr(book, key, value)

    # 提交到数据库
    db.session.commit()

    # 响应消息
    msg = f"修改图书{book.book_name}成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.UPDATE_BOOK_SUCCESS.value, data=None, msg=msg).__dict__)


# 查 GET
@app.route('/books', methods=['GET'])
def get_all_books():
    # 查询所有的Book对象
    books = Book.query.all()

    # 将Book对象转换成字典格式
    json_books = [book_to_dict(book) for book in books]
    # 响应消息
    msg = "查询所有图书成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.GET_BOOK_SUCCESS.value, data=json_books, msg=msg).__dict__)


@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    # 通过id找到对应的Book对象
    book = Book.query.get(id)

    # 将Book对象转换成字典格式
    json_book = book_to_dict(book)
    # 响应消息
    msg = f"查询图书{book.book_name}成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.GET_BOOK_SUCCESS.value, data=json_book, msg=msg).__dict__)


'''
    User 模块
    增:
        POST /users
    删:
        DELETE /users/id
    改:
        PUT /users/id
    查:
        GET /users
            /users/id
    TODO 密码加密
'''


# 增 POST
@app.route('/users', methods=['POST'])
def add_user():
    # 接受前端传来的json格式的数据
    data = request.get_json(force=True)
    # 创建一个新的User对象
    new_user = User(**data)
    # 添加到数据库
    db.session.add(new_user)
    db.session.commit()

    # 响应消息
    msg = f"添加用户{new_user.user_name}成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.ADD_USER_SUCCESS.value, data=None, msg=msg).__dict__)


# 删 DELETE
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    # 通过id找到对应的User对象
    user = User.query.get(id)
    # 删除这个对象,并提交到数据库
    db.session.delete(user)
    db.session.commit()

    # 响应消息
    msg = f"删除用户{user.user_name}成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.DELETE_USER_SUCCESS.value, data=None, msg=msg).__dict__)


# 改 PUT
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    # 通过id找到对应的User对象
    user = User.query.get(id)

    # 接受前端传来的json格式的数据
    data = request.get_json(force=True)

    for key, value in data.items():
        # 如果这个属性存在并且值不相等，就修改这个属性的值
        if hasattr(user, key) and getattr(user, key) != value:
            setattr(user, key, value)

    # 提交到数据库
    db.session.commit()

    # 响应消息
    msg = f"修改用户{user.user_name}成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.UPDATE_USER_SUCCESS.value, data=None, msg=msg).__dict__)


# 查 GET
@app.route('/users', methods=['GET'])
def get_all_users():
    # 查询所有的User对象
    users = User.query.all()

    # 将User对象转换成字典格式
    json_users = [user_to_dict(user) for user in users]
    # 响应消息
    msg = "查询所有用户成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.GET_USER_SUCCESS.value, data=json_users, msg=msg).__dict__)


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    # 通过id找到对应的User对象
    user = User.query.get(id)

    # 将User对象转换成字典格式
    json_user = user_to_dict(user)
    # 响应消息
    msg = f"查询用户{user.user_name}成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.GET_USER_SUCCESS.value, data=json_user, msg=msg).__dict__)


# ——————————————————————————————————————————————————————————————————
# 登录+个人中心+个人图书城+信息专栏API部分
@app.route('/login', methods=['POST'])
def login_by_account():
    # 获取前端发送过来的账号和密码信息
    account = request.json.get('user_account')
    password = request.json.get('user_password')

    # 在数据库中查找是否存在对应账号的用户
    user = User.query.filter_by(user_account=account).first()

    if user and user.user_password == password:
        # 如果账号密码匹配成功，返回除了密码以外的个人信息给前端
        user_info = {
            'user_id': user.user_id,
            'user_account': user.user_account,
            'user_name': user.user_name,
            'gender': user.gender,
            'phone': user.phone,
            'email': user.email,
            'profile': user.profile
        }
        return jsonify(APIResponse(ResposeCode.GET_USER_SUCCESS.value, data=user_info, msg='success').__dict__)
    else:
        # 如果账号密码匹配失败，返回错误信息给前端
        return jsonify(APIResponse(ResposeCode.GET_USER_ERR.value, data='', msg='error').__dict__)


# 查个人的消息（别人请求借自己图书城的书）
@app.route('/asks/<int:user_id>', methods=['GET'])
def get_asks(user_id):
    # 查询所有is_agree=0且borrower_id为指定用户ID的借书请求
    asks = UBorrow.query.filter_by(is_agree=0, lender_id=user_id).all()
    if asks:
        ask_list = []
        for ask in asks:
            # 查询借书人的用户名
            borrower_name = User.query.filter_by(user_id=ask.borrower_id).first().user_name
            # 将借书请求信息封装为字典
            ask_info = {
                'id': ask.id,
                'username': borrower_name,
                'bookName': ask.book_name,
                'time': ask.borrow_date.strftime('%Y-%m-%d')  # 将日期格式化为字符串
            }

            ask_list.append(ask_info)

        # 将列表转换为JSON格式并返回给前端
        return jsonify(APIResponse(ResposeCode.GET_UBorrow_SUCCESS.value, data=ask_list, msg='success').__dict__)
    else:
        # 如果没有找到相关的借书请求，返回空列表给前端
        return jsonify(APIResponse(ResposeCode.GET_UBorrow_ERR.value, data='', msg='error').__dict__)


# 查个人借阅信息
@app.route('/borrows/<int:user_id>', methods=['GET'])
def get_borrows(user_id):
    try:
        # 查询用户借阅信息
        borrows = Borrow.query.filter_by(user_id=user_id).filter(
            (Borrow.is_agree == 0) | ((Borrow.is_agree == 1) & (Borrow.is_return == 0))).all()
        # 封装数据
        borrow_data = []
        for borrow in borrows:
            # 查询书籍信息
            book = Book.query.filter_by(book_id=borrow.book_id).first()
            print(book)
            if not book:
                continue  # 如果书籍不存在，则跳过当前借阅信息
            # 格式化日期
            borrow_date = borrow.borrow_date.strftime('%Y-%m-%d') if borrow.borrow_date else ""
            expired_date = borrow.expired_date.strftime('%Y-%m-%d') if borrow.expired_date else ""
            # 封装数据
            borrow_info = {
                'id': borrow.id,
                'book_id': borrow.book_id,
                'cover': book.cover,
                'book_name': borrow.book_name,
                'borrow_date': borrow_date,
                'expired_date': expired_date,
                'isAgree': borrow.is_agree
            }
            borrow_data.append(borrow_info)

        return jsonify(APIResponse(ResposeCode.GET_Borrow_SUCCESS.value, data=borrow_data, msg='success').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.GET_Borrow_ERR.value, data="", msg='error').__dict__)


# 取消某个借书申请
@app.route('/borrows/<int:id>', methods=['DELETE'])
def delete_borrows(id):
    try:
        # 查询是否存在对应的借阅记录
        borrow = Borrow.query.get(id)
        if not borrow:
            return jsonify(APIResponse(ResposeCode.DELETE_Borrow_ERR.value, data="", msg='未发现该图书').__dict__)

        db.session.delete(borrow)  # 从数据库中删除借阅记录
        db.session.commit()

        return jsonify(APIResponse(ResposeCode.DELETE_Borrow_SUCCESS.value, data="",
                                   msg='取消申请成功').__dict__)
    except Exception as e:
        return jsonify(
            APIResponse(ResposeCode.DELETE_Borrow_ERR.value, data="", msg='error').__dict__)


# 还特定书籍
@app.route('/borrows/<int:id>', methods=['PUT'])
def update_borrows(id):
    try:
        # 查询是否存在对应的借阅记录
        borrow = Borrow.query.get(id)
        if not borrow:
            return jsonify(APIResponse(ResposeCode.UPDATE_Borrow_ERR.value, data="", msg='未发现记录').__dict__)

        # 将对应的借阅记录的 is_return 字段设置为 1
        borrow.is_return = 1
        db.session.commit()

        return jsonify(APIResponse(ResposeCode.UPDATE_Borrow_SUCCESS.value, data="", msg='还书成功！').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.UPDATE_Borrow_ERR.value, data="", msg='error').__dict__)


# 查借书记录
@app.route('/borrowsHistory/<int:user_id>', methods=['GET'])
def get_borrows_history(user_id):
    try:
        # 查询用户借书历史记录（is_agree=1表示借出）
        borrows = Borrow.query.filter_by(user_id=user_id, is_agree=1).all()
        # 封装数据
        borrow_data = []
        for borrow in borrows:
            # 查询书籍信息
            book = Book.query.get(borrow.book_id)
            if book:
                # 封装书籍信息
                book_info = {
                    'book_id': book.book_id,
                    'cover': book.cover,
                    'book_name': book.book_name,
                    'author': book.author,
                    'category': book.category,
                    'press': book.press,
                    'borrow_date': borrow.borrow_date.strftime('%Y-%m-%d'),
                    'id': borrow.id
                }
                borrow_data.append(book_info)

        return jsonify(APIResponse(ResposeCode.GET_Borrow_SUCCESS.value, data=borrow_data, msg='success').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.GET_Borrow_ERR.value, data="", msg='error').__dict__)


# 删除借书记录
@app.route('/borrowsHistory/<int:id>', methods=['DELETE'])
def delete_borrows_history(id):
    try:
        # 查询是否存在对应的借阅记录
        borrow = Borrow.query.get(id)
        if not borrow:
            return jsonify(APIResponse(ResposeCode.DELETE_Borrow_ERR.value, data="", msg='未发现记录').__dict__)

        # 删除记录
        db.session.delete(borrow)
        db.session.commit()

        return jsonify(APIResponse(ResposeCode.DELETE_Borrow_SUCCESS.value, data="",
                                   msg='删除成功！').__dict__)
    except Exception as e:
        return jsonify(
            APIResponse(ResposeCode.DELETE_Borrow_ERR.value, data="", msg='error').__dict__)


# 个人图书馆资源查询
@app.route('/myResources/<int:user_id>', methods=['GET'])
def get_my_resources(user_id):
    try:
        # 查询属于个人图书馆的图书
        personal_books = ULibrary.query.filter_by(user_id=user_id).all()
        # 封装数据
        books_data = []
        for book in personal_books:
            # 查询该图书的所有借阅记录
            borrow_records = UBorrow.query.filter_by(book_id=book.id).all()
            # 判断是否有符合条件的借阅记录
            status = 0
            for record in borrow_records:
                if record.is_agree == 1 and record.is_return == 0:
                    status = 1  # 已借阅但未归还
                    break  # 如果找到符合条件的记录，跳出循环
            # 封装数据
            book_info = {
                'book_id': book.id,
                'bookName': book.book_name,
                'author': book.author,
                'category': book.category,
                'press': book.press,
                'status': status
            }
            books_data.append(book_info)

        return jsonify(APIResponse(ResposeCode.GET_ULibrary_SUCCESS.value, data=books_data, msg='查询成功').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.GET_ULibrary_ERR.value, data="", msg='error').__dict__)


# 个人图书下架
@app.route('/myResources/<int:id>', methods=['DELETE'])
def delete_my_resources(id):
    try:
        # 查询要删除的图书
        book_to_delete = ULibrary.query.get(id)
        # 如果图书不存在，返回404
        if not book_to_delete:
            return jsonify(APIResponse(ResposeCode.DELETE_UBorrow_ERR.value, data="", msg='未发现书籍！').__dict__)

        # 删除图书
        db.session.delete(book_to_delete)
        db.session.commit()

        return jsonify(APIResponse(ResposeCode.DELETE_UBorrow_SUCCESS.value, data="", msg='下架成功！').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.DELETE_UBorrow_ERR.value, data="", msg='error').__dict__)


# 个人借阅其他“个人图书城”的借阅情况
@app.route('/otherResources/<int:borrower_id>', methods=['GET'])
def get_other_resource(borrower_id):
    try:
        # 查询符合条件的借书信息,未审查的或者是未归还的
        borrow_info = UBorrow.query.filter(
            UBorrow.borrower_id == borrower_id,
            (UBorrow.is_agree == 0) | ((UBorrow.is_agree == 1) & (UBorrow.is_return == 0))
        ).with_entities(
            UBorrow.id,
            UBorrow.book_id,
            UBorrow.book_name,
            UBorrow.borrow_date,
            UBorrow.is_agree
        ).all()

        # 封装数据
        borrow_data = []
        for borrow in borrow_info:
            borrow_info = {
                'id': borrow.id,
                'book_id': borrow.book_id,
                'book_name': borrow.book_name,
                'borrow_date': borrow.borrow_date,
                'is_agree': borrow.is_agree
            }
            borrow_data.append(borrow_info)

        return jsonify(APIResponse(ResposeCode.GET_UBorrow_SUCCESS.value, data=borrow_data, msg='查询成功！').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.GET_UBorrow_ERR.value, data="", msg='error').__dict__)


# 个人图书城的还书
@app.route('/otherResources/<int:id>', methods=['PUT'])
def update_other_resources(id):
    try:
        # 查询指定ID的借书记录
        borrow_record = UBorrow.query.get(id)
        if borrow_record:
            # 将借书记录的is_return字段置为1
            borrow_record.is_return = 1
            db.session.commit()  # 提交事务
            return jsonify(APIResponse(ResposeCode.UPDATE_UBorrow_SUCCESS.value, data="", msg='还书成功！').__dict__)
        else:
            return jsonify(APIResponse(ResposeCode.UPDATE_UBorrow_ERR.value, data="", msg='未找到资源！').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.UPDATE_UBorrow_ERR.value, data="", msg='error').__dict__)


# 个人图书城的取消申请
@app.route('/otherResources/<int:id>', methods=['DELETE'])
def delete_other_resources(id):
    try:
        # 查询指定ID的借书记录，需要是is_agree=0还未通过的
        borrow_record = UBorrow.query.filter_by(id=id, is_agree=0).first()

        if borrow_record:
            db.session.delete(borrow_record)  # 取消申请
            db.session.commit()  # 提交事务
            return jsonify(APIResponse(ResposeCode.DELETE_UBorrow_SUCCESS.value, data="", msg='取消申请成功').__dict__)
        else:
            return jsonify(APIResponse(ResposeCode.DELETE_UBorrow_ERR.value, data="", msg='未找到资源！').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.DELETE_UBorrow_ERR.value, data="", msg='error').__dict__)


# 个人图书资源上传
@app.route('/myResources', methods=['POST'])
def post_my_resources():
    try:
        # 从请求中获取书籍信息数据
        data = request.get_json()

        new_book = ULibrary(
            user_id=data['user_id'],
            book_name=data['book_name'],
            author=data['author'],
            category=data['category'],
            press=data['press'],
            introduction=data['introduction']
        )
        db.session.add(new_book)
        db.session.commit()

        return jsonify(APIResponse(ResposeCode.ADD_ULibrary_SUCCESS.value, data="", msg='success').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.ADD_ULibrary_SUCCESS.value, data="", msg='error').__dict__)


# 信息专栏公告
@app.route('/announcements', methods=['GET'])
def get_announcements():
    try:
        # 查询所有公告，并按照时间排序
        announcements = Announcement.query.order_by(Announcement.publish_time.desc()).all()
        # 封装数据
        announcement_data = []
        for announcement in announcements:
            announcement_info = {
                'id': announcement.id,
                'title': announcement.title,
                'content': announcement.content,
                'publish_time': announcement.publish_time
            }
            announcement_data.append(announcement_info)

        return jsonify(APIResponse(ResposeCode.GET_Announcement_SUCCESS.value, data=announcement_data, msg='success').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.GET_Announcement_ERR.value, data="", msg='error').__dict__)


# 读者咨询
@app.route('/consults', methods=['POST'])
def post_consults():
    try:
        # 从请求中获取咨询数据
        data = request.get_json()

        # 创建咨询对象并插入数据库
        new_consult = Consult(
            user_id=data['user_id'],
            user_name=data['user_name'],
            title=data['title'],
            content=data['content'],
            consult_date=datetime.now()  # 记录当前时间
        )
        db.session.add(new_consult)
        db.session.commit()

        return jsonify(APIResponse(ResposeCode.ADD_Consult_SUCCESS.value, data="", msg='success').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.ADD_Consult_SUCCESS.value, data="", msg='error').__dict__)


# ——————————————————————————————————————————————————————————————————

if __name__ == '__main__':
    app.run()
