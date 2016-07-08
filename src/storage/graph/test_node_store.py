import unittest
import struct
import node_store
import shutil
from .structures import Node


class TestNodeAPI(unittest.TestCase):
    def setUp(self):
        self.file_name = "nodes"
        with open(self.file_name, 'w'):
            pass

    def tearDown(self):
        pass

    def test_get_first_free_bit(self):
        self.assertEqual(get)

    def test_save_node(self):
        write_info = struct.pack('i', 1, 0, 0)
        node = Node()
