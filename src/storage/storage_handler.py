from graph.storage_handler import StorageHandler


class Node:
    def __init__(self, label, properties, v_in, v_out, unique_id=None):
        self.__unique_id = unique_id
        self.label = label
        self.properties = properties
        self.v_in = v_in
        self.v_out = v_out


class Edge:
    def __init__(self, labels, properties, unique_id=None):
        self.__unique_id = unique_id
        self.labels = labels
        self.properties = properties


class StorageManager:
    def __init__(self, *args, **kwargs):
        self.storage = StorageHandler(*args, **kwargs)

    def get_neighbouring_nodes(**kwargs):
        """
        Args:
            node (Node): used to filter of Vertice
            relationships (List<Edge>): types of *relationships* used
                                        to filter out neighbours
            properties (Dict): used to filter out neighbours
            labels (List<String>): used to filter out neighbours
        Returns:
            list(Node): returns a list of neighbouring nodes
        """

    def get_nodes(**kwargs):
        """
        Args:
            properties (Dict)
            label (List<String>)
        Returns:
            list(Node): Retruns a list of nodes that correspond to
                        the given properties and labels
        """

    def get_edges(self):
        pass

    def add_node(self):
        pass

    def add_edge(self):
        pass

    def update_node(self):
        pass

    def update_edge(self):
        pass

    def delete_node(self):
        pass

    def delete_edge(self):
        pass
