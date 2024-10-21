
class DataSourceError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidData(DataSourceError):

    def __str__(self):
        return f'Invalid data: {self.args[0]}'
