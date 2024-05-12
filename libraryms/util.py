from enum import Enum
from libraryms.models import Administrator, Book, Borrow, Comment, ULibrary, User, Announcement, Consult, UBorrow
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
            3 代表Announcement表
            4 代表U_Library表
            5 代表U_Borrow表
            6 代表Borrow表
            7 代表Consult表
            8 代表Comment表
            9 代表TTS
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

    # Announcement表状态码
    ADD_ANNOUNCEMENT_SUCCESS = 20031
    DELETE_ANNOUNCEMENT_SUCCESS = 20032
    UPDATE_ANNOUNCEMENT_SUCCESS = 20033
    GET_ANNOUNCEMENT_SUCCESS = 20034

    ADD_ANNOUNCEMENT_ERR = 40031
    DELETE_ANNOUNCEMENT_ERR = 40032
    UPDATE_ANNOUNCEMENT_ERR = 40033
    GET_ANNOUNCEMENT_ERR = 40034

    # U_Library表状态码
    ADD_ULibrary_SUCCESS = 20041
    DELETE_ULibrary_SUCCESS = 20042
    UPDATE_ULibrary_SUCCESS = 20043
    GET_ULibrary_SUCCESS = 20044

    ADD_ULibrary_ERR = 40041
    DELETE_ULibrary_ERR = 40042
    UPDATE_ULibrary_ERR = 40043
    GET_ULibrary_ERR = 40044

    # U_Borrow表状态码
    ADD_UBorrow_SUCCESS = 20051
    DELETE_UBorrow_SUCCESS = 20052
    UPDATE_UBorrow_SUCCESS = 20053
    GET_UBorrow_SUCCESS = 20054

    ADD_UBorrow_ERR = 40051
    DELETE_UBorrow_ERR = 40052
    UPDATE_UBorrow_ERR = 40053
    GET_UBorrow_ERR = 40054

    # Borrow表状态码
    ADD_BORROW_SUCCESS = 20061
    DELETE_BORROW_SUCCESS = 20062
    UPDATE_BORROW_SUCCESS = 20063
    GET_BORROW_SUCCESS = 20064

    ADD_BORROW_ERR = 40061
    DELETE_BORROW_ERR = 40062
    UPDATE_BORROW_ERR = 40063
    GET_BORROW_ERR = 40064

    # Consult表状态码
    ADD_CONSULT_SUCCESS = 20071
    DELETE_CONSULT_SUCCESS = 20072
    UPDATE_CONSULT_SUCCESS = 20073
    GET_CONSULT_SUCCESS = 20074

    ADD_CONSULT_ERR = 40071
    DELETE_CONSULT_ERR = 40072
    UPDATE_CONSULT_ERR = 40073
    GET_CONSULT_ERR = 40074

    # Comment 表状态码
    ADD_COMMENT_SUCCESS = 20081
    DELETE_COMMENT_SUCCESS = 20082
    UPDATE_COMMENT_SUCCESS = 20083
    GET_COMMENT_SUCCESS = 20084

    ADD_COMMENT_ERR = 40081
    DELETE_COMMENT_ERR = 40082
    UPDATE_COMMENT_ERR = 40083
    GET_COMMENT_ERR = 40084

    # Chat状态码
    GET_CHAT_RESPONSE_SUCCESS = 20094
    GET_CHAT_RESPONSE_ERR = 40094

    # TTS状态码
    ADD_TTS_SUCCESS = 200101
    GET_TTS_SUCCESS = 200104

    ADD_TTS_ERR = 400101
    GET_TTS_ERR = 400104


class AccessKey(Enum):
    API_KEY = "MD8Yqq2yYA0ox52Hu8WvpWPY"
    SECRET_KEY = "12QK4F9C6TKtwT0diqKQkylcBnypNcsZ"



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


def comment_to_dict(comment: Comment):
    return {
        'comment_id': comment.id,
        'user_id': comment.user_id,
        'user_name': comment.user_name,
        'book_id': comment.book_id,
        'content': comment.content,
        'comment_date': comment.comment_date
    }


def borrow_to_dict(borrow: Borrow):
    return {
        'id': borrow.id,
        'user_id': borrow.user_id,
        'user_name': borrow.user_name,
        'book_id': borrow.book_id,
        'book_name': borrow.book_name,
        'borrow_date': borrow.borrow_date.strftime('%Y-%m-%d') if borrow.borrow_date else None,
        'expired_date': borrow.expired_date.strftime('%Y-%m-%d') if borrow.expired_date else None,
        'is_return': borrow.is_return,
        'is_agree': borrow.is_agree
    }


def comment_to_dict(comment: Comment):
    return {
        'id': comment.id,
        'user_id': comment.user_id,
        'user_name': comment.user_name,
        'book_id': comment.book_id,
        'content': comment.content,
        'comment_date': comment.comment_date.strftime('%Y-%m-%d') if comment.comment_date else None
    }


def u_library_to_dict(u_library: U_Library):
    return {
        'id': u_library.id,
        'user_id': u_library.user_id,
        'book_name': u_library.book_name,
        'author': u_library.author,
        'category': u_library.category,
        'press': u_library.press,
        'introduction': u_library.introduction
    }


def u_borrow_to_dict(u_borrow: UBorrow):
    return {
        'id': u_borrow.id,
        'borrow_id': u_borrow.borrower_id,
        'lender_id': u_borrow.lender_id,
        'book_id': u_borrow.book_id,
        'book_name': u_borrow.book_name,
        'borrow_date': u_borrow.borrow_date,
        'is_agree': u_borrow.is_agree,
        'is_return': u_borrow.is_return
    }


def announcement_to_dict(announcement: Announcement):
    return {
        'id': announcement.id,
        'title': announcement.title,
        'content': announcement.content,
        'publish_time': announcement.publish_time.strftime('%Y-%m-%d %H:%M:%S') if announcement.publish_time else None
    }


def consult_to_dict(consult: Consult):
    return {
        'id': consult.id,
        'user_id': consult.user_id,
        'user_name': consult.user_name,
        'title': consult.title,
        'content': consult.content,
        'consult_time': consult.consult_time.strftime('%Y-%m-%d %H:%M:%S') if consult.consult_time else None
    }
