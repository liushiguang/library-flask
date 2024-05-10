from flask import Flask, request, jsonify, render_template
from libraryms import app, db
from libraryms.models import Administrator, Book, Borrow, Comment, ULibrary, User
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


if __name__ == '__main__':
    app.run()
