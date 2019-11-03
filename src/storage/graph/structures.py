
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
