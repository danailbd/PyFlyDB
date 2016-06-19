import re
import collections
import itertools
import logging as Logger

from src.query_engine.errors.syntax import *

from src.query_engine.query_ast.operators import *
from src.query_engine.query_ast.query import *
from src.query_engine.query_ast.models import *
from src.query_engine.query_ast.clauses import *
from src.query_engine.query_ast.expression import *
from src.query_engine.query_ast import utils

'''
Support Notes:
- Nodes properties may have space between value and key
- Properties value may be - string, number
- Nodes may have more than 1 space between labels and properties
- Support whitespaces in id/labels  ???
- Case-sensitive labels and ids  ??
- Edges with properties

- Only Edge search -> ()-[]-()

- Support split by ',' expressions


- split to clauses  (Match)
- split to sub-query (Where) -> Clause, expr, Cluase, expr ...
- Parse expression by clause


new MatchClause()
'''
# TODO flags -> convert to number; find all matches
# TODO use \w ?? or \S
IDENTIFIER_REGEX = re.compile('^(\w+)(?:|\s)?')
LABELS_REGEX = re.compile(':(\w+)(?:|\s)?')

# TODO allowed_val_chars = '\w|\''
PROPERTIES_BODY_REGEX = re.compile('{(.*?)}')
PROPERTY_REGEX = re.compile('(?P<key>\w+):\s*"?(?P<val>[\w|.]+)"?,?\s*')

# TODO FIX
# TODO caseInsensitive
def split_list(unsplitted, sep_list, PN=False):
    """
    Splits a string by list of separators

    Unary prefix by default.
    """

    # TODO use re.split() !!!

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

'''
   ** PARSER **
'''
def check_valid_edge(raw_node):
    # Does it have brackets
    error = None
    if len(raw_node) - 2 != len(raw_node.strip('[]')):
        error = 'Edge must be enclosed in []'
    # TODO other checks
    # elif

    if error:
        raise InvalidEdgeError(raw_node, error)


def check_valid_node(raw_node):
    # Does it have brackets
    error = None
    if len(raw_node) - 2 != len(raw_node.strip('()')):
        error = 'Node must be enclosed in ()'
    # TODO other checks
    # elif

    if error:
        raise InvalidNodeError(raw_node, error)


def get_properties(raw_elem):
    """
    Gets properties; Parses to Number if possible.
    Args:
        raw_node (str):

    Returns:
        List[Property]:

    """
    def to_number(s):
        """Tries to parse element to number."""
        try:
            return float(s)
        except ValueError:
            try:
                return int(s)
            except ValueError:
                return s

    # MATCH should work (match the beginning ...)
    # Else raise error
    # TODO or use findAll
    # TODO check for {} brackets
    properties = []
    raw_props = PROPERTIES_BODY_REGEX.search(raw_elem)
    # get matched group
    if raw_props and raw_props.group(1):
        raw_props = raw_props.group(1)
        Logger.debug('Processing properties: ', raw_props)

        # Use Named Groups to match elements
        match = PROPERTY_REGEX.match(raw_props)
        while match:
            key = match.group('key').strip()
            value = to_number(match.group('val').strip())
            properties.append(Property(key=key, value=value))

            match = PROPERTY_REGEX.match(raw_props, match.end())

    return properties


def get_labels(raw_elem, multi=True):
    """
     ;id {};id:... {}
    Args:
        raw_node (str):
    Returns:
        List[Label]:
    """
    match = LABELS_REGEX.findall(raw_elem)
    # edge labels
    if match and (len(match) > 1 and not multi):
        raise InvalidLabelsCountError()
    # Make to system labels
    match = [Label(raw_label) for raw_label in match]
    if match and not multi:
        # Is edge label
        match = match[0]
    return match


def get_identifier(raw_elem):
    """
     ;id {};id:... {}
    Args:
        raw_node (str):
    Returns:
        Identifier|None:
    """
    match = IDENTIFIER_REGEX.search(raw_elem)
    if match:
        match = Identifier(match.group(1).strip())
    return match


def is_node(raw_elem):
    pass


def is_edge(raw_elem):
    pass


def parse_node(raw_node):
    """
    Node must follow the pattern: ([identifier][:label:label...] [{properties}])
    Args:
        raw_node (str):
    Returns:
        Node:
    Raises:
        InvalidNodeError:
    """
    check_valid_node(raw_node)

    identifier = get_identifier(raw_node)
    labels = get_labels(raw_node)
    properties = get_properties(raw_node)

    return Node(identifier=identifier, labels=labels, properties=properties)


def parse_edge(raw_edge):
    """
    An edge can
    Returns an edge with specified properties and orientation.
    """
    check_valid_edge(raw_edge)
    raw_edge = raw_edge.strip()

    identifier = get_identifier(raw_edge)
    label = get_labels(raw_edge, True)
    properties = get_properties(raw_edge)

    return Edge(identifier=identifier, label=label, properties=properties)


def parse_simple_graph_expr(raw_simple_expr):
    """
    Expression must follow the pattern:
        Node[Edge && Node ...]
    Args:
        raw_simple_expr (str):
    Returns:
        SimpleGraphPatternExpression:

    Raises:
        InvalidGraphExpressionError:

    """
    # split to items
    # parse Node, parse Edge
    simple_expr_raw_elements = raw_simple_expr.split('-')

    simple_expr_elements = []

    for elem in simple_expr_raw_elements:
        # Parse by element type
        if is_node(elem):
            parsed_elem = parse_node(elem)
        elif is_edge(elem):
            parsed_elem = parse_edge(elem)

        else:
            raise InvalidGraphExpressionError(elem)

        simple_expr_elements.append(parsed_elem)
        # TODO populate Edges

    return SimpleGraphPatternExpression(simple_expr_elements)


def parse_graph_expression(simple_graph_exprs):
    """
     ()-[]-(); (); (), ()-[]-()
     Args:
         simple_graph_exprs (List[str]):
     Returns:
         GraphPatternExpression:

     """
    # Split by ,
    # split by -
    # parse elements as follows -> node, edge, node edge ...
    # TODO  MOVE TO SPLITTER
    simple_graph_exprs = [parse_simple_graph_expr(simple_expr)
                          for simple_expr in simple_graph_exprs]

    return GraphPatternExpression(simple_graph_exprs)


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
    expression = expression.split(',')

    if expression_type == GraphPatternExpression:
        parser = parse_graph_expression
    elif expression_type == OperatorExpression:
        parser = parse_operator_expression
    else:
        raise UnsupportedExpressionType(expression_type)

    return parser(expression)


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

            # TODO split expressions by ','

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
