from src.lib.utils import ensure_tuple

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
class Clause:
    pass


class Match(Clause):

    def __init__(self, expression):
        self.expression = expression


class Create(Clause):

    def __init__(self, expr):
        self.expr = expr


class Where(Clause):

    def __init__(self, expr):
        self.expr = expr


class Return(Clause):

    def __init__(self, props=()):
        self.props = ensure_tuple(props)

        #raise InvalidArguments('Return needs at least one item')


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

