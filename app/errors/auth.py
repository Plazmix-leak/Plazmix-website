class AuthError(Exception):
    def __init__(self, reason="Неизвестная ошибка, свяжитесь с администрацией!"):
        self._reason = reason

    @property
    def get_reason(self):
        return self._reason