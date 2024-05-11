from flask import Flask, request, jsonify, render_template
from libraryms import app, db
from libraryms.models import Administrator, Book, Borrow, Comment, U_Library, User, U_Borrow, Annocement, Consult
from libraryms.util import APIResponse, ResposeCode, book_to_dict, user_to_dict, borrow_to_dict, consult_to_dict, annocement_to_dict
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
    # TODO 封面

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
    # TODO 封面

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


'''
    Borrow 模块
    增:
        POST /borrows
    删:
        DELETE /borrows/id
    改:
        PUT /borrows/id
    查:
        GET /borrows
            /borrows/id
'''
# 增 POST
@app.route('/borrows', methods=['POST'])
def add_borrow():
    # 接受前端传来的json格式的数据
    data = request.get_json(force=True)
    # 创建一个新的Borrows对象
    new_borrow = Borrow(**data)
    # 添加到数据库
    db.session.add(new_borrow)
    db.session.commit()

    # 响应消息
    msg = f"用户{new_borrow.user_name}在{new_borrow.borrow_date}申请借阅了{new_borrow.book_name}"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.ADD_BORROW_SUCCESS.value, data=None, msg=msg).__dict__)

# 删 DELETE
@app.route('/borrows/<int:id>', methods=['DELETE'])
def delete_borrow(id):
    # 通过id找到对应的Borrow对象
    borrow = Borrow.query.get(id)
    # 删除这个对象,并提交到数据库
    db.session.delete(borrow)
    db.session.commit()

    # 响应消息
    msg = f"删除用户{borrow.user_name}在{borrow.borrow_date}借阅{borrow.book_name}的申请"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.DELETE_BORROW_SUCCESS.value, data=None, msg=msg).__dict__)

# 改 PUT
@app.route('/borrows/<int:id>', methods=['PUT'])
def update_borrow(id):

    # 通过id找到对应的Borrow对象
    borrow = Borrow.query.get(id)

    # 接受前端传来的json格式的数据
    data = request.get_json(force=True)

    for key, value in data.items():
        # 如果这个属性存在并且值不相等，就修改这个属性的值
        if hasattr(borrow, key) and getattr(borrow, key) != value:
            setattr(borrow, key, value)

    # 提交到数据库
    db.session.commit()

    # 响应消息
    msg = ""
    # 通过借阅
    if borrow.is_agree == 1:
        msg = f"通过了用户{borrow.user_name}在{borrow.borrow_date}借阅图书{borrow.book_name}的申请"
    # 拒绝借阅
    if borrow.is_agree == -0:
        msg = f"拒绝了用户{borrow.user_name}在{borrow.borrow_date}借阅图书{borrow.book_name}的申请"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.UPDATE_BORROW_SUCCESS.value, data=None, msg=msg).__dict__)

# 查 GET
@app.route('/borrows', methods=['GET'])
def get_all_borrows():
    # 查询所有的Borrow对象
    borrows = Borrow.query.all()

    # 将Borrow对象转换成字典格式
    json_borrows = [borrow_to_dict(borrow) for borrow in borrows]
    # 响应消息
    msg = "查询所有借阅关系成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.GET_BORROW_SUCCESS.value, data=json_borrows, msg=msg).__dict__)

@app.route('/borrows/<int:id>', methods=['GET'])
def get_borrow(id):
    # 通过id找到对应的Borrow对象
    borrow = Borrow.query.get(id)

    # 将Borrow对象转换成字典格式
    json_borrow = borrow_to_dict(borrow)
    # 响应消息
    msg = f"查询到用户{borrow.user_name}在{borrow.borrow_date}申请借阅了{borrow.book_name}"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.GET_BORROW_SUCCESS.value, data=json_borrow, msg=msg).__dict__)

if __name__ == '__main__':
    app.run()
