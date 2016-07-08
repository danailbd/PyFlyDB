import struct


class FormatStringNotSupportedError(Exception):
    def __init__(self, format_string):
        self.message = "Format string: '{}' not supported".format(format_string)

    def __str__(self):
        return self.message


class FormatStringError(Exception):
    def __init__(self, format_string, table_length, map_size):
        self.message = "Format string '{format_string}' byte size " \
                       "and table length:{table_length} " +\
                       "do not match allocation map size {map_size}"

        self.kwargs = {'format_string': format_string,
                       'table_length': table_length,
                       'map_size': map_size}

    def __str__(self):
        return self.message.format(**self.kwargs)


class GlobalAllocationMapMixin:
    """
    This class defines basic functionality
    for global allocation maps keeping
    track and managing empty blocks in a file
    """

    # format strings defined in python docs for more information:
    # https://docs.python.org/3/library/struct.html#format-characters
    FORMAT_STRING_SIZES = {
        'q': 8,  # long long, 8 bytes
        'i': 4,  # int , 4 bytes
        'h': 2,  # short, 2 bytes
        'b': 1,  # signed char , 1 byte
        }

    def create_empty_table(self, number_of_elements):
        return (0 for i in range(number_of_elements))

    def create_binary_table(self, table=None, format_type='b'):
        """
        Args:
            table (iterable(int)): representing the information in the allocation map
            format_type (string): one char contained in FORMAT_STRING_SIZES class variable
                                  defining the way data should be packed

        Returns:
            bytes: the information given in table ready
                   to be writen in a binary file
        """
        element_size = self.__class__.FORMAT_STRING_SIZES.get(format_type)
        number_of_elements = self.allocation_map_size / element_size

        if number_of_elements != len(table):
            raise

        if not element_size:
            raise FormatStringNotSupportedError(format_type)
        if not table:
            table = self.create_empty_table(number_of_elements)

        format_string = format_type * number_of_elements

        return struct.pack(format_string, *table)

    def get_free_blocks(self, table, number_of_needed_blocks):
        """
        Takes an allocation map
        Args:
            table (iterable(int)): representing the information in the allocation map
                                   should be an integer in [-128;127] range
            number_of_needed_blocks (int): how many free blocks are needed
        Returns
            list(int): numbers of free blocks
        """
        offset = 128
        result = []
        for byte in enumerate(table):
            byte += 128
            if byte == 255:
                continue
            free_blocks = self.free_bits[byte]
            while len(result) < number_of_needed_blocks and free_blocks:
                result.append(free_blocks.pop(0))

            if len(result) >= number_of_needed_blocks:
                break

        return result


class FileIOMixin:
    """
    This class defines basic functionality for handling
    reading and writing to a binary file
    """

    def read_bytes(self, place, size):
        with open(self.file_name, "rb") as f:
            f.seek(place)
            info = f.read(size)

        return info

    def write_bytes(self, info, place):
        with open(self.file_name, "wb") as f:
            f.seek(place)
            f.write(info)


class FileManagementMixin:
    """
    This class defines functionality for manging data location in files
    """

    def get_allocation_map_place(self, sequence_number):
        return sequence_number * self.allocation_map_size * (1 + self.element_size)

    def get_element_place(self, sequence_number):
        offset_form_page_begining = sequence_number % self.allocation_map_size * self.element_size
        page_number = sequence_number // self.allocation_map_szie
        offset_from_file_begining = page_number * self.allocation_map_size * (1 + self.element_size)
        return offset_form_page_begining + offset_from_file_begining


class StoreBase():
    """
    This class is the base for the node, edge and property store classes.
    It defines basic file structure and
    API for saving, retrieving and updating data.
    """

    def __init__(self, file_name, element_size, allocation_map_size=1024):
        self.file_name = file_name
        self.element_size = element_size
        self.allocation_map_size = allocation_map_size

    def create_table(self, table=None, format_string='q', ):
        if not table:
            table = tuple(0 for i in range(8))

        format_string = format_string * len(table)

        return struct.pack(format_string, *table)

    def get_table(self, page):
        with open(self.file_name, 'r') as f:
            pass
