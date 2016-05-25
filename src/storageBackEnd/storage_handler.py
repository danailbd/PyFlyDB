from .relationalDB.sqlhandler import SqlHandler

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
        self.storage = SqlHandler(*args, **kwargs)

    def get_neighbouring_nodes(vertice, **kwargs):
        """
        Args:
            node (Node): used to filter of Vertice 
            relationships (List<Edge>): types of *relationships* used to filter out neighbours 
            properties (Dict): used to filter out neighbours
            labels (List<String>): used to filter out neighbours 
        """
        pass


    def get_nodes(**kwargs):
        """
        Args:
            properties (Dict)
            label (List<String>)
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
