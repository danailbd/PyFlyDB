from .base import StoreBase


"""
TODO: add timestamp to records on write
"""


class NodeStoreElement:
    def __init__(self, edge_in, edge_out, first_property, label, id=None):
        self.id = id
        self.edge_in = edge_in
        self.edge_out = edge_out
        self.property = first_property
        self.label = label


class NodeStore(StoreBase):
    """
    This class handles management of node storing on disk
    Nodes of
    """
    def __init__(self, file_name):
        element_size = 8
        super().__init__(self, file_name, element_size)

    def encode_element(self, element):
        """
        Args:
            element (tuple(int)):
        """

        edge_in = self.encode_int(element.edge_in)
        edge_out = self.decode_int(element.edge_out)
        fproperty = self.encode_int(element.firstproperty)
        label = self.encode_int(element.label)

        return edge_in + edge_out + fproperty + label

    def decode_element(self, byte_string):
        pass


class EdgeStoreElement:
    def __init__(self, node_out, node_in, label,
                 property, next_edge_in, next_edge_out, id=None):
        self.id = id
        self.node_out = node_out
        self.node_in = node_in
        self.property = property
        self.next_edge_in = next_edge_in
        self.next_edge_out = next_edge_out
        self.label = label


class EdgeStore(StoreBase):
    pass


class PropertySore(StoreBase):
    pass


class LabelStore(StoreBase):
    pass
