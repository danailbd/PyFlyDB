from src.lib.utils import ensure_array

class Expression:
    '''
    A where (and other elements?) expression handler
    Contains a list of elements - variables, consts and operations
    '''

    def __init__(self, elements):
        self.elements = ensure_array(elements)

    # TODO probably not ...
    def validate_expression(self):
        pass


class GraphPatternExpression(Expression):

    def __init__(self, elements):
        Expression.__init__(self, elements)


class OperatorExpression(Expression):

    def __init__(self, elements):
        Expression.__init__(self, elements)


