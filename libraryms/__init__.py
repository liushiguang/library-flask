from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from libraryms.setting import BaseConfig

app=Flask('libraryms',template_folder="../templates",static_folder="../static")

# 解决跨域问题，允许所有域名访问
CORS(app, resources=r'/*')

# 从配置文件中读取配置
app.config.from_object(BaseConfig)

# 数据库配置
db = SQLAlchemy(app)