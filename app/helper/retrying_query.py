from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import OperationalError, StatementError
from time import sleep


class RetryingQuery(BaseQuery):
    __retry_count__ = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        attempts = 0
        while True:
            attempts += 1
            try:
                return super().__iter__()
            except OperationalError as ex:
                # if "server closed the connection unexpectedly" not in str(ex):
                #     raise
                if attempts < self.__retry_count__:
                    sleep_for = 2 ** (attempts - 1)
                    print(
                        "Database connection error: {} - sleeping for {}s"
                        " and will retry (attempt #{} of {})".format(
                            ex, sleep_for, attempts, self.__retry_count__
                        ))
                    sleep(sleep_for)
                    continue
                else:
                    raise
            except StatementError as ex:
                if "reconnect until invalid transaction is rolled back" not in str(ex):
                    raise
                self.session.rollback()
