from app import celery


@celery.task(name="user.mail_login")
def user_mail_login(user_uuid, ip):
    pass
