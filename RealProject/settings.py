from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent  # 项目根目录
# 这里的__file__是settings.py文件的路径，resolve()方法返回一个绝对路径，parent.parent表示上两级目录
    #数据库连接
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:020121@localhost:3306/ai_mianshi'

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.urandom(24)  # 用于会话加密的密钥

SQLALCHEMY_COMMIT_ON_TEARDOWN = False