class InvalidSyntaxError(Exception):
    def __init__(self, value):
        """Base syntax error."""
        self.value = value


class UnsupportedClauseError(InvalidSyntaxError):
    pass


class UnsupportedExpressionType(InvalidSyntaxError):
    pass


class NumberOfOperandsError(InvalidSyntaxError):
    pass


class InvalidOperationError(InvalidSyntaxError):
    pass


class InvalidExpressionError(InvalidSyntaxError):
    pass


class InvalidGraphExpressionError(InvalidExpressionError):
    pass


class BadGraphExpressionElementError(InvalidGraphExpressionError):
    pass


class InvalidNodeError(InvalidGraphExpressionError):
    def __init__(self, value, msg):
        InvalidGraphExpressionError.__init__(self, value)
        self.msg = msg


class EmptyGraphPatternExpressionError(InvalidGraphExpressionError):
    pass


class InvalidGraphExpressionPropertiesError(InvalidGraphExpressionError):
    def __init__(self, value, msg=''):
        InvalidGraphExpressionError.__init__(self, value)
        self.msg = msg


class InvalidEdgeError(InvalidGraphExpressionError):
    def __init__(self, value, msg=''):
        InvalidGraphExpressionError.__init__(self, value)
        self.msg = msg


class InvalidEdgeLabelError(InvalidEdgeError):
    def __init__(self, value, msg):
        InvalidEdgeError.__init__(self, value)
        self.msg = msg


class InvalidLabelsCountError(InvalidGraphExpressionError):
    pass


class InvalidOperatorExpression(InvalidExpressionError):
    pass
