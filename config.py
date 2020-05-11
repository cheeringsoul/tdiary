import os
from datetime import timedelta
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'tdiary': {
        'class': "logging.handlers.RotatingFileHandler",
        'filename': 'tdiary.log',
        'maxBytes': 1023*3,
        'backupCount': 5,
        'mode': 'w',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['tdiary']
    }
})

#
# class FlaskAppConfigMeta(type):
#     def __new__(mcs, name, bases, attrs):
#         config = super().__new__(mcs, name, bases, attrs)
#         if not os.getenv('SECRET_KEY'):
#             raise Exception('SECRET_KEY环境变量必须设置')
#         config.SECRET_KEY = os.environ['SECRET_KEY']
#         return config
#
#
# class FlaskAppConfig(metaclass=FlaskAppConfigMeta):
#     PERMANENT_SESSION_LIFETIME = timedelta(days=7)
#     ALLOW_IMAGE_TYPE = {'png', 'jpg', 'jpeg', 'heic', 'webp',
#                         'gif', 'avif', 'bmp', 'tiff', 'PGM', 'PPM'}
#
#
# class FlaskAppProductionConfig(FlaskAppConfig):
#     DEBUG = False
#     IMG_PREFIX = '/images/_data/'
#     UPLOAD_FOLDER = '/app/files'
#
#
# class FlaskAppDevelopmentConfig(FlaskAppConfig):
#     DEBUG = True
#     IMG_PREFIX = '/images/_data/'
#     UPLOAD_FOLDER = '/app/files'
#
#
# class MySQLConfig(object):
#     def __init__(self):
#         # 工单系统数据库配置
#         if not os.getenv('DB_USER'):
#             raise Exception('DB_USER环境变量必须设置')
#         self.db_user = os.environ['DB_USER']
#
#         if not os.getenv('DB_PASSWORD'):
#             raise Exception('DB_PASSWORD环境变量必须设置')
#         self.db_password = os.environ['DB_PASSWORD']
#
#         if not os.getenv('DB_HOST'):
#             raise Exception('DB_HOST环境变量必须设置')
#         self.db_host = os.environ['DB_HOST']
#
#         if not os.getenv('DB_PORT'):
#             raise Exception('DB_PORT环境变量必须设置')
#         self.db_port = os.environ['DB_PORT']
#
#         if not os.getenv('DB_NAME'):
#             raise Exception('DB_NAME环境变量必须设置')
#         self.db_name = os.environ['DB_NAME']
#
#     @property
#     def ticket_db_uri(self):
#         return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4&binary_prefix=true"
#
#
# db_uri = MySQLConfig().ticket_db_uri
