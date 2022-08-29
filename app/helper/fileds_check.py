from wtforms.fields import HiddenField, SubmitField


def view_filed(filed):
    check = True

    if isinstance(filed, HiddenField) is True:
        check = False

    if isinstance(filed, SubmitField) is True:
        check = False
    return check
