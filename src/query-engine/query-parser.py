import re
import collections
import itertools


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

    splitter = sep_list[0]
    rest = sep_list[1:]

    if isinstance(unsplitted, list):
        splitted_list = []
        for sub_str in unsplitted:
            splitted_com = sub_str.split(splitter)
            if len(splitted_com) > 0:
                apply_notation(splitted_com, splitter)

            splitted_list.append(splitted_com)
            unsplitted = list(itertools.chain(*splitted_list))
    else:
        unsplitted = unsplitted.split(splitter)
        apply_notation(unsplitted, splitter)

    return split_list(unsplitted, rest)


class InvalidSyntaxError(Exception):
    pass


class Command:

    """ Defines a basic command for the db (MATCH, WHERE, ...) """

    def __init__(self, clause, expression):
        """TODO: to be defined1.

        Args:
            clause (Clause): TODO
            expression (Expression): TODO


        """
        self._clause = clause
        self._expression = expression
        
 
class SubQuery:

    """Docstring for QueryModel. """

    def __init__(self, commands)
        """TODO: to be defined1.

        Args:
            commands (List[Command]):
        """
        self._commands = commands
               

class Query:

    """Docstring for Query. """

    def __init__(self, queries):
        """
        Defines a whole query.

        Args:
            queries (List[SubQuery]):
        """
        self._queries = queries
        


def sytax_check(query):
    '''
    TODO
    Some big regex to check for proper syntax
    '''
    pass



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

# -- EXPRESSIONS --

MATCH_SPLITTERS = ['-']
MULTI_ELEMENTS_SPLITTER = [',']


OPERATORS_BY_PRIORITY = ['OR', 'XOR', 'AND', 'OR', '>', '<', '<=', '>=', 'IN']
ops = {
    'or': Operator('or', lambda a, b: a || b)
}

COMMANDS = {}


class NumberOfOperandsError(Exception):
    pass

class InvalidOperationError(Exception):
    pass


class Literal(object):

    """Defines a literal for an expression."""

    def __init__(self, value):
        """TODO: to be defined1.

        Args:
            value (any): TODO
        """
        self._value = value


class Identifier:
    """
    Defines an identifier for a query. It can be
    specified by name and populated on sub-query execution.
    """
    def __init__(self, letter, value=None):
        self._letter = letter
        self._value = value

    @property
    def value(self):
        return self._value


class Operator:
    def __init__(self, op, processor, operands=0):
        self.operation = op
        self.priority = priority
        self.processor = processor
        self.operands = operands

    def execute(*args):
        '''
        Pass the required number of operands to the
            operator
        '''
        return self.processor(*args)


class Expression:

    '''
    A where (and other elements?) expression handler
    Contains a list of elements - variables, consts and operations
    '''

    def __init__(self, elements):
        self.elements = elements

    # TODO probably not ...
    def validate_expression(self):
        pass


class Edge:

    """
    TODO: make it immutable
    An edge:
        - has label
        - identifier - used to keep the name of the matched edge
        - has [properties]
        - direction - true/false
        - nodeIn, nodeOut - in case a direction if given, the edge direction
        is determined from the node sequence given
        """

    def __init__(self, label, nodeIn, nodeOut, direction, identifier=None, properties={}):
        self.__label = label
        self.__properties = properties
        self.__nodeIn = nodeIn
        self.__nodeOut = nodeOut
        self.__directed = directed
        self.identifier = identifier

    def isDirected(self):
        return self.direction

    def getNodes(self):
        """
        Get a directed node pair out - in (direction flag needed)
        """
        return (self.nodeOut, self.nodeIn)

    def getLabel(self):
        return self.__label

    def getProperties(self):
        return self.__properties


class ReturnEdge(Edge):

    """
    A returned edge must have an identifier, if not
    it shouldn't be returned.
    """

    def __init__(self, direction, label, nodeLeft, nodeRight, _id, identifier, properties):
        Edge.__init__(self, label, properties)
        self.__id = _id

        # TODO implement setters


class Node:

    """
    TODO: make it immutable
    A node:
        - identifier -- used to define the result variable
        - has label/s
        - has [properties]
        """

    def __init__(self, labels, identifier=None, properties={}):
        self.identifier = identifier
        self.labels = labels
        self.properties = properties


class ReturnNode(Node):

    def __init__(self, identifier, _id, properties, labels=[]):
        Node.__init__(self, identifier, properties, labels)
        self.__id = _id


class QueryParser:
    """
    Creates a Query object out of a query string.
    """

    @staticmethod
    def parse_query(query):
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
            varibalbe_str = re.search('[^(]\w*(\)|\{))]', node_string)
            return varibalbe_str.group(0).split(':') if varibalbe_str else None

        def __parse_node(node_string):
            """
            Accepts (var:label {})

            Do paring of string to node data and
            return Node Object
        """
        properties = __get_properties(node_string)
        labels = __get_labels(__parse_node)

        def __parse_edge(self, node_string):
            """
            An edge can
            Returns an edge with specified properties and orientation.
            """
            properties = __get_properties(node_string)
            labels = __get_labels(__parse_node)

        def parse_expression(expression_string, expression_type):


        def parse_sub_query(sub_query):
            # Break to smaller parts with sub clauses - RETURN, WHERE
            # List of: Clause, expressions (, separated)
            clauses_split = split_list(query_part, SUB_CLAUSES)
            # process expressions (of MATCH, WHERE, ...

# TODO expression type is defined by the clause it refers to -- use that cluase
            expressions_split = parse_expression(sub_split)

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

        Returns a list:
            [ [operation, [*args]], - the comma separated elements
            [ops, [*args], ...]
            [ [MATCH, Node, edge, ...] ..]
            """

        # Process query by parts.
        # Sub queries are defined by specific Clauses
        sub_queries = split_list(query, MAIN_CLAUSES)

        parsed_sub_queries = [parse_sub_query(sub_query) for sub_query in sub_queries]

        return parsed_sub_queries
# TODO variables ???

    @staticmethod
    def __execute_command(command, *args):
        # use commands dict
        pas
            command = op[0]
            subcommands = op[1:]
            QueryEngine.__execute_command(op, *subcommands)


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
