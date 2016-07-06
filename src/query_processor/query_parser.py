import re
from enum import Enum

import logging as Logger

from src.query_processor.errors.syntax import *

from src.query_processor.query_ast.operators import *
from src.query_processor.query_ast.query import *
from src.query_processor.query_ast.models import *
from src.query_processor.query_ast.clauses import *
from src.query_processor.query_ast.expression import *
from src.query_processor.query_ast.utils import *
from src.lib import utils

'''
Support Notes:
- Nodes properties may have space between value and key
- Properties value may be - string, number, identifier
-- any string
-- float or integer
-- letters_and_numbers. ...
- Nodes may have more than 1 space between labels and properties
- Support whitespaces in id/labels  ???
- Case-sensitive labels and ids  ??
- Edges with properties

- Only Edge search -> ()-[]-()

- Support split by ',' expressions


- split to clauses  (Match)
- split to sub-query (Where) -> Clause, expr, Cluase, expr ...
- Parse expression by clause


TODO --
- Set x.y = 10
- WITH c, SUM(..) AS x


TODO -- support for properties
Variable fields:
- in node -> (var)
- Return, With, ...
- properties

GraphExpressions
OperatorExpressions
IdExpressions

'''
MATCH_NODE = '\(.*?\)'
MATCH_EDGE = '<?-?\[.*?\]-?>?'
PARSE_GRAPH_EXPRESSION = re.compile(
    '(?P<node>{})|(?P<edge>{})'.format(MATCH_NODE, MATCH_EDGE))


# TODO ONE BIG VALIDATION REGEX

class EdgeDirections(Enum):
    left = 1
    right = 2


# TODO flags -> convert to number; find all matches
# TODO use \w ?? or \S
IDENTIFIER_REGEX = re.compile('^(\w+)(?:|\s)?')
VARIABLE_REGEX = re.compile('\w+(\.\w+)*(?:|\s)?')

# Match labels, without matching properties
LABELS_REGEX = re.compile('[\w:]*?:([\w_]+)(?:|\s)?')

# TODO allowed_val_chars = '\w|\''
PROPERTIES_BODY_REGEX = re.compile('{(.*?)}')
KEY = '(?P<key>\w+)'
VAR = '(?P<var>\w+(\.\w+)*)'
NUM = '(?P<num>[\d.]+)'
STR = '("(?P<val>(.+?))")'
# Matches item sequentianally by their type
PROPERTY_REGEX = re.compile('{}:\s*({}|{}|{}),?\s*'.format(KEY, NUM, VAR, STR))

BODY_REGEX = '(.*?)'
EDGE_BODY_REGEX = re.compile('<?-\[{}\]->?'.format(BODY_REGEX))
NODE_BODY_REGEX = re.compile('\({}\)'.format(BODY_REGEX))


# TODO FIX
# TODO caseInsensitive
def split_list(unsplitted, sep_list):
    """
    Splits a string by list of separators
    """
    # TODO make it case insensitive
    splitted = re.split('\s*({})\s+'.format('|'.join(sep_list)),
                        unsplitted)

    if len(splitted) > 0 and not splitted[0]:
        splitted = splitted[1:]
    return splitted


# -- EXPRESSIONS --

MATCH_SPLITTERS = ['-']
MULTI_ELEMENTS_SPLITTER = [',']

'''
   ** PARSER **
'''


def check_valid_edge(raw_node):
    # XXX
    # TODO FIX
    # XXX
    error = None

    if error:
        raise InvalidEdgeError(raw_node, error)


def check_valid_node(raw_node):
    # XXX
    # TODO FIX
    # XXX
    error = None

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

        def is_int(n):
            try:
                int(n)
            except ValueError:
                return False
            return float(n) == int(n)

        if is_int(s):
            return int(s)
        else:
            try:
                return float(s)
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
            if match.group('var'):
                # it's an identifier
                var = match.group('var').split('.')
                value = Identifier(name=var[0],
                                   fields=var[1:])
            elif match.group('num'):
                # try to parse it to string
                value = to_number(match.group('num').strip())
            elif match.group('val'):
                # it's just a string
                value = to_number(match.group('val').strip())
            else:
                raise InvalidGraphExpressionPropertiesError(raw_props)

            properties.append(Property(key=key, value=value))

            match = PROPERTY_REGEX.match(raw_props, match.end())

    return tuple(properties)


