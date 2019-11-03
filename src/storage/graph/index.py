from base import (FileManagementMixin,
                  GlobalAllocationMapMixin,
                  FileIOMixin)


class BNodeKey:
    def __init__(self, property, value):
        self.property = self.property
        self.value = self.value

    def __lt__(self, other):
        if self.key < other.key:
            return True
        if self.key == other.key:
            return self.value < other.key
        return False

    def __le__(self, other):
        if self.key < other.key:
            return True
        if self.key == other.key:
            return self.value <= other.value
        return False

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value


class BNode:
    def __init__(self, node_size, contents=None,
                 children=None, null_value=None):
        self.null_value = null_value
        self.node_size = node_size
        self.contents = contents or (null_value,) * self.node_size
        self.children = children or (null_value,) * self.node_size
        self.is_leaf = False

    def free_space(self):
        return self.children.count(self.null_value)

    def find_child(self, element):
        index = 0
        for index, key in enumerate(self.contents):
            if element.key < key:
                return self.children[index]
        return self.children[index+1]

    def insert(self, element, left_child=None, right_child=None):
        pass

    def split(self):
        middle = self.node_size // 2
        mid_element = self.contents[middle]
        left_content = self.contents[0:middle] + \
            (self.null_value,) * (self.node_size - middle)

        left_children = self.children[0:middle] + \
            (self.null_value,) * (self.node_size - middle + 1)

        right_content = self.contents[middle+1:self.node_size] + \
            (self.null_value,) * (self.node_size - middle)

        right_children = self.contents[middle:self.node_size+1] + \
            (self.null_value,) * (self.node_size - middle + 1)

        left = BNode(self.node_size, left_content,
                     left_children, self.null_value)
        right = BNode(self.node_size, right_content,
                      right_children, self.null_value)
        return (left, right, mid_element)

    def insert_split(self, element):
        self.insert(element)
        return self.split()

    def insert_shrink_from_left(self, element):
        self.insert(element)

    def insert_shrink_from_right(self, element):
        pass


class BPlusNode(BNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def find_child(self, element):
        for key in self.contents:
            if key == element:
                return element

    def change_brother(self, brother):
        self.children[self.node_size+1] = brother

    def insert(self, element):
        pass

    def insert_shrink_from_left(self, element):
        pass

    def insert_shrink_from_right(self, element):
        pass


class BTree(FileManagementMixin, GlobalAllocationMapMixin, FileIOMixin):

    DEFAULTS = {
        'node_size': 10
    }

    def __init__(self, root=None, **kwargs):
        """
        If root is not given and custom settings are
        needed supply the given key word arguments
        given bellow

        Args:
            root (BNode): root of the b-tree
            node_size (int): number of keys in a node
        """
        self.root = root or self._new_root(**kwargs)

    def insert(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass
