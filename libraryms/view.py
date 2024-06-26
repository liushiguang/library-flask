from flask import Flask, request, jsonify, render_template
from datetime import datetime
from libraryms import app, db
from libraryms.models import Administrator, Book, Borrow, Comment, ULibrary, User, TTS_Info
from libraryms.tts_util.tts_info import tts_info
from libraryms.tts_util.util_for_tts import Ws_Param, on_open, on_message, on_error, on_close, pcm_to_wav
from libraryms.util import APIResponse, ResposeCode, book_to_dict, user_to_dict, comment_to_dict, AccessKey, \
    u_library_to_dict, announcement_to_dict
from libraryms.models import Administrator, Book, Borrow, Comment, ULibrary, User, UBorrow, Announcement, Consult
from libraryms.util import APIResponse, ResposeCode, book_to_dict, user_to_dict, borrow_to_dict
import json
import requests
from flask import send_file
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os
import wave
# from  tts_util.util_for_tts import on_open, Ws_Param, on_message, on_error, on_close, pcm_to_wav

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
    msg = f"添加图书《{new_book.book_name}》成功！"

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
    msg = f"删除图书《{book.book_name}》成功！"

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
    msg = f"修改图书《{book.book_name}》成功！"

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
    msg = f"查询图书《{book.book_name}》成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.GET_BOOK_SUCCESS.value, data=json_book, msg=msg).__dict__)


# 通过类别查询图书
@app.route('/books/category/<string:category>', methods=['GET'])
def get_book_by_category(category):
    # （get通过主键查询）这里根据属性值查询
    books = Book.query.filter_by(category=category).all()
    json_book = [book_to_dict(book) for book in books]
    msg = f"查询图书种类成功！"
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
    # TODO 头像

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
    Comment 模块
    增:
        POST /comments
    删:
        DELETE /comments/id
    改:
        PUT /comments/id
    查:
        GET /comments/book_id
'''


@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json(force=True)
    new_comment = Comment(**data)
    db.session.add(new_comment)
    db.session.commit()
    msg = f"发布评论{new_comment.comment_id}成功"

    return jsonify(APIResponse(ResposeCode.ADD_COMMENT_SUCCESS.value, data=None, msg=msg).__dict__)


@app.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    # 通过id找到对应的Comment对象
    comment = Comment.query.get(id)
    # 删除这个对象,并提交到数据库
    db.session.delete(comment)
    db.session.commit()

    # 响应消息
    msg = f"删除评论{comment.id}成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.DELETE_COMMENT_SUCCESS.value, data=None, msg=msg).__dict__)


@app.route('/comments/<int:id>', methods=['PUT'])
def update_comment(id):
    # 通过id找到对应的Comment对象
    comment = Comment.query.get(id)

    # 接受前端传来的json格式的数据
    data = request.get_json(force=True)

    for key, value in data.items():
        # 如果这个属性存在并且值不相等，就修改这个属性的值
        if hasattr(comment, key) and getattr(comment, key) != value:
            setattr(comment, key, value)

    # 提交到数据库
    db.session.commit()

    # 响应消息
    msg = f"修改图书{comment.id}成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.UPDATE_COMMENT_SUCCESS.value, data=None, msg=msg).__dict__)


@app.route('/comments/<int:book_id>', methods=['GET'])
def get_all_comments_by_book_id(book_id):
    comments = Comment.query.filter_by(book_id=book_id).all()
    json_comments = [comment_to_dict(comment) for comment in comments]
    msg = "获取所有评论成功！"
    return jsonify(APIResponse(ResposeCode.GET_COMMENT_SUCCESS.value, data=json_comments, msg=msg).__dict__)


'''
    附加CommentInfo 模块
    这里使用的code和comment一样
    查:
        GET /commentInfo/book_id