def get_labels(raw_elem, multi=True):
    """
     ;id {};id:... {}
    Args:
        raw_elem (str):
        multi (bool):
    Returns:
        List[Label]:
    """
    matches = []
    # NOTE Use match to match the begging.
    match = LABELS_REGEX.match(raw_elem)
    while match:
        matches.append(match.group(1))
        match = LABELS_REGEX.match(raw_elem, match.end())

    # edge labels
    if matches and (len(matches) > 1 and not multi):
        raise InvalidLabelsCountError()
    # Make to system labels
    matches = tuple(Label(raw_label.strip()) for raw_label in matches)
    if not multi:
        # Is edge label
        return matches[0] if matches else None
    else:
        return matches

# ## TODO ONLY ONE INSTANCE
# def get_identifier_by_name(name):
#             """Keep only one identifier instance by name."""
#             identifier = identifiers.get(name)
#             if not identifier:
#                 identifier = Identifier(name=name)
#                 # add to existing
#                 identifiers[name] = identifier
#             return identifier
#
#         def get_variable(raw_elem):
#             """
#              ;id {};id:... {}
#             Args:
#                 raw_node (str):
#             Returns:
#                 Variable|None:
#             """
#             match = VARIABLE_REGEX.match(raw_elem)
#             if match:
#                 match = match.group(0).split('.')
#                 id = get_identifier_by_name(match[0])
#                 fields = match[1:]
#                 match = Variable(identifier=id, fields=fields )
#             return match

def get_variable(raw_elem):
    """
    Args:
        raw_elem (str):
    Returns:
        List[str]
    """
    match = VARIABLE_REGEX.match(raw_elem)
    if match:
        # separate the properties
        match = match.group(0).split('.')
        match = Variable(name=match[0], fields=match[1:])
    return match


def get_identifier(raw_elem):
    """
     ;id {};id:... {}
    Args:
        raw_node (str):
    Returns:
        Identifier|None:
    """
    match = VARIABLE_REGEX.match(raw_elem)
    if match:
        match = match.group(0).split('.')
        match = Identifier(name=match[0], fields=match[1:])
    return match


def parse_node(raw_node):
    """
    Node must follow the pattern: ([identifier][:label:label...] [{properties}])
    Args:
        raw_node (str): (data)
    Returns:
        Node:
    Raises:
        InvalidNodeError:
    """
    check_valid_node(raw_node)
    raw_node_body = NODE_BODY_REGEX.match(raw_node)
    if raw_node_body:
        raw_node_body = raw_node_body.group(1).strip()
    else:
        raise InvalidEdgeError(raw_node)

    identifier = get_identifier(raw_node_body)
    labels = get_labels(raw_node_body)
    properties = get_properties(raw_node_body)

    return Node(identifier=identifier, labels=labels, properties=properties)


