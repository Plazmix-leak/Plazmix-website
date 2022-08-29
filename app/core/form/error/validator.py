class ValidationError(Exception):
    def __init__(self, comment):
        self.comment = comment