'''


@app.route('/commentInfo/<int:book_id>', methods=['GET'])
def get_all_comment_info_by_book_id(book_id):
    comments = Comment.query.filter_by(book_id=book_id).all()
    json_comments = [comment_to_dict(comment) for comment in comments]
    # 获取用户姓名，评论内容、时间列表和user_id
    user_names = [comment['user_name'] for comment in json_comments]
    contents = [comment['content'] for comment in json_comments]
    times = [comment['comment_date'] for comment in json_comments]
    comment_users = [comment['user_id'] for comment in json_comments]
    # 用户头像列表
    comment_user_covers = []
    for user_id in comment_users:
        user = User.query.get(user_id)
        json_user = user_to_dict(user)
        print(json_user)
        comment_user_covers.append(json_user['cover'])

    # 所有列表合并起来并转化为json格式
    merged_data = [
        {'user_cover': comment_user_cover, 'user_name': user_name, 'content': content, 'comment_date': str(time)} for
        comment_user_cover, user_name, content, time
        in zip(comment_user_covers, user_names, contents, times)]

    # json_data = json.dumps(merged_data)

    msg = "获取所有评论成功！"

    # 注意，这里返回的就是dict字典数据，这样在前端可以直接使用data.map作为数组遍历获取数据
    # 不要转为json格式
    print(merged_data)

    return jsonify(APIResponse(ResposeCode.GET_COMMENT_SUCCESS.value, data=merged_data, msg=msg).__dict__)

'''
    大模型ERNIE-4.0-8K-Preview调用
'''


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=MD8Yqq2yYA0ox52Hu8WvpWPY&client_secret=12QK4F9C6TKtwT0diqKQkylcBnypNcsZ"
    # grant_type = "client_credentials"
    # base_url = "https://aip.baidubce.com/oauth/2.0/token"
    #
    # url = f"{base_url}?grant_type={grant_type}&client_id={AccessKey.API_KEY}&client_secret={AccessKey.SECRET_KEY}"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


@app.route('/chat/<string:ask_content>', methods=['GET'])
def get_chat_response(ask_content):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-8k-preview?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": ask_content
            }
        ]
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # 将响应体内容转化为字典
    chat_data = response.json()
    # 打印回复内容
    chat_data = [chat_data]
    print(chat_data)
    msg = "获取回复成功"
    return jsonify(APIResponse(ResposeCode.GET_CHAT_RESPONSE_SUCCESS.value, data=chat_data, msg=msg).__dict__)



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


# 取消某个借书申请
@app.route('/borrows/<int:id>', methods=['DELETE'])
def delete_borrows(id):
    try:
        # 查询是否存在对应的借阅记录
        borrow = Borrow.query.get(id)
        if not borrow:
            return jsonify(APIResponse(ResposeCode.DELETE_BORROW_ERR.value, data="", msg='未发现该图书').__dict__)

        db.session.delete(borrow)  # 从数据库中删除借阅记录
        db.session.commit()

        return jsonify(APIResponse(ResposeCode.DELETE_BORROW_SUCCESS.value, data="",
                                   msg='取消申请成功').__dict__)
    except Exception as e:
        return jsonify(
            APIResponse(ResposeCode.DELETE_BORROW_ERR.value, data="", msg='error').__dict__)


# 还特定书籍与同意借阅特定书籍
@app.route('/borrows/<int:id>', methods=['PUT'])
def update_borrow(id):
    # 查询是否存在对应的借阅记录
    borrow = Borrow.query.get(id)
    if not borrow:
        return jsonify(APIResponse(ResposeCode.UPDATE_BORROW_SUCCESS.value, data="", msg='未发现记录').__dict__)

    # WARNING 你这样写代码把我的路全部堵死了
    # 将对应的借阅记录的 is_return 字段设置为 1
    # borrow.is_return = 1
    # db.session.commit()

    # 接受前端传来的json格式的数据
    data = request.get_json(force=True)

    # 响应消息
    msg = ""

    print(borrow.is_agree, data["is_agree"], borrow.is_return, data["is_return"])
    # 判断是处理借阅申请还是归还申请
    if borrow.is_agree != data["is_agree"]:
        if data["is_agree"] == 1:
            msg = f"通过了用户{borrow.user_name}在{borrow.borrow_date}借阅图书《{borrow.book_name}》的申请"
        # 拒绝借阅
        if data["is_agree"] == -1:
            msg = f"拒绝了用户{borrow.user_name}在{borrow.borrow_date}借阅图书《{borrow.book_name}》的申请"

    elif borrow.is_return != data["is_return"]:
        if data["is_return"] == 1:
            msg = f"用户{borrow.user_name}在{borrow.borrow_date}归还了图书《{borrow.book_name}》"

    for key, value in data.items():
        # 如果这个属性存在并且值不相等，就修改这个属性的值
        if hasattr(borrow, key) and getattr(borrow, key) != value:
            setattr(borrow, key, value)

    # 提交到数据库
    db.session.commit()

    print(msg)
    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.UPDATE_BORROW_SUCCESS.value, data=None, msg=msg).__dict__)


# 查 GET
@app.route('/borrows', methods=['GET'])
def get_all_borrows():
    # 查询所有的Borrow对象
    borrows = Borrow.query.all()

    # 将Borrow对象转换成字典格式
    json_borrows = [borrow_to_dict(borrow) for borrow in borrows]

    print(json_borrows[0])

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

    print(json_borrow)

    # 响应消息
    msg = f"查询到用户{borrow.user_name}在{borrow.borrow_date}申请借阅了{borrow.book_name}"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.GET_BORROW_SUCCESS.value, data=json_borrow, msg=msg).__dict__)


# 获取指定用户借阅的书籍
@app.route('/userBorrow/<int:user_id>', methods=['GET'])
def get_user_borrow(user_id):
    borrows = Borrow.query.filter_by(user_id).all()
    json_borrows = [borrow_to_dict(borrow) for borrow in borrows]
    msg = f"查询用户借阅书籍成功"
    return jsonify(APIResponse(ResposeCode.GET_BORROW_SUCCESS.value, data=json_borrows, msg=msg).__dict__)


'''
    Announcement 模块
    增:
        POST /announcements
    删:
        DELETE /announcements/id
    改:
        PUT /announcements/id
    查:
        GET /announcements
            /announcements/id
