class Node:
    def __init__(self, label, properties, v_in, v_out, unique_id=None):
        self.__unique_id = unique_id
        self.label = label
        self.properties = properties
        self.v_in = v_in
        self.v_out = v_out


class Vertice:
    def __init__(self, labels, properties, unique_id=None):
        self.__unique_id = unique_id
        self.labels = labels
        self.properties = properties


def get_neighbouring_nodes(vertices, **kwargs):
    """
    Args:
        verices (List)
        list of *relationship* types,
        list of *properties*
        list of *labels*
        and a *groupby* variable
        which represents the key by which returned nodes should be grouped
        by default - the key is relationship
    """
    pass


def get_nodes(**kwargs):
    """
    recieves a list of *properties*
    list of *labels*
    list of *names*
    and a *groupby* variable
    which represents the key by which returned nodes should be grouped
    by default - the key is relationship
    """
    pass


def get_edges():
    pass


def add_node():
    pass


def add_edge():
    pass


def update_node():
    pass


def update_edge():
    pass


def delete_node():
    pass


def delete_edge():
    pass
