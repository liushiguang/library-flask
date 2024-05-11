from enum import Enum
from libraryms.models import Administrator, Book, Borrow, Comment, U_Library, User, U_Borrow, Annocement, Consult
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
            3 代表Borrow表
            4 Announcement表
            5 Consult表
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

    # Borrow表状态码
    ADD_BORROW_SUCCESS = 20031
    DELETE_BORROW_SUCCESS = 20032
    UPDATE_BORROW_SUCCESS = 20033
    GET_BORROW_SUCCESS = 20034

    ADD_BORROW_ERR = 40031
    DELETE_BORROW_ERR = 40032
    UPDATE_BORROW_ERR = 40033
    GET_BORROW_ERR = 40034

    # Announcement表状态码
    ADD_ANNOUNCEMENT_SUCCESS = 20041
    DELETE_ANNOUNCEMENT_SUCCESS = 20042
    UPDATE_ANNOUNCEMENT_SUCCESS = 20043
    GET_ANNOUNCEMENT_SUCCESS = 20044

    ADD_ANNOUNCEMENT_ERR = 40041
    DELETE_ANNOUNCEMENT_ERR = 40042
    UPDATE_ANNOUNCEMENT_ERR = 40043
    GET_ANNOUNCEMENT_ERR = 40044

    # Consult表状态码
    ADD_CONSULT_SUCCESS = 20051
    DELETE_CONSULT_SUCCESS = 20052
    UPDATE_CONSULT_SUCCESS = 20053
    GET_CONSULT_SUCCESS = 20054

    ADD_CONSULT_ERR = 40051
    DELETE_CONSULT_ERR = 40052
    UPDATE_CONSULT_ERR = 40053
    GET_CONSULT_ERR = 40054

def book_to_dict(book: Book):
    return {
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
            'user_id': user.user_id,
            'user_account': user.user_account,
            'user_name': user.user_name,
            'user_password': user.user_password,
            'gender': user.gender,
            'phone': user.phone,
            'email': user.email,
            'profile': user.profile,
            'cover': user.cover
        }

def borrow_to_dict(borrow: Borrow):
    return {
            'id': borrow.id,
            'user_id': borrow.user_id,
            'user_name': borrow.user_name,
            'book_id': borrow.book_id,
            'book_name': borrow.book_name,
            'borrow_date': borrow.borrow_date,
            'expired_date': borrow.expired_date,
            'is_return': borrow.is_return
        }

def consult_to_dict(consult: Consult):
    return {
            'id': consult.id,
            'user_id': consult.user_id,
            'user_name': consult.user_name,
            'title': consult.title,
            'content': consult.content,
            'consult_time': consult.consult_time,
        }

def annocement_to_dict(annocement: Annocement):
    return {
            'id': annocement.id,
            'title': annocement.title,
            'content': annocement.content,
            'publish_time': annocement.publish_time
        }
