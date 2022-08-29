class EventError(Exception):
    def __init__(self, comment):
        self.comment = comment


class EventResponse(Exception):
    def __init__(self, response):
        self.response = response