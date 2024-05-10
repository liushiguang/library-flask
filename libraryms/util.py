from enum import Enum
from libraryms.models import Administrator, Book, Borrow, Comment, ULibrary, User
# 定义返回数据的规范类
class APIResponse:
    def __init__(self, code, data=None, msg=None):
        self.code = code
        self.data = data
        self.msg = msg

class ResposeCode(Enum):
    '''
        状态码中200 400 代表成功与否 第四位代表
        第四位代表对不同的表进行操作
            1 代表Book表
            2 代表User表
            3 代表Comment表
        第五位代表操作的类型
            1 代表增
            2 代表删
            3 代表改
            4 代表查
    '''

    # Book表状态码
    ADD_BOOK_SUCCESS = 20011
    DELETE_BOOK_SUCCESS = 20012
    UPDATE_BOOK_SUCCESS = 20013
    GET_BOOK_SUCCESS = 20014

    ADD_BOOK_ERR = 40011
    DELETE_BOOK_ERR = 40012
    UPDATE_BOOK_ERR = 40013
    GET_BOOK_ERR = 40014

    # User表状态码
    ADD_USER_SUCCESS = 20021
    DELETE_USER_SUCCESS = 20022
    UPDATE_USER_SUCCESS = 20023
    GET_USER_SUCCESS = 20024

    ADD_USER_ERR = 40021
    DELETE_USER_ERR = 40022
    UPDATE_USER_ERR = 40023
    GET_USER_ERR = 40024

    # Comment 表状态码
    ADD_COMMENT_SUCCESS = 20031
    DELETE_COMMENT_SUCCESS = 20032
    UPDATE_COMMENT_SUCCESS = 20033
    GET_COMMENT_SUCCESS = 20034

    ADD_COMMENT_ERR = 40031
    DELETE_COMMENT_ERR = 40032
    UPDATE_COMMENT_ERR = 40033
    GET_COMMENT_ERR = 40034

    # Chat状态码
    GET_CHAT_RESPONSE_SUCCESS = 20094
    GET_CHAT_RESPONSE_ERR = 40094

class AccessKey(Enum):
    API_KEY = "MD8Yqq2yYA0ox52Hu8WvpWPY"
    SECRET_KEY = "12QK4F9C6TKtwT0diqKQkylcBnypNcsZ"



def book_to_dict(book: Book):
    return {
            # 增加id
            'book_id': book.book_id,
            'book_name': book.book_name,
            'author': book.author,
            'category': book.category,
            'press': book.press,
            'introduction': book.introduction,
            'stars': book.stars,
            'number': book.number,
            'cover': book.cover
        }


def user_to_dict(user: User):
    return {
            'user_account': user.user_account,
            'user_name': user.user_name,
            'user_password': user.user_password,
            'gender': user.gender,
            'phone': user.phone,
            'email': user.email,
            'profile': user.profile,
            'cover': user.cover
        }


def comment_to_dict(comment: Comment):
    return {
        'comment_id': comment.id,
        'user_id': comment.user_id,
        'user_name': comment.user_name,
        'book_id': comment.book_id,
        'content': comment.content,
        'comment_date': comment.comment_date
    }
