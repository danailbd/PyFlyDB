from src.lib.utils import ensure_array
from src.lib.Printable import Printable


class Expression(Printable):
    '''
    A where (and other elements?) expression handler
    Contains a list of elements - variables, consts and operations
    '''

    def __init__(self, elements):
        self.elements = ensure_array(elements)

    def __repr__(self):
        return '<' + type(self).__name__ + '>' + str(self.elements)

    def __eq__(self, other):
        return self.elements == other.elements

    # TODO probably not ...
    def validate_expression(self):
        pass


class SimpleGraphPatternExpression(Expression):
    def __init__(self, expr):
        """

        Args:
            expr (List[Node|Edge]):
        """
        Expression.__init__(self, expr)


class GraphPatternExpression(Expression):
    def __init__(self, simple_exprs):
        """

        Args:
            simple_exprs (List[SimpleGraphPatternExpression]):
        """
        Expression.__init__(self, simple_exprs)


class OperatorExpression(Expression):
    def __init__(self, elements):
        Expression.__init__(self, elements)
