from src.lib.utils import ensure_tuple
from src.lib.utils import collect_identifiers
from src.lib.printable import Printable
from src.query_processor.query_ast.models import *


class Expression(Printable):
    """
    A where (and other elements?) expression handler
    Contains a list of elements - variables, consts and operations
    """

    def __init__(self, elements):
        self.elements = ensure_tuple(elements)

    def __repr__(self):
        return '<' + type(self).__name__ + '>' + str(self.elements)

    def __eq__(self, other):
        return self.elements == other.elements

    # TODO probably not ...
    def validate_expression(self):
        pass


class IdentifierExpression(Expression, IdentifierHolderMixin):
    def __init__(self, elements, identifiers):
        """"""
        super().__init__(elements)
        self.identifiers = identifiers

    def get_identifiers(self):
        return self.identifiers


class SimpleGraphPatternExpression(IdentifierExpression):
    def __init__(self, expr):
        """

        Args:
            expr (List[Node|Edge]):
        """
        # collect identifiers
        super().__init__(expr, collect_identifiers(expr))


class GraphPatternExpression(IdentifierExpression):
    def __init__(self, simple_exprs):
        """

        Args:
            simple_exprs (List[SimpleGraphPatternExpression]):
        """
        super().__init__(simple_exprs, collect_identifiers(simple_exprs))


class OperatorExpression(Expression):
    def __init__(self, elements):
        super().__init__(elements)


class GenericExpression(IdentifierExpression):
    def __init__(self, elements):
        super().__init__(elements, collect_identifiers(elements))
