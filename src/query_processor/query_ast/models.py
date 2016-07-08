from src.lib.printable import Printable
from src.lib.utils import ensure_tuple


class PropertiesHolderMixin:
    def properties_as_dict(self):
        props = {}
        for prop in self.properties:
            props[prop.key] = prop.value
        return props


class IdentifierHolderMixin:
    def get_identifiers(self):
        raise NotImplementedError()


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


class Property(Printable):
    def __init__(self, key, value):
        """
        Args:
            key:
            value (str|number|Identifier):
        """
        self.key = key
        self.value = value

    def __repr__(self):
        return '<Property><' + self.key + ': ' + str(self.value) + '>'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Identifier:
    """
    Defines an identifier for a query. It can be
    """

    def __init__(self, name=None, fields=(), value=None):
        """
        Args:
            letter:
            value:
        """
        self._name = name
        self._value = value
        self._fields = ensure_tuple(fields)

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name + '.' + '.'.join(self._fields) + ' ' + \
               str(self._value)

    def __repr__(self):
        return '<Identifier><' + str(self._name) + ' ' + str(self._value) + '>'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        # XXX it's a quick fix -- __hash__ must be compatible with __eq__
        return id(self)


class Variable:
    """Keeps data about referenced identifiers."""

    def __init__(self, identifier, fields):
        """
        Args:
            name (str):
            fields (List[str]): represents the variable properties
            sequence -> a.b.c -> [b, c]
        """
        self.id = identifier
        self.fields = ensure_tuple(fields)


class Label:
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Edge(Printable, IdentifierHolderMixin, PropertiesHolderMixin):
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

    def __init__(self, node_in=None, node_out=None, label=None,
                 directed=False, identifier=None, properties=()):
        """
        Args:
            label:
            node_in (Node):
            node_out (Node):
            directed (bool|str): left or right directed
            variable (Identifier|Variable):
            properties:
        """
        self.__label = label
        self.__properties = ensure_tuple(properties)
        self.__node_in = node_in
        self.__node_out = node_out
        self.__directed = directed
        self.identifier = identifier

    def __repr__(self):
        return '<Edge>[' + str(self.identifier) + ':' + \
               str(self.__label) + ' { ' + str(self.__properties) + ' } < ' + \
               str(self.__node_in) + ' > < ' + str(self.__node_out) + ' > - ' + \
               str(self.__directed) + ']'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def is_directed(self):
        return self.__directed

    def get_nodes(self):
        """
        Get a directed node pair out - in (direction flag needed)
        """
        return (self.__node_in, self.__node_out)

    def get_identifiers(self):
        ids = []
        if self.identifier:
            ids.append(self.identifier)
        if self.__node_in and self.__node_in.get_identifiers():
            ids.append(*self.__node_in.get_identifiers())
        if self.__node_out and self.__node_out.get_identifiers():
            ids.append(*self.__node_out.get_identifiers())
        return ids

    @property
    def label(self):
        return self.__label

    @property
    def properties(self):
        return self.__properties


class ReturnEdge(Edge):
    """
    A returned edge must have an identifier, if not
    it shouldn't be returned.
    """

    def __init__(self, direction, label, nodeLeft, nodeRight, _id, variable,
                 properties):
        Edge.__init__(self, label, properties)
        self.__id = _id

        # TODO implement setters


class Node(Printable, IdentifierHolderMixin, PropertiesHolderMixin):
    """
    TODO: make it immutable
    A node:
        - identifier -- used to define the result variable
        - has label/s
        - has [properties]
    """

    def __init__(self, labels=(), identifier=None, properties=()):
        self.identifier = identifier
        self.properties = ensure_tuple(properties)
        self.labels = ensure_tuple(labels)

    def get_identifiers(self):
        return [self.identifier] if self.identifier else []

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ReturnNode(Node):
    def __init__(self, variable, _id, properties, labels=[]):
        Node.__init__(self, variable, properties, labels)
        self.__id = _id
