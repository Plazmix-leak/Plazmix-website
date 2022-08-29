from functools import wraps

from flask import g, render_template, flash, redirect, url_for, request, abort

from app import redis_client
from app.core.permissions.groups import PermissionGroups
from app.core.user.module import UserPasswordRestore
from app.core.user import User, UserBalanceLog
from app.core.permissions import Permissions, rule_access_check
from app.helper.badges import BadgeCollections
from app.helper.decorators.web import login_required
from app.helper.flash_types import FlashTypes
from app.helper.simple_page.panel import AdminPanelErrorPage, AdminPanelSimplePage
from .forms import UserControlForm, UserChangePassword, UserBadgesForm, TechnicalSupportPanel, TSPasswordRequired, \
    UserSearchForm, UserBannedForm, UserUnBannedForm, UserMoneyChange, ClearGlobalCacheForm, \
    PermissionEditGroupModeration, PermissionEditGroupBuilder, PermissionEditGroupYouTube
from ... import panel


def _check_user(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user_uuid = kwargs.get('user_uuid', None)
        try:
            user: User = User.get_from_uuid(user_uuid)
        except ValueError:
            return AdminPanelErrorPage(comment="Такого пользователя не существует!").build()

        user_main_group = user.permission_group
        my_group = g.user.permission_group

        if user_main_group > my_group:
            return AdminPanelErrorPage(
                comment="Недостаточно прав для просмотра информации об этом пользователе!").build()

        kwargs['user'] = user
        return function(*args, **kwargs)

    return wrapper


@panel.route('/user/information/<user_uuid>', methods=['GET', 'POST'])
@login_required
@rule_access_check(Permissions.USER_VIEW)
@_check_user
def user_information(user_uuid, user: User):
    def _build(target, my_form, my_form_tp):
        return render_template('adminpanel/elements/users/information.html',
                               player=target, form=my_form, form_tp=my_form_tp)

    form = UserControlForm()
    form_tp = TechnicalSupportPanel()

    if form.validate_on_submit():
        if form.password_change.data:
            return redirect(url_for('panel.user_edit_password', user_uuid=user_uuid))
        elif form.badges.data:
            return redirect(url_for('panel.user_edit_badge', user_uuid=user.uuid))
        elif form.edit_money.data:
            return redirect(url_for('panel.user_money_edit', user_uuid=user.uuid))

    if form_tp.validate_on_submit():
        if form_tp.generate_password_reset_link.data:
            return redirect(url_for('panel.user_support_password', user_uuid=user_uuid))

    return _build(target=user, my_form=form, my_form_tp=form_tp)


@panel.route('/user/<user_uuid>/money/edit', methods=['GET', 'POST'])
@login_required
@rule_access_check(Permissions.USER_CHANGE)
@_check_user
def user_money_edit(user_uuid: str, user: User):
    form = UserMoneyChange()
    page = AdminPanelSimplePage(title="Изменение баланса", page_title="Изменение баланса",
                                comment=f"Изменение баланса у пользователя {user.bukkit.nickname}",
                                form=form)

    if form.validate_on_submit():
        comment = "Администрация Plazmix"
        amount = form.amount.data
        UserBalanceLog.user_money_edit(user, amount, comment=comment)
        flash(f"Баланс пользователя {user.bukkit.nickname} изменён на {amount} рублей", FlashTypes.INFO)
        return redirect(url_for('panel.user_information', user_uuid=user.uuid))
    return page.build()


@panel.route('/user/information/<user_uuid>/edt/password', methods=['GET', 'POST'])
@login_required
@rule_access_check(Permissions.USER_CHANGE)
@_check_user
def user_edit_password(user_uuid, user: User):
    form = UserChangePassword()
    page = AdminPanelSimplePage(title="Изменение пароля", page_title="Изменение пароля",
                                comment=f"Вы собираетесь изменить пароль у пользователя {user.bukkit.nickname}",
                                form=form)

    if form.validate_on_submit():
        password_one = form.new_password_one.data
        password_two = form.new_password_two.data
        if password_one != password_two:
            flash("Пароли не совпадают!", FlashTypes.ERROR)
            return page.build()

        user.edit_password(password_two, send_notification=False)
        flash(f"Вы успешно изменили пароль пользователю - {user.bukkit.nickname}")
        return redirect(url_for('panel.user_information', user_uuid=user.uuid))
    return page.build()


@panel.route('/user/information/<user_uuid>/edit/badge', methods=['GET', 'POST'])
@login_required
@rule_access_check(Permissions.USER_CHANGE)
@_check_user
def user_edit_badge(user_uuid, user: User):
    form = UserBadgesForm(user=user)
    page = AdminPanelSimplePage(title="Смена значков", page_title="Смена значков",
                                comment=f"Вы собираетесь изменить значки у пользователя {user.bukkit.nickname}",
                                form=form)

    if form.validate_on_submit():
        activate_badges = []
        all_badges = BadgeCollections.get_all()

        for badge in all_badges:
            instance = getattr(form, badge.technical_name, None)

            if instance is None:
                continue
            if instance.data.lower() == "yes":
                activate_badges.append(badge)
        user.badges_list = activate_badges

        flash("Вы успешно изменили бейдж", FlashTypes.INFO)
        return redirect(url_for('panel.user_information', user_uuid=user_uuid))

    return page.build()


@panel.route('/user/information/<user_uuid>/support/password', methods=['GET', 'POST'])
@login_required
@rule_access_check(Permissions.TECHNICAL_SUPPORT_ACCESS)
@_check_user
def user_support_password(user_uuid, user: User):
    form = TSPasswordRequired()
    page = AdminPanelSimplePage(title="ВНИМАНИЕ!",
                                page_title="Ссылка восстановления пароля",
                                comment=f"Вы собираетесь создать уникальную ссылку для сброса проля пользователя"
                                        f" {user.bukkit.nickname}. Перед тем как сгенерировать её, убедитесь,"
                                        f" что пользователь предоставиль достаточно доказательств подтверждающих"
                                        f" владение аккаунтом! Если вы успешно подтвердили личность владельца,"
                                        f" то нажмите кнопку 'сгенерировать ссылку'",
                                form=form)
    if form.validate_on_submit():
        if form.canceled.data:
            return redirect(url_for('panel.user_information', user_uuid=user_uuid))

        restore = UserPasswordRestore.init_from_user(user, send_email=False)
        return AdminPanelSimplePage(title="Ссылка для сброса", page_title="Ссылка для сброса",
                                    comment=f"Ссылка для сброса пароля успешно создана,"
                                            f" скопируйте её и отрпвьте пользователю"
                                            f"<p>{restore.link}</p>").build()

    return page.build()


@panel.route('/user/<user_uuid>/give/ban', methods=['POST', 'GET'])
@login_required
@rule_access_check(Permissions.ADMIN_ACCESS)
@_check_user
def user_ban(user_uuid, user: User):
    if user.block_status is True:
        flash(f"Пользователь {user.bukkit.nickname} уже заблокирован", FlashTypes.WARNING)
        return redirect(url_for('panel.user_information', user_uuid=user_uuid))
    form = UserBannedForm()
    page = AdminPanelSimplePage(title="Заблокировать пользователя",
                                comment=f"Вы собираетесь выдать блокировку пользователю {user.bukkit.nickname}",
                                form=form)

    if form.validate_on_submit():
        reason = form.reason.data or None
        user.banned(form.reason.data or None)
        flash(f"Пользователь {user.bukkit.nickname} успешно заблокирован по причине: {reason or 'Причина не указана'}",
              FlashTypes.INFO)
        return redirect(url_for('panel.user_information', user_uuid=user_uuid))
    return page.build()


@panel.route('/user/<user_uuid>/give/unban', methods=['POST', 'GET'])
@login_required
@rule_access_check(Permissions.ADMIN_ACCESS)
@_check_user
def user_unban(user_uuid, user: User):
    if user.block_status is False:
        flash(f"Пользователь {user.bukkit.nickname} не заблокирован", FlashTypes.WARNING)
        return redirect(url_for('panel.user_information', user_uuid=user_uuid))

    form = UserUnBannedForm()
    page = AdminPanelSimplePage(title="Разблокировать пользователя",
                                comment=f"Вы собираетесь снять блокировку пользователю {user.bukkit.nickname}",
                                form=form)

    if form.validate_on_submit():
        user.unbanned()
        flash(f"Пользователь {user.bukkit.nickname} успешно разблокирован",
              FlashTypes.INFO)
        return redirect(url_for('panel.user_information', user_uuid=user_uuid))
    return page.build()


@panel.route('/user/search', methods=['POST', 'GET'])
@login_required
@rule_access_check(Permissions.PANEL_ACCESS)
def users_search():
    form = UserSearchForm()
    users = []

    def _build():
        return render_template('adminpanel/elements/users/search.html', form=form, users=users)

    if form.validate_on_submit():
        nickname = form.nickname_like.data

        form.nickname_like.data = nickname
        if len(nickname) < 3:
            flash("Никнейм должен быть не мнее 3-х символов", FlashTypes.ERROR)
            return _build()
        users = sorted(User.search_from_nickname(nickname, page=1, limit=50),
                       key=lambda element: element.permission_group, reverse=True)

    return _build()


@panel.route('/user/<user_uuid>/permission/group/<cluster>', methods=['POST', 'GET'])
@login_required
@rule_access_check(Permissions.APPLICATION_CONTROL)
@_check_user
def permission_control(user_uuid, cluster, user: User):
    lower_cluster = cluster.lower()

    if lower_cluster == "mod":
        form = PermissionEditGroupModeration()
    elif lower_cluster == "build":
        form = PermissionEditGroupBuilder()
    elif lower_cluster == "yt":
        form = PermissionEditGroupYouTube()
    else:
        return abort(404)

    page = AdminPanelSimplePage(title="Управление группой прав пользователя",
                                comment=f"Вы собираетесь изменить группу прав пользователя {user.bukkit.nickname}",
                                form=form, page_title="Управление группой прав пользователя")

    if request.method.lower() == "get":
        return page.build()
    if form.validate_on_submit():
        if lower_cluster == "mod":
            if form.junior.data:
                user.give_permission_group(PermissionGroups.JUNIOR)
            if form.junior_remove.data:
                user.remove_permission_group(PermissionGroups.JUNIOR)

            if form.moderation.data:
                user.give_permission_group(PermissionGroups.MODERATOR)
            if form.moderation_remove.data:
                user.remove_permission_group(PermissionGroups.MODERATOR)

            if form.senior.data:
                if g.user.permission_group < PermissionGroups.ADMINISTRATOR.value:
                    return abort(403)
                user.give_permission_group(PermissionGroups.MODERATOR_PLUS)
            if form.senior.data:
                if g.user.permission_group < PermissionGroups.ADMINISTRATOR.value:
                    return abort(403)
                user.remove_permission_group(PermissionGroups.MODERATOR_PLUS)

            if form.delete_all.data:
                user.remove_permission_group(PermissionGroups.JUNIOR)
                user.remove_permission_group(PermissionGroups.MODERATOR)
                user.remove_permission_group(PermissionGroups.MODERATOR_PLUS)

            flash("Группы изменены", FlashTypes.INFO)
            return page.build()

        elif lower_cluster == "build":
            if g.user.permission_group < PermissionGroups.ADMINISTRATOR.value:
                return abort(403)

            if form.build.data:
                user.give_permission_group(PermissionGroups.BUILDER)
            if form.remove_build.data:
                user.remove_permission_group(PermissionGroups.BUILDER)

            if form.senior_builder.data:
                user.give_permission_group(PermissionGroups.BUILDER_PLUS)
            if form.senior_builder_remove.data:
                user.remove_permission_group(PermissionGroups.BUILDER_PLUS)

            if form.delete_all.data:
                user.remove_permission_group(PermissionGroups.BUILDER)
                user.remove_permission_group(PermissionGroups.BUILDER_PLUS)

            flash("Группы изменены", FlashTypes.INFO)
            return page.build()

        elif lower_cluster == "yt":
            if g.user.permission_group < PermissionGroups.OWN.value:
                return abort(403)

            if form.add_yt.data:
                user.give_permission_group(PermissionGroups.YOUTUBE)
            if form.remove_yt.data:
                user.remove_permission_group(PermissionGroups.YOUTUBE)

            if form.add_yt_plus.data:
                user.give_permission_group(PermissionGroups.YOUTUBE_PLUS)
            elif form.remove_yt.data:
                user.remove_permission_group(PermissionGroups.YOUTUBE_PLUS)

            if form.delete_all.data:
                user.remove_permission_group(PermissionGroups.YOUTUBE)
                user.remove_permission_group(PermissionGroups.YOUTUBE_PLUS)

            flash("Группы изменены", FlashTypes.INFO)
            return page.build()

    flash("Ошибка обработки формы!", FlashTypes.ERROR)
    return page.build()


@panel.route('/global/cache/clear', methods=['POST', 'GET'])
@login_required
@rule_access_check(Permissions.OWNER_ACCESS)
def clear_global_cache():
    form = ClearGlobalCacheForm()
    page = AdminPanelSimplePage(title="Очистка кэша", comment="Вы собираетесь очистить кэш проекта."
                                                              f" Размер базы на данный момент: {redis_client.dbsize()}",
                                form=form)

    if form.validate_on_submit():
        redis_client.flushall()
        flash("Кэш успешно очищен", FlashTypes.INFO)
        print(redis_client.dbsize())
    return page.build()
