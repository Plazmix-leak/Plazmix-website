from flask import render_template, url_for, abort

from app.core.pages.models import Page
from . import main
from ...core import News
from ...helper.simple_page import SimplePage, PageButton, ButtonType, ErrorPage
from ...lib.clarence.metric import Metric
from ...lib.clarence.sorted.sorter import DataMetricSorted
from ...lib.clarence.sorted.type import SortType


@main.route("/")
def index():
    return render_template("application/main/index.html")


@main.route('/ajax/news')
def load_news():
    return render_template("application/main/ajax/news.html", posts=News.get_last(6))


@main.route('/pages')
def pages():
    return render_template('application/main/pages.html', pages=Page.get_all_publish())


@main.route('/page/<page_uri>')
def page(page_uri):
    try:
        current_page: Page = Page.get_from_uri(uri=page_uri)
    except ValueError:
        return abort(404)

    if current_page.public is False:
        return abort(404)
    try:
        version = current_page.current_version
    except RuntimeError:
        return ErrorPage(comment="Возникла непредвиденная ошибка, пожалуйста сообщите о ней нам").add_button(
            PageButton(url="https://vk.me/plazmixnetwork",
                       text="Техническая поддержка",
                       button_type=ButtonType.COLOR_PRIMARY)
        ).build()
    return render_template('application/main/page.html', content=version, current_page=current_page)


@main.route('/about')
def about():
    return render_template('application/main/about.html')


@main.route("/secret/badge/crown")
def badge_crown():
    return SimplePage(title="Бейдж: Администрация",
                      comment="Данный бейдж нельзя получить и он не выдаётся аккаунтам, данный символ"
                              " присваивается техническим аккаунтам администрации", icon="fad fa-crown fa-8x",
                      icon_color="#FFD700", page_title="Admin badge").add_button(
        PageButton(url=url_for("main.index"), text="На главную", button_type=ButtonType.COLOR_PRIMARY)).build()
