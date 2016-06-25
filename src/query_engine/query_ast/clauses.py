from src.query_engine.errors.syntax import *
from src.query_engine.query_ast.expression import *
from src.lib.printable import Printable

"""
Either add some serious logic to items or generate them dynamicaly
(type)

MAIN_CLAUSES = [
    'MATCH',
    'MERGE',
    # This matches or creates semantics by using
    # indexes and locks. You can specify different
    # operations in case of a MATCH (part of the
    #     pattern already existed) or on CREATE
    # (pattern did not exist yet).

    'CREATE UNIQUE',
    'CREATE',
    'SET',     # This updates properties and labels on nodes
    'REMOVE',  # +and/or relationships.
    'DELETE',   # It deletes nodes and relationships

    'PROFILE',
]

SUB_CLAUSES = [
    'RETURN',
    'WHERE',
    'WITH',
    'DISTINCT',
    'ORDER BY'
]
"""


class Clause(Printable):
    expression_type = None

    def __init__(self, expression):
        self.expression = expression

    @classmethod
    def get_expression_type(cls):
        return cls.expression_type


class Match(Clause):
    expression_type = GraphPatternExpression

    def __init__(self, expression):
        super().__init__(expression)


class Create(Clause):
    expression_type = GraphPatternExpression

    def __init__(self, expression):
        super().__init__(expression)


class Where(Clause):
    expression_type = OperatorExpression

    def __init__(self, expression):
        super().__init__(expression)


class Return(Clause):
    expression_type = GenericExpression

    def __init__(self, expression, props=()):
        super().__init__(expression)
        self.props = ensure_tuple(props)

        # raise InvalidArguments('Return needs at least one item')


MAIN_CLAUSES = [
    'MATCH',
    'MERGE',
    # This matches or creates semantics by using
    # indexes and locks. You can specify different
    # operations in case of a MATCH (part of the
    #     pattern already existed) or on CREATE
    # (pattern did not exist yet).

    'CREATE UNIQUE',
    'CREATE',
    'SET',  # This updates properties and labels on nodes
    'REMOVE',  # +and/or relationships.
    'DELETE',  # It deletes nodes and relationships

    'PROFILE',
]

SUB_CLAUSES = [
    'RETURN',
    'WHERE',
    'WITH',
    'DISTINCT',
    'ORDER BY'
]
