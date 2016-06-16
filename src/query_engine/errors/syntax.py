class InvalidSyntaxError(Exception):
    def __init__(self, value):
        """"""
        self.value = value


class UnsupportedExpressionType(InvalidSyntaxError):
    def __init__(self, value):
        """"""
        InvalidSyntaxError.__init__(self, value)

class NumberOfOperandsError(InvalidSyntaxError):
    pass

class InvalidOperationError(InvalidSyntaxError):
    pass


