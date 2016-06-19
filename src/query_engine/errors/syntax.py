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


class InvalidExpressionError(InvalidSyntaxError):
    def __init__(self, value):
        InvalidSyntaxError.__init__(self, value)


class InvalidGraphExpressionError(InvalidExpressionError):
    def __init__(self, value):
        InvalidExpressionError.__init__(self, value)


class InvalidNodeError(InvalidGraphExpressionError):
    def __init__(self, value, msg):
        InvalidGraphExpressionError.__init__(self, value)
        self.msg = msg


class InvalidEdgeError(InvalidGraphExpressionError):
    def __init__(self, value, msg):
        InvalidGraphExpressionError.__init__(self, value)
        self.msg = msg


class InvalidEdgeLabelError(InvalidEdgeError):
    def __init__(self, value, msg):
        InvalidEdgeError.__init__(self, value)
        self.msg = msg


class InvalidLabelsCountError(InvalidGraphExpressionError):
    def __init__(self):
        pass


class InvalidOperatorExpression(InvalidExpressionError):
    def __init__(self, value):
        InvalidExpressionError.__init__(self, value)
