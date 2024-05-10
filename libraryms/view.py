from flask import Flask, request, jsonify, render_template
from libraryms import app, db
from libraryms.models import Administrator, Book, Borrow, Comment, ULibrary, User
from libraryms.util import APIResponse, ResposeCode, book_to_dict, user_to_dict, comment_to_dict, AccessKey
import json
import requests

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
    # url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=[api key]&client_secret=[应用Secret Key]"
    grant_type = "client_credentials"
    base_url = "https://aip.baidubce.com/oauth/2.0/token"

    url = f"{base_url}?grant_type={grant_type}&client_id={AccessKey.API_KEY}&client_secret={AccessKey.SECRET_KEY}"

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
    print(response.text)
    msg = "获取回复成功"
    return jsonify(APIResponse(ResposeCode.GET_CHAT_RESPONSE_SUCCESS.value, data=chat_data, msg=msg).__dict__)


if __name__ == '__main__':
    app.run()
