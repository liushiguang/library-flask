from flask import Flask, request, jsonify, render_template
from libraryms import app, db
from libraryms.models import Administrator, Book, Borrow, Comment, ULibrary, User
from libraryms.util import APIResponse, ResposeCode, book_to_dict
import json

# 处理异常操作
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

    db.session.commit()

    # 响应消息
    msg = f"修改图书{book.book_name}成功！"

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.UPDATE_BOOK_SUCCESS.value, data=None, msg=msg).__dict__)

# 查 GET
@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()



    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return 'get books'

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)

    json_book = book_to_dict(book)

    # 将返回结果封装成APIResponse对象，然后转换成json格式返回给前端
    return jsonify(APIResponse(ResposeCode.GET_BOOK_SUCCESS.value, data=json_book, msg=None).__dict__)

if __name__ == '__main__':
    app.run()
