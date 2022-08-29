class PaySystemError(Exception):
    def __init__(self, comment="unknown"):
        self.comment = comment

    def __repr__(self):
        return f"Pay system error comment - {self.comment}"

    __str__ = __repr__
