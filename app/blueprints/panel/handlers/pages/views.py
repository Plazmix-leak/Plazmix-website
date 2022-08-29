from flask import render_template, g, flash, redirect, url_for

from app.blueprints.panel.handlers.pages.form import PageEditor, PageCreate
from app.core.permissions import Permissions
from app.helper.flash_types import FlashTypes
from app.helper.simple_page.panel import AdminPanelErrorPage, AdminPanelSimplePage
from app.core.pages.models import Page
from app.blueprints.panel import panel
from app.core.permissions import rule_access_check
from app.helper.decorators.web import login_required


@panel.route('/page/list')
@login_required
@rule_access_check(Permissions.PAGE_EDIT)
def page_list():
    pages = Page.get_all()
    return render_template('adminpanel/elements/pages/list.html', pages=pages)


@panel.route('/page/<int:page_id>/edit', methods=['GET', 'POST'])
@login_required
@rule_access_check(Permissions.PAGE_EDIT)
def page_edit(page_id):
    try:
        page: Page = Page.get_from_id(page_id)
    except ValueError:
        return AdminPanelErrorPage(comment="Такой страницы не существует!").build()

    form = PageEditor(page_content=page)
    page_view = AdminPanelSimplePage(title=f"Редактирование {page.uri}",
                                     comment=f"Вы редактируете страницуу {page.uri}",
                                     page_title=f"Редактирование {page.uri}",
                                     form=form)

    if form.validate_on_submit():
        cv = page.current_version
        if cv.title != form.title.data or cv.content != form.content.data:
            new_version = page.new_version(g.user, title=form.title.data, content=form.content.data)
            page.current_version = new_version

        if form.publish.data == 'no':
            page.hide()
        elif form.publish.data == 'yes':
            page.publish()

        flash(f"Вы успешно изменили страницу {page.uri}", FlashTypes.INFO)
        return redirect(url_for('panel.page_list'))

    return page_view.build()


@panel.route('/page/create', methods=['GET', 'POST'])
@login_required
@rule_access_check(Permissions.PAGE_EDIT)
def page_create():
    form = PageCreate()
    page = AdminPanelSimplePage(title="Создание страницы", page_title="Создание старницы",
                                form=form, comment=None)

    if form.validate_on_submit():
        new = Page.create(form.uri.data, g.user, form.title.data,
                          form.content.data)

        if form.publish.data == 'no':
            new.hide()
        elif form.publish.data == 'yes':
            new.publish()

        flash(f"Вы успешно создали страницу {new.uri}", FlashTypes.INFO)
        return redirect(url_for('panel.page_list'))
    return page.build()