'''


# 增 POST
@app.route('/announcements', methods=['POST'])
def add_announcement():
    # 接受前端传来的json格式的数据
    data = request.get_json(force=True)
    # 创建一个新的Announcement对象
    new_announcement = Announcement(**data)
    # 添加到数据库
    db.session.add(new_announcement)
    db.session.commit()

    # 响应消息
    msg = f"发布公告\"{new_announcement.title}\"成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.ADD_ANNOUNCEMENT_SUCCESS.value, data=None, msg=msg).__dict__)


# 删 DELETE
@app.route('/announcements/<int:id>', methods=['DELETE'])
def delete_announcement(id):
    # 通过id找到对应的Announcement对象
    announcement = Announcement.query.get(id)
    # 删除这个对象,并提交到数据库
    db.session.delete(announcement)
    db.session.commit()

    # 响应消息
    msg = f"删除公告\"{announcement.title}\"成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.DELETE_ANNOUNCEMENT_SUCCESS.value, data=None, msg=msg).__dict__)


# 改 PUT
@app.route('/announcements/<int:id>', methods=['PUT'])
def update_announcement(id):
    # 通过id找到对应的Announcement对象
    announcement = Announcement.query.get(id)

    # 接受前端传来的json格式的数据
    data = request.get_json(force=True)

    for key, value in data.items():
        # 如果这个属性存在并且值不相等，就修改这个属性的值
        if hasattr(announcement, key) and getattr(announcement, key) != value:
            setattr(announcement, key, value)

    # 提交到数据库
    db.session.commit()

    # 响应消息
    msg = f"修改公告\"{announcement.title}\"成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.UPDATE_ANNOUNCEMENT_SUCCESS.value, data=None, msg=msg).__dict__)


# 查 GET
@app.route('/announcements', methods=['GET'])
def get_all_announcements():
    # 查询所有的Announcement对象
    announcements = Announcement.query.all()

    # 将Announcement对象转换成字典格式
    json_announcements = [announcement_to_dict(announcement) for announcement in announcements]
    # 响应消息
    msg = "查询所有公告成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.GET_ANNOUNCEMENT_SUCCESS.value, data=json_announcements, msg=msg).__dict__)


@app.route('/announcements/<int:id>', methods=['GET'])
def get_announcement(id):
    # 通过id找到对应的Announcement对象
    announcement = Announcement.query.get(id)

    # 将Announcement对象转换成字典格式
    json_announcement = announcement_to_dict(announcement)
    # 响应消息
    msg = f"查询公告\"{announcement.title}\"成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.GET_ANNOUNCEMENT_SUCCESS.value, data=json_announcement, msg=msg).__dict__)

'''
    Restful API设计
    Administrator 模块
    登录
        POST /administrators
