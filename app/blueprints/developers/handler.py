from typing import List

from flask import render_template, g, redirect, url_for, request, flash

from app.core.developers.api_application import DeveloperApiApplication
from app.core.developers.oauth.model import OauthApplication
from app.core.developers.team import DeveloperTeam
from app.helper.decorators.web import login_required
from app.helper.flash_types import FlashTypes
from app.helper.simple_page import ErrorPage, SimplePage
from app.helper.simple_page.gray_page import GrayPage
from . import dev
from .form import CreateApiApplication, CreateOauthApplication, CreateDevelopmentTeamForm
from .helper import team_get_and_check


def split_by_crlf(s):
    return [v for v in s.split() if v]


@dev.route('/')
def index():
    return render_template('application/dev/index.html')


@dev.route('/teams')
@login_required
def teams():
    dev_teams: List[DeveloperTeam] = g.user.developer_teams
    return render_template('application/dev/user_team.html', teams=dev_teams)


@dev.route('/team/create', methods=['POST', 'GET'])
@login_required
def create_team():
    form = CreateDevelopmentTeamForm()
    page = GrayPage(comment="Создание команды разработчиков, после создания"
                            " вы соможете пригласить до 5-ти челвоек в команду. "
                            "Так-же вы можете создать до 5-ти приложений", form=form,
                    title="Создание команды разработчиков")
    if request.method.lower() == 'post':
        try:
            DeveloperTeam.create(g.user, form.name.data)
        except RuntimeError:
            return ErrorPage(comment="Похоже, что у вас уже больше 5-ти команд").build()
        return redirect(url_for('developers.teams'))
    return page.build()


@dev.route('/team/<team_uuid>/open')
@login_required
@team_get_and_check
def open_team(team_uuid, team: DeveloperTeam):
    return render_template('application/dev/open_team.html', team=team)


@dev.route('/team/<team_uuid>/application/app/create', methods=['GET', 'POST'])
@login_required
@team_get_and_check
def create_api_application(team_uuid, team: DeveloperTeam):
    form = CreateApiApplication()
    page = SimplePage(title="Создание API приложения",
                      comment=f"Вы собираетесь создать API приложение для команды {team.name}",
                      form=form)

    if request.method.lower() == 'post':
        try:
            DeveloperApiApplication.create(team, form.name.data)
        except RuntimeError:
            flash("Вы создали более 5-ти париложений!", FlashTypes.ERROR)
            return page.build()

        return redirect(url_for('developers.open_team', team_uuid=team_uuid))
    return page.build()


@dev.route('/team/<team_uuid>/application/oauth/create', methods=['GET', 'POST'])
@login_required
@team_get_and_check
def create_oauth_application(team_uuid, team: DeveloperTeam):
    form = CreateOauthApplication()
    page = SimplePage(title="Создание Oauth2 приложение",
                      comment=f"Вы собираетесь создать Oauth2 приложение для команды {team.name}",
                      form=form)

    if request.method.lower() == 'post':
        try:
            oauth_application = OauthApplication.generate_new_app(team, form.name.data)
            client_metadata = {
                "client_uri": form.redirect_url.data,
                "redirect_uris": form.redirect_url.data,
                "scope": "profile",
                "token_endpoint_auth_method": 'client_secret_basic',
                "grant_types": ["authorization_code"],
                "response_types": ["code"]
            }
            oauth_application.set_client_metadata(client_metadata)
        except RuntimeError:
            flash("Вы создали более 5-ти париложений!", FlashTypes.ERROR)
            return page.build()

        return redirect(url_for('developers.open_team', team_uuid=team_uuid))
    return page.build()


@dev.route('/team/<team_uuid>/application/oauth/<oauth_uuid>/info')
@login_required
@team_get_and_check
def info_application_oauth(team_uuid, team: DeveloperTeam, oauth_uuid: str):
    try:
        oauth_app: OauthApplication = OauthApplication.get_from_client_id_info(oauth_uuid)
    except ValueError:
        return ErrorPage(comment="Приложение не найдено!").build()

    if oauth_app.team_uuid != team_uuid:
        return ErrorPage(comment="Не принадлежит данной команде!").build()

    return render_template('application/dev/oauth_app_info.html', app=oauth_app)


@dev.route('/team/<team_uuid>/application/app/<app_uuid>/info')
@login_required
@team_get_and_check
def info_application_api(team_uuid, team: DeveloperTeam, app_uuid: str):
    try:
        application: DeveloperApiApplication = DeveloperApiApplication.get_from_uuid(app_uuid)
    except ValueError:
        return ErrorPage(comment="Приложение не найдено!").build()

    if application.team_uuid != team_uuid:
        return ErrorPage(comment="Не принадлежит данной команде!").build()

    return render_template('application/dev/api_app_info.html', app=application)


@dev.route('/team/<team_uuid>/application/app/<app_uuid>/edit', methods=['GET', 'POST'])
@login_required
@team_get_and_check
def edit_application_api(team_uuid, team: DeveloperTeam, app_uuid: str):
    try:
        application: DeveloperApiApplication = DeveloperApiApplication.get_from_uuid(app_uuid)
    except ValueError:
        return ErrorPage(comment="Приложение не найдено!").build()

    if application.team_uuid != team_uuid:
        return ErrorPage(comment="Не принадлежит данной команде!").build()

    form = CreateApiApplication()
    if request.method.lower() == 'get':
        form.name.data = application.name

    page = SimplePage(comment=f"Редактирование API приложения {application.name}", title=application.name,
                      page_title=application.name, form=form)

    if request.method.lower() == 'post':
        application.update_config(form.name.data)
        flash(f"Настройки приложения {application.name} обновлены!", FlashTypes.INFO)
        return redirect(url_for('developers.open_team', team_uuid=team_uuid))

    return page.build()


@dev.route('/team/<team_uuid>/application/oauth/<oauth_uuid>/edit', methods=['GET', 'POST'])
@login_required
@team_get_and_check
def edit_application_oauth(team_uuid, team: DeveloperTeam, oauth_uuid: str):
    try:
        oauth_app: OauthApplication = OauthApplication.get_from_client_id_info(oauth_uuid)
    except ValueError:
        return ErrorPage(comment="Приложение не найдено!").build()

    if oauth_app.team_uuid != team_uuid:
        return ErrorPage(comment="Не принадлежит данной команде!").build()

    form = CreateOauthApplication()
    if request.method.lower() == 'get':
        form.name.data = oauth_app.name
        form.redirect_url.data = oauth_app.redirect_uris

    page = SimplePage(comment=f"Редактирование API приложения {oauth_app.name}", title=oauth_app.name,
                      page_title=oauth_app.name, form=form)

    if request.method.lower() == 'post':
        client_metadata = {
            "client_uri": form.redirect_url.data,
            "redirect_uris": form.redirect_url.data,
            "scope": 'uuid',
            "token_endpoint_auth_method": 'client_secret_basic',
            "grant_types": ["authorization_code"],
            "response_types": ["code"]
        }
        oauth_app.update_config(form.name.data, metadata=client_metadata)
        flash(f"Настройки приложения {oauth_app.name} обновлены!", FlashTypes.INFO)
        return redirect(url_for('developers.open_team', team_uuid=team_uuid))

    return page.build()




