from flask import Flask, request, jsonify, render_template
from libraryms import app, db
from libraryms.models import Administrator, Book, Borrow, Comment, ULibrary, User
import json

# MainPage
@app.route('/')
def index():
    return render_template('index.html')

# 404 Not Found Page
@app.errorhandler(404)  # 传入错误码作为参数状态
def error_date(error):  # 接受错误作为参数
    return render_template("404.html"), 404  # 返回对应的http状态码，和返回404错误的html文件


# Restful API设计
'''
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
    data = request.get_json()
    return data

# 删 DELETE
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    return 'delete book %s' % id

# 改 POST
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    return 'update book %s' % id

# 查 GET
@app.route('/books', methods=['GET'])
def get_all_books():
    return 'get books'

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    return 'get book %s' % id

if __name__ == '__main__':
    app.run()
