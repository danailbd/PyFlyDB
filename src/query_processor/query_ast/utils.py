from src.query_processor.query_ast.expression import *
from src.query_processor.query_ast.clauses import *
from src.query_processor.errors.syntax import UnsupportedClauseError

# TODO rename file ...

STR_TO_CLAUSE = {
    'match': Match,
    'create': Create,
    'return': Return,
    'where': Where
}


def get_clause_type(clause_str):
    """
    Args:
        clause_str (str):
    Returns:
        Clause|None:
    """
    clause = clause_str.lower()
    clause = STR_TO_CLAUSE.get(clause)
    if clause:
        return clause
    else:
        raise UnsupportedClauseError(clause_str)

