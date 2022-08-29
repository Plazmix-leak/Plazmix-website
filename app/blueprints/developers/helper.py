from functools import wraps

from flask import g

from app.core.developers.team import DeveloperTeam
from app.helper.simple_page import ErrorPage


def team_get_and_check(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            team: DeveloperTeam = DeveloperTeam.get_from_uuid(ident=kwargs.get('team_uuid', 'none'))
        except ValueError:
            return ErrorPage(comment="Команда не найдена!").build()
        user = g.user
        if team.user_can_member(user) is False:
            return ErrorPage(comment=f"Вы не являетесь членом команды {team.name}").build()
        kwargs['team'] = team
        return function(*args, **kwargs)
    return wrapper
