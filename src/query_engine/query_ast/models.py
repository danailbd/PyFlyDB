from src.lib.utils import ensure_array


class Literal:
    """Defines a literal for an expression."""

    def __init__(self, value):
        """
        Args:
            value:
        """
        self._value = value

    def __repr__(self):
        return self._value

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Property:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return self.key + ':' + str(self.value)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Identifier:
    """
    Defines an identifier for a query. It can be
    """

    def __init__(self, letter, value=None):
        """
        Args:
            letter:
            value:
        """
        self._letter = letter
        self._value = value

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return self._letter + ' ' + self._value

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Label:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


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

    def __init__(self, node_in=None, node_out=None, label='', directed=False,
                 identifier=None,
                 properties=()):
        """
        Args:
            label:
            node_in:
            node_out:
            directed:
            identifier:
            properties:
        """
        self.__label = label
        self.__properties = ensure_array(properties)
        self.__node_in = node_in
        self.__node_out = node_out
        self.__directed = directed
        self.identifier = identifier

    def __repr__(self):
        return self.identifier + ':' + self.__label + \
               ' ' + self.__properties + ' ' + self.__node_in + \
               ' ' + self.__node_out + ' ' + str(self.__directed)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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

    def __init__(self, direction, label, nodeLeft, nodeRight, _id, identifier,
                 properties):
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

    def __init__(self, labels=(), identifier=None, properties=()):
        self.identifier = identifier
        self.properties = ensure_array(properties)
        self.labels = ensure_array(labels)

    def __repr__(self):
        return self.identifier + ':' + self.labels + ' ' + self.properties

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ReturnNode(Node):
    def __init__(self, identifier, _id, properties, labels=[]):
        Node.__init__(self, identifier, properties, labels)
        self.__id = _id
