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
            ...(待补充)
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


def book_to_dict(book: Book):
    return {
            'book_name': book.book_name,
            'author': book.author,
            'category': book.category,
            'press': book.press,
            'introduction': book.introduction,
            'stars': book.stars,
            'number': book.number,
            'cover': book.cover
        }