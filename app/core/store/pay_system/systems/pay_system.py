class PaySystem:
    def __init__(self, label: str, technical_name: str, payment_cls, payment_check_cls,
                 client_cls):
        self._label = label
        self._technical_name = technical_name
        self._payment_cls = payment_cls
        self._payment_check_cls = payment_check_cls
        self._client_cls = client_cls

    @property
    def label(self):
        return self._label

    @property
    def technical_name(self):
        return self._technical_name

    @property
    def payment_cls(self):
        return self._payment_cls

    @property
    def payment_check_cls(self):
        return self._payment_check_cls

    @property
    def client(self):
        return self._client_cls()
