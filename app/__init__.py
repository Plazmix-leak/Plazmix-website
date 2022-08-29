from dotenv import load_dotenv
from sentry_sdk import capture_exception
from werkzeug.exceptions import HTTPException

from .helper.simple_page import ErrorPage, PageButton

load_dotenv()

import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask, g, request
from celery import Celery

from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from flask_redis import FlaskRedis
from flask_migrate import Migrate
from app.helper.retrying_query import RetryingQuery

db = SQLAlchemy(query_class=RetryingQuery)
redis_client = FlaskRedis()

# https://habr.com/ru/post/346344/
migrate = Migrate()
basedir = os.getcwdb().decode("utf-8")

app = Flask(__name__, static_folder=os.path.join(basedir, "static"),
            template_folder=os.path.join(basedir, "templates"))

app.config.from_object(os.getenv('FLASK_ENV') or 'config.Production')

# if app.config.get('DEVELOPMENT', False) is False:
#     sentry_sdk.init(
#         dsn=os.getenv("SENTRY_URI"),
#         integrations=[FlaskIntegration()]
#     )

db.init_app(app)
redis_client.init_app(app)
migrate.init_app(app, db)
oauth_client = OAuth(app)

oauth_client.register(name="discord",
                      api_base_url='https://discord.com/api/',
                      access_token_url='https://discord.com/api/oauth2/token',
                      authorize_url='https://discord.com/api/oauth2/authorize',
                      client_kwargs={"scope": "identify"}
                      )

oauth_client.register(name='vk',
                      api_base_url='https://api.vk.com/method/',
                      access_token_url='https://oauth.vk.com/access_token',
                      access_token_params={"client_id": os.getenv('VK_CLIENT_ID'),
                                           "client_secret": os.getenv('VK_CLIENT_SECRET')},
                      authorize_url='https://oauth.vk.com/authorize',
                      client_kwargs={"display": "page", "response_type": "code", "v": "5.131",
                                     'token_endpoint_auth_method': 'client_secret_basic'}
                      )

from .blueprints import *
from .core.user.module.session import UserAuthSession
from .core.form.models.answer import FormAnswer
from .blueprints.gift.engine.models import *
from .core.panel.models import *
from .core.store.models import *
from .core.pages.models import *
from .core.developers.api_application.model import *
from .core.developers.team import *
from .core.developers.oauth.model import *
from app.core.permissions.permissions import Permissions

app.register_blueprint(main_blueprint)

if app.config.get('DEVELOPMENT', False):
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    app.register_blueprint(gift_blueprint, url_prefix='/gift')
    app.register_blueprint(team_blueprint, url_prefix='/team')
    app.register_blueprint(store_blueprint, url_prefix='/store')
    app.register_blueprint(adminpanel_blueprint, url_prefix='/panel')
    app.register_blueprint(dev_blueprint, url_prefix='/dev')
    app.register_blueprint(event_blueprint, url_prefix='/event')
else:
    app.register_blueprint(auth_blueprint, subdomain='auth')
    app.register_blueprint(api_blueprint, subdomain='api')
    app.register_blueprint(api_blueprint, subdomain='ap', url_prefix='/api')
    app.register_blueprint(profile_blueprint, subdomain='profile')
    app.register_blueprint(gift_blueprint, subdomain='gift')
    app.register_blueprint(team_blueprint, subdomain='team')
    app.register_blueprint(store_blueprint, subdomain='store')
    app.register_blueprint(adminpanel_blueprint, subdomain='ap')
    app.register_blueprint(dev_blueprint, subdomain='dev')
    app.register_blueprint(event_blueprint, subdomain='event')


@app.before_request
def before_request():
    if "https://api.plazmix.net/" in request.url or "static" in request.url:
        return

    user_session = UserAuthSession.get_session_or_none()

    g.session = user_session
    g.user = None if user_session is None else user_session.user

    if g.user is None:
        return

    if g.user.block_status is False:
        return

    return ErrorPage(title="Ваш аккаунт заблокирован!", page_title="Аккаунт заблокирован",
                     comment=f"<h5>Ваш профиль заблокирован  "
                             f"за нарушение правил проекта!</h5>\n"
                             f" {f'<h6>Комментарий: {g.user.block_comment}</h6>' if g.user.block_comment else ''}"
                             f"<small>Если вы не согласны с блокировкой,"
                             f" то свяжитесь с технической поддержкой проекта!</small>",
                     icon="fad fa-user-lock fa-5x",
                     icon_color="ff5252"
                     ).add_button(PageButton(url="https://vk.me/plazmixnetwork",
                                             text="Техническая поддержка")).build()


@app.context_processor
def utility_processor():
    try:
        body = {
            "user": g.user,
            "session": g.session,
            "permissions": Permissions
        }
    except AttributeError:
        body = {}
    return body


@app.errorhandler(HTTPException)
def handle_exception(e):
    if e.code == 500:
        capture_exception(e)
    return ErrorPage(comment=f"Ошибка: {e.code}").add_button(
        PageButton(url="https://vk.me/plazmixnetwork", text="Связаться с тех поддержкой")).build()


# @app.errorhandler(OAuthError)
# def handle_error(error):
#     return ErrorPage(comment=f"Oauth Error: {error}").build()

from app.helper.fileds_check import view_filed

app.jinja_env.globals.update(view_filed=view_filed)
# app.jinja_env.globals.update(only_this_group_access=only_this_group_access)

CELERY_TASK_LIST = [
    'app.task.user',
    'app.task.email'
]


def make_celery():
    celery = Celery(app.import_name,
                    backend=f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:"
                            f"{os.getenv('REDIS_PORT')}/0",
                    broker=f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:"
                           f"{os.getenv('REDIS_PORT')}/0",
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    celery.conf.task_routes = {
        "user.*": {"queue": "user"},
        "email.*": {"queue": "email"},
        "bukkit.*": {"queue": "bukkit"},
        "clarence.*": {"queue": "clarence"},
        "tools.*": {"queue": "tools"},
    }
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery()

from app.core.developers.oauth.ext import config_oauth

config_oauth(app)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from app.task.bukkit_server import update_online
    from app.task.clarence import sync_counters, third_minute
    sender.add_periodic_task(60.0, update_online.s(), name='Update server online')
    sender.add_periodic_task(30.0, sync_counters.s(), name='Sync metrics')
    sender.add_periodic_task(1800.0, third_minute.s(), name='Clarence')
