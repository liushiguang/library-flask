class BaseConfig(object):

    dialct = 'mysql'
    driver = 'pymysql'
    host = 'rm-cn-36z3o5awf000cd8o.rwlb.rds.aliyuncs.com'
    port = '3306'
    user = 'root'
    password = 'Jjhbpd_2022'
    database = 'librarydbms'

    SQLALCHEMY_DATABASE_URI= f'{dialct}+{driver}://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False