'''
@app.route('/administrators/account', methods=['POST'])
def administrator_login_by_account():
    # 获取前端发送来json格式的数据
    data = request.get_json(force=True)
    # 创建一个新的Administrator对象
    administrator = Administrator(**data)
    # 查询数据库中是否存在对应的管理员
    exist = Administrator.query.filter_by(admin_account=administrator.admin_account).first()

    # 响应消息 与 状态码
    msg = ''
    code = ''
    # 如果不存在对应的管理员，返回错误信息
    if not exist:
        msg = f"账号{administrator.admin_account}不存在！"
        code = ResposeCode.ADD_ADMINISTRATOR_ERR.value
    else:
        # 如果存在对应的管理员，判断密码是否正确
        if exist.admin_password == administrator.admin_password:
            msg = f"登录成功！"
            code = ResposeCode.ADD_ADMINISTRATOR_SUCCESS.value
        else:
            msg = f"账号{exist.admin_account}密码错误！"
            code = ResposeCode.ADD_ADMINISTRATOR_ERR.value

    return jsonify(APIResponse(code=code, data=None, msg=msg).__dict__)

# ——————————————————————————————————————————————————————————————————
# 登录+个人中心+个人图书城+信息专栏API部分
@app.route('/login', methods=['POST'])
def login_by_account():
    # 获取前端发送过来的账号和密码信息us
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


# 查个人借阅信息
@app.route('/borrowsForUser/<int:user_id>', methods=['GET'])
def get_borrows_user(user_id):
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
            'is_agree': borrow.is_agree
        }
        borrow_data.append(borrow_info)

    return jsonify(APIResponse(ResposeCode.GET_BORROW_SUCCESS.value, data=borrow_data, msg='success').__dict__)


# 还书
@app.route('/borrowsForUser/<int:id>', methods=['PUT'])
def return_borrows_user(id):
    # 查询 Borrow 表格，找到符合条件的第一个记录
    borrow_to_return = Borrow.query.filter_by(id=id, is_agree=1, is_return=0).first()

    if borrow_to_return:
        # 更新符合条件的记录的 is_return 字段为 1
        borrow_to_return.is_return = 1
        # 提交事务
        db.session.commit()

        return jsonify(APIResponse(ResposeCode.UPDATE_BORROW_SUCCESS.value, data="", msg='success').__dict__)
    else:
        return jsonify(APIResponse(ResposeCode.UPDATE_BORROW_ERR.value, data="", msg='error').__dict__)


# 取消借阅申请
@app.route('/borrowsForUser/<int:id>', methods=['DELETE'])
def delete_borrows_user(id):
    # 查询要删除的 Borrow 记录
    borrow_to_delete = Borrow.query.get(id)

    if borrow_to_delete:
        db.session.delete(borrow_to_delete)
        db.session.commit()

        return jsonify(APIResponse(ResposeCode.DELETE_BORROW_SUCCESS.value, data="", msg='success').__dict__)
    else:
        return jsonify(APIResponse(ResposeCode.DELETE_BORROW_ERR.value, data="", msg='error').__dict__)


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
                'user_name': borrower_name,
                'book_name': ask.book_name,
                'time': ask.borrow_date.strftime('%Y-%m-%d')  # 将日期格式化为字符串
            }

            ask_list.append(ask_info)

        # 将列表转换为JSON格式并返回给前端
        return jsonify(APIResponse(ResposeCode.GET_UBorrow_SUCCESS.value, data=ask_list, msg='success').__dict__)
    else:
        # 如果没有找到相关的借书请求，返回空列表给前端
        return jsonify(APIResponse(ResposeCode.GET_UBorrow_ERR.value, data='', msg='error').__dict__)


# 同意他人借阅自己的图书
@app.route('/asksAgree/<int:id>', methods=['POST'])
def agree_asks(id):
    borrow_request = UBorrow.query.get_or_404(id)  # 获取特定 ID 的借书请求记录
    borrow_request.is_agree = 1  # 将 is_agree 设置为 1，表示已同意
    db.session.commit()  # 提交更改到数据库
    return jsonify(APIResponse(ResposeCode.UPDATE_UBorrow_SUCCESS.value, data='', msg='success').__dict__)


# 拒绝
@app.route('/asksRefuse/<int:id>', methods=['POST'])
def refuse_asks(id):
    borrow_request = UBorrow.query.get_or_404(id)  # 获取特定 ID 的借书请求记录
    borrow_request.is_agree = -1  # 将 is_agree 设置为 1，表示已同意
    db.session.commit()  # 提交更改到数据库
    return jsonify(APIResponse(ResposeCode.UPDATE_UBorrow_SUCCESS.value, data='', msg='success').__dict__)


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

        return jsonify(APIResponse(ResposeCode.GET_BORROW_SUCCESS.value, data=borrow_data, msg='success').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.GET_BORROW_SUCCESS.value, data="", msg='error').__dict__)


# 删除借书记录
@app.route('/borrowsHistory/<int:id>', methods=['DELETE'])
def delete_borrows_history(id):
    try:
        # 查询是否存在对应的借阅记录
        borrow = Borrow.query.get(id)
        if not borrow:
            return jsonify(APIResponse(ResposeCode.DELETE_BORROW_SUCCESS.value, data="", msg='未发现记录').__dict__)

        # 删除记录
        db.session.delete(borrow)
        db.session.commit()

        return jsonify(APIResponse(ResposeCode.DELETE_BORROW_SUCCESS.value, data="",
                                   msg='删除成功！').__dict__)
    except Exception as e:
        return jsonify(
            APIResponse(ResposeCode.DELETE_BORROW_ERR.value, data="", msg='error').__dict__)


# 获取所有个人图书馆资源
@app.route('/myResources', methods=['GET'])
def get_all_resources():
    personal_books = ULibrary.query.all()
    json_personal_books = [u_library_to_dict(book) for book in personal_books]
    msg = f"查询所有个人图书馆资源成功！"
    return jsonify(APIResponse(ResposeCode.GET_ULibrary_SUCCESS.value, data=json_personal_books, msg=msg).__dict__)


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
                'book_name': book.book_name,
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

        # 查询UBorrow表中对应book_id且is_agree为0的记录
        u_borrow_records = UBorrow.query.filter_by(book_id=id, is_agree=0).all()
        # 将这些记录的状态置为-1,即为拒绝
        for record in u_borrow_records:
            record.is_return = -1

        db.session.commit()
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
            UBorrow.is_agree,
            UBorrow.lender_id
        ).all()
        # 封装数据
        borrow_data = []
        for borrow in borrow_info:
            lender_name = User.query.filter_by(user_id=borrow.lender_id).first().user_name
            borrow_info = {
                'id': borrow.id,
                'book_id': borrow.book_id,
                'book_name': borrow.book_name,
                'borrow_date': borrow.borrow_date.strftime('%Y-%m-%d'),
                'is_agree': borrow.is_agree,
                'lender_name': lender_name
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
# @app.route('/announcements', methods=['GET'])
# def get_announcements():
#     try:
#         # 查询所有公告，并按照时间排序
#         announcements = Announcement.query.order_by(Announcement.publish_time.desc()).all()
#         # 封装数据
#         announcement_data = []
#         for announcement in announcements:
#             announcement_info = {
#                 'id': announcement.id,
#                 'title': announcement.title,
#                 'content': announcement.content,
#                 'publish_time': announcement.publish_time.strftime('%Y-%m-%d'),
#             }
#             announcement_data.append(announcement_info)
#
#         return jsonify(
#             APIResponse(ResposeCode.GET_ANNOUNCEMENT_SUCCESS.value, data=announcement_data, msg='success').__dict__)
#     except Exception as e:
#         return jsonify(APIResponse(ResposeCode.GET_ANNOUNCEMENT_ERR.value, data="", msg='error').__dict__)


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
            consult_time=datetime.now()  # 记录当前时间
        )
        db.session.add(new_consult)
        db.session.commit()

        return jsonify(APIResponse(ResposeCode.ADD_CONSULT_SUCCESS.value, data="", msg='success').__dict__)
    except Exception as e:
        return jsonify(APIResponse(ResposeCode.ADD_CONSULT_ERR.value, data="", msg='error').__dict__)


# ——————————————————————————————————————————————————————————————————


@app.route('/uBorrow', methods=['POST'])
def add_u_borrow():
    data = request.get_json(force=True)
    new_u_borrow = UBorrow(**data)
    db.session.add(new_u_borrow)
    db.session.commit()
    msg = f"用户{new_u_borrow.borrower_id}向{new_u_borrow.lender_id}在{new_u_borrow.borrow_date}申请借阅了{new_u_borrow.book_name}"
    return jsonify(APIResponse(ResposeCode.ADD_UBorrow_SUCCESS.value, data=data, msg=msg).__dict__)


# 返回保存在服务器上面的音频文件url
@app.route('/audio/wav/<filename>')
def get_audio(filename):
    # 确定保存文件的目录
    save_dir = 'tts_audio/wav'
    # 返回保存在服务器上的音频文件
    return send_file(os.path.join(save_dir, filename), as_attachment=True)



# tts文字转语音请求
@app.route('/audio', methods=["POST"])
def handle_tts():
    data = request.get_json(force=True)
    tts_data = TTS_Info(**data)
    book_name = tts_data.book_name
    wsParam = Ws_Param(APPID='3d152a69', APISecret='MWRjM2M5ODY4ZWNmYTIzYjI0MWYyMzQ0',
                       APIKey='287a5996f08773bfdc57ef33d55de798',
                       Text=tts_data.text)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=lambda ws, message: on_message(ws, message, book_name), on_error=on_error, on_close=on_close)
    ws.on_open = lambda ws: on_open(ws, wsParam, book_name)  # 在这里调用 on_open 函数
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    # 输出路径
    current_pcm_directory = './tts_audio/pcm'
    current_wav_directory = './tts_audio/wav'
    filename = tts_data.book_name
    pcm_extension = '.pcm'
    wav_extension = '.wav'
    input_pcm_file = os.path.join(current_pcm_directory, filename + pcm_extension)
    output_wav_file = os.path.join(current_wav_directory, filename + wav_extension)

    # 转换为wav文件
    pcm_to_wav(input_pcm_file=input_pcm_file, output_wav_file=output_wav_file)
    msg = f"转换成功"
    return jsonify(APIResponse(ResposeCode.ADD_TTS_SUCCESS.value, data=None, msg=msg).__dict__)


if __name__ == '__main__':
    app.run()