def parse_edge(raw_edge, node_left, node_right):
    """
    Args:
        raw_edge (str): -[]-, <-[]-, ...
        node_left (Node):
        node_right (Node):
    Returns:
        Edge:
    """

    def get_edge_direction(raw_edge):
        # TODO raise on bad direction ...
        if raw_edge[0] == '<':
            return EdgeDirections.left
        elif raw_edge[len(raw_edge) - 1] == '>':
            return EdgeDirections.right
        return None

    check_valid_edge(raw_edge)
    raw_edge_body = EDGE_BODY_REGEX.match(raw_edge)
    if raw_edge_body:
        raw_edge_body = raw_edge_body.group(1).strip()
    else:
        raise InvalidEdgeError(raw_edge)

    identifier = get_identifier(raw_edge_body)
    label = get_labels(raw_edge_body, False)
    properties = get_properties(raw_edge_body)
    direction = get_edge_direction(raw_edge)

    if direction == EdgeDirections.left:
        # Swap edges to keep the proper ordering
        # simplifies the code
        node_left, node_right = node_right, node_left

    return Edge(identifier=identifier,
                label=label,
                properties=properties,
                directed=bool(direction),
                node_in=node_left,
                node_out=node_right)


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
    def collect_elements(raw_simple_expr):
        raw_nodes = []
        raw_edges = []

        match = PARSE_GRAPH_EXPRESSION.match(raw_simple_expr)
        while match:
            if match.group('node'):
                raw_nodes.append(match.group('node'))
            elif match.group('edge'):
                raw_edges.append(match.group('edge'))
            else:
                raise BadGraphExpressionElementError(match.group())
            match = PARSE_GRAPH_EXPRESSION.match(raw_simple_expr, match.end())

        return {'nodes': raw_nodes, 'edges': raw_edges}

    raw_elements = collect_elements(raw_simple_expr)

    # TODO check number of nodeshttps://gist.github.com/mkaz/141394d9ee97bed99121

    # Parse nodes
    nodes = [parse_node(raw_node) for raw_node in raw_elements['nodes']]

    edges = []

    # Parse edges
    for raw_edge, edge_nodes in zip(raw_elements['edges'],
                                    utils.pairwise(nodes)):
        edges.append(parse_edge(raw_edge, edge_nodes[0], edge_nodes[1]))

    res = None
    if edges:
        res = tuple(edges)
    elif nodes:
        if len(nodes) > 1:
            raise InvalidGraphExpressionError
        res = nodes[0]

    return SimpleGraphPatternExpression(res)

def optimize_identifiers(expr):
    """Reuse same identifier objects for different elements."""
    return expr

#######################################################################
#                         Expressions parsing                         #
#######################################################################

def parse_generic_expression(raw_subexprs):
    """
    Args:
        raw_subexprs (List[str]):
    Returns:
        GenericExpression:
    """

    def parse_generic_subexpression(subexpession):
        # TODO more cases
        return get_identifier(subexpession)

    generic_subexpressions = \
        tuple(parse_generic_subexpression(expr) for expr in raw_subexprs)
    return GenericExpression(generic_subexpressions)


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
    simple_graph_exprs = tuple(parse_simple_graph_expr(simple_expr)
                               for simple_expr in simple_graph_exprs)

    return GraphPatternExpression(simple_graph_exprs)


def parse_operator_expression(simple_graph_exprs):
    # TODO
    pass


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
    elif expression_type == GenericExpression:
        parser = parse_generic_expression
    else:
        raise UnsupportedExpressionType(expression_type)

    expression = optimize_identifiers(expression)

    return parser(expression)


def parse_clause(raw_clause):
    """

    Args:
        raw_clause (List[srt]): [clause, expr]

    Returns:
        Clause: The generated clause
    """
    clause_str, expr = raw_clause

    clause_type = get_clause_type(clause_str)

    expr = parse_expression(expr,
                            clause_type.get_expression_type())
    return clause_type(expr)


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
            clause = raw_sub_query[0]
            subclauses_split = split_list(raw_sub_query[1], SUB_CLAUSES)

            #  process expressions (of MATCH, WHERE, ...
            # TODO expression type is defined by the clause it refers to -- use that cluase
            subclauses = (parse_clause(clause)
                          for clause in
                          utils.pairize((clause, *subclauses_split)))

            return SubQuery(subclauses)

        # Process query by parts.
        # Sub queries are defined by specific Clauses

        # TODO trailing spaces
        sub_queries_str = utils.pairize(split_list(query, MAIN_CLAUSES))

        sub_queries = [parse_sub_query(sub_query) for sub_query in
                       sub_queries_str]
        # TODO parse to Query object ?

        # TODO - go through the sub_queries and apply matching variables
        ##apply_variables(sub_queries)

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
