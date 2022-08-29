from app.core.store.pay_system.errors import PaySystemError


class EnotApiError(PaySystemError):
    def __init__(self, comment="unknown error with enot.io system"):
        super(EnotApiError, self).__init__(comment=comment)