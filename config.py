import os


class Development(object):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('BASE_WEB_USER')}:" \
                              f"{os.getenv('BASE_WEB_PASS')}@{os.getenv('BASE_WEB_HOST')}/{os.getenv('BASE_WEB_BASE')}"

    SQLALCHEMY_BINDS = {
        "web": f"mysql+pymysql://{os.getenv('BASE_WEB_USER')}:"
               f"{os.getenv('BASE_WEB_PASS')}@{os.getenv('BASE_WEB_HOST')}/{os.getenv('BASE_WEB_BASE')}",

        "bukkit": f"mysql+pymysql://{os.getenv('BASE_BUKKIT_USER')}:"
                  f"{os.getenv('BASE_BUKKIT_PASS')}@{os.getenv('BASE_BUKKIT_HOST')}/{os.getenv('BASE_BUKKIT_BASE')}",
    }

    REDIS_URL = f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0?db=0"
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = os.getenv("SECRET_KEY", None)
    FLASK_SECRET = os.getenv("FLASK_SECRET", None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_SIZE = 50
    SQLALCHEMY_POOL_TIMEOUT = 200
    SQLALCHEMY_MAX_OVERFLOW = 50
    RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_SECRET_CODE')
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_CODE')
    DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
    DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
    VK_CLIENT_ID = os.getenv('VK_CLIENT_ID')
    VK_CLIENT_SECRET = os.getenv('VK_CLIENT_SECRET')


class Production(Development):
    DEVELOPMENT = False
    DEBUG = False
    SERVER_NAME = os.getenv("SERVER_NAME", "localhost")
