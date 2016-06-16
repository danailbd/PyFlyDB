import re
import collections
import itertools

from src.query_engine.errors.syntax import *

from src.query_engine.query_ast.operators import *
from src.query_engine.query_ast.query import *
from src.query_engine.query_ast.models import *
from src.query_engine.query_ast.clauses import *
from src.query_engine.query_ast.expression import *
from src.query_engine.query_ast import utils

'''
- split to clauses  (Match)
- split to sub-query (Where) -> Clause, expr, Cluase, expr ...
- Parse expression by clause


new MatchClause()
'''


# TODO FIX
# TODO caseInsensitive
def split_list(unsplitted, sep_list, PN=False):
    """
    Splits a string by list of separators

    Unary prefix by default.
    """

    def apply_notation(splitted_list, splitter):
        # TODO splitter may provide type of the notation (infix, postfix, suffix)
        if PN:
            # Binary operators - in_fix
            for split_pos in range(0, len(splitted_list), 3):
                splitted_list.insert(split_pos, splitter)
        else:
            # unary operators - prefix
            for split_pos in range(1, len(splitted_list)):

                splitted_list.insert(split_pos, splitter)
                if not unsplitted or len(sep_list) == 0:
                    return unsplitted

    splitter = sep_list[0] + ' '  # don't match
    rest = sep_list[1:]
    # splitted = []

    if isinstance(unsplitted, list):
        splitted_list = []
        for sub_str in unsplitted:
            splitted_com = sub_str.split(splitter)
            if len(splitted_com) > 0:
                apply_notation(splitted_com, splitter)

            splitted_list.append(splitted_com)
        splitted = list(itertools.chain(*splitted_list))
    else:
        splitted = unsplitted.split(splitter)
        apply_notation(splitted, splitter)

    return split_list(splitted, rest)


# -- EXPRESSIONS --

MATCH_SPLITTERS = ['-']
MULTI_ELEMENTS_SPLITTER = [',']

OPERATORS_BY_PRIORITY = ['OR', 'XOR', 'AND', 'OR', '>', '<', '<=', '>=', 'IN']

COMMANDS = {}

'''
   ** PARSER **
'''

def __parse_node(node_string):
    """
    Accepts (var:label {})

    Do paring of string to node data and
    return Node Object
    """
    properties = __get_properties(node_string)

    labels = __get_labels(__parse_node)

    varibalbe_str = re.search('[^(]\w*(\)|\{))]', node_string)
    return varibalbe_str.group(0).split(':') if varibalbe_str else None


def __get_properties(node_string):
    """
        {name: "Emu", ..} - dict use eval
        returns prop dict or None
        """
    properties_string = re.search('\{.*\}', node_string)
    return eval(properties_string) if properties_string else None


def __get_labels(node_string):
    """
    varName:Label1:Label2:...
    returns {
    varName: ...,
    labels: []
    } or None
    """
    pass


def __parse_edge(self, node_string):
    """
    An edge can
    Returns an edge with specified properties and orientation.
    """
    properties = __get_properties(node_string)
    labels = __get_labels(__parse_node)


def generate_clause(clause, raw_expr):
    """

    Args:
        clause (str):
        raw_expr (str|List(str)):

    Returns:
        Clause:
    """
    clause = utils.get_clause_type(clause)
    return clause(raw_expr)


def parse_expression(expression, expression_type):
    """

    Args:
        expression (str):
        expression_type (Expression): The type of expression. Note it represents
            a class, not an instance.

    Returns:
        Expression: the generated expression

    Raises:
        InvalidSyntaxError:
    """

    if expression_type == GraphPatternExpression:
        parser = parse_graph_expression
    elif expression_type == OperatorExpression:
        parser = parse_operator_expression
    else:
        raise UnsupportedExpressionType(expression_type)

    return expression_type(parser(expression))


def parse_clause(raw_clause):
    """

    Args:
        raw_clause (List[srt]): [clause, expr]

    Returns:
        Clause: The generated clause
    """
    clause_str = raw_clause[0]
    expr = raw_clause[1]

    expr = parse_expression(expr,
                            utils.get_expression_type(clause_str))
    return generate_clause(clause_str, expr)


class QueryParser:
    """
    Creates a Query object out of a query string.
    """

    @staticmethod
    def parse_query(query):
        """
        Parses an incoming query
            CREATE ...
            MATCH ...
            as follows:
                * get subqueries -- [CREATE ..., MATCH, ...]
                * parse each sub query -
                * define operation
                * extract expression
                * extract sub commands (WHERE, RETURN)
                * TODO -- optimize query
                * run sub query
                * result in identifiers
                * process next items with results from first

        Args:
            query (str):

        Returns:
            Query: generated query

        """

        def parse_sub_query(raw_sub_query):
            """

            Args:
                raw_sub_query (List[str]):
                    A list containing the sub-query elements,
                    e.g. ['Match', '(you)'],
                          ['Match', '(you)', 'Return', 'you.a']

            Returns:
                SubQuery: generated SubQuery
            """

            # Break to smaller parts with sub clauses - RETURN, WHERE
            # List of: Clause, expressions (, separated)
            subclauses_split = split_list(raw_sub_query, SUB_CLAUSES)

            #  process expressions (of MATCH, WHERE, ...
            # TODO expression type is defined by the clause it refers to -- use that cluase
            subclauses = (parse_clause(subclause_list)
                          for subclause_list in subclauses_split)

            return SubQuery(subclauses)

        # Process query by parts.
        # Sub queries are defined by specific Clauses

        # TODO trailing spaces
        sub_queries_str = split_list(query, MAIN_CLAUSES)

        sub_queries = [parse_sub_query(sub_query) for sub_query in
                       sub_queries_str]
        # TODO parse to Query object ?

        # createSubQueries()
        # createQueryObject()

        return Query(sub_queries)  # TODO variables ???


"""
Spliting
    By main operation keyword - MATCH, CREATE ...
    Subspliting:
        CREATE -- ',' (),(), ()-[]->()
        MATCH -- ','; '-'
        -- split by, and then by - ... it must be: (node),[edge],(node)<,[edge], ...
        -- ()-->()
        -- ()--()
        -- (a)-->()<--(b)  -- path
        -- ({x:1})
        -- (a)-[{b:3}]->(b)
        -- (a)-[:A]-()

    WHERE e.name IN ['a', 'b'] AND e.b > 5 OR  ...
    """

# query -> main_parts ->
"""
CREATE (m:Person {name:'b'})
MATCH n WHERE n.name='B' RETURN n.name
==>  Split by main clauses
'MATCH (n), (a)-->(b)<--c<--(d),  WHERE n.name RETURN n.name'
==> Split by sub clauses ((a n1 n2 n3))
[
['MATCH', (n)--()],
['WHERE', 'n.name=\'B\''],
['RETURN', 'n.name']
]
-> [commands] -- [M, W, R],
[expressions] -- list, tree ?


list  --  a > 5 AND b < 3 --> [and, >, a, 5, <, b, 3]
"""
