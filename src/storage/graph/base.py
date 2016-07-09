import struct


class StorageHandlingException(Exception):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return self.message.format(self.kwargs)


class FormatStringNotSupportedError(StorageHandlingException):
    def __init__(self, format_string):
        self.message = "Format string: '{format_sting}' not supported"
        super().__init__(self, self.message, format_string)


class FormatStringError(StorageHandlingException):
    def __init__(self, format_string, table_length, map_size):
        self.message = "Format string '{format_string}' byte size " \
                       "and table length:{table_length} " +\
                       "do not match allocation map size {map_size}"
        super().__init__(self, self.message, format_string,
                         table_length, map_size)


class BlockOutOfRangeError(StorageHandlingException):
    def __init__(self, block, allocation_map_size):
        self.message = "Block:{block} is greater than the " + \
                       "allocation map size:{allocation_map_size}"
        super().__init__(self, block, allocation_map_size)


class GlobalAllocationMapMixin:
    """
    This class defines basic functionality
    for global allocation maps keeping
    track and managing empty blocks in a file
    """

    def create_empty_table(self, number_of_elements):
        return (0 for i in range(number_of_elements))

    def get_free_blocks(self, table, number_of_needed_blocks):
        """
        Takes an allocation map
        Args:
            table (iterable(int)): representing the information in the
                                   allocation map should be an integer
                                   in range [-128;127]
            number_of_needed_blocks (int): how many free blocks are needed
        Returns
            list(int): numbers of free blocks
        """
        result = []
        for index, byte in enumerate(table):
            if byte == 255:
                continue
            free_blocks_in_byte = self.free_bits[byte]

            while free_blocks_in_byte:
                result.append(free_blocks_in_byte.pop(0))

                if len(result) >= number_of_needed_blocks:
                    break
            if len(result) >= number_of_needed_blocks:
                break

        bits_in_byte = 8
        offset = bits_in_byte * index

        return ((offset + bit) for bit in result)

    def get_block_location(self, block):
        if block >= self.allocation_map_size:
            raise BlockOutOfRangeError(block, self.allocation_map_size)

        byte = block // 8
        bit = block % 8

        return byte, bit

    def bit_flag(self, bit):
        flags = [128, 64, 32, 16, 8, 4, 2, 1]
        return flags[bit]

    def free_block(self, block, table):
        """
        Frees block by setting corresponding bit in map to 0
        Args:
            block (int): place of block in table
            table (list(int)): list from ints in range [-128;127]
                               each int represent a byte from the table

        raises BlockOutOfRangeError if the block number is higher
               than the allocation table max size
        """
        byte, bit = self.get_block_location(block)

        flag = self.bit_flag(bit)

        if table[byte] & flag == flag:
            table[byte] ^= flag

    def occupy_block(self, block, table):
        """
        Occupies a block by setting corresponding bit in map to 1
        Args:
            block (int): place of block in table
            table (list(int)): list from ints in range [-128;127]
                               each int represents a byte from the table

        raises BlockOutOfRangeError if the block number is higher than
               the allocation table max size
        """

        byte, bit = self.get_block_location(block)

        flag = self.bit_flag(bit)

        if table[byte] & flag == 0:
            table[byte] ^= flag


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


class DataConverterMixin:
    """
    This class provides functionality for converting
    data (int and string) to and from bytes of fixed size
    for reading, writing from a binary file
    """

    # format strings defined in python docs for more information:
    # https://docs.python.org/3/library/struct.html#format-characters
    FORMAT_TYPE_SIZES = {
        'q': 8,  # long long, 8 bytes
        'i': 4,  # int , 4 bytes
        'h': 2,  # short, 2 bytes
        'b': 1,  # signed char , 1 byte
    }

    INTEGER_OFFSET = {
        'q': 2 ** 63,
        'i': 2 ** 31,
        'h': 2 ** 15,
        'b': 2 ** 7
    }

    STRING_END = '~'  # represents end of string (e.g. '\0')

    def encode_string(self, string, size):
        """
        Args:
            string (str): string to be converted
            size (int): number of chars in string
        Returns:
            bytes object
        """
        number_of_null_symbols = size - len(string)
        null_symbols = self.__class__.STRING_END * number_of_null_symbols
        string += null_symbols
        return string.encode(encoding='ascii')

    def decode_string(self, bytes_string):
        string = bytes_string.decode(encoding='ascii')
        string_end = self.__class__.STRING_END
        return ''.join(char for char in string if char != string_end)

    def encode_int(self, value, format_type):
        """
        Args:
            value (int): the number to be converted
            format_type (string): one char representing the format string
                                  that will be used for the encoding and
                                  packing of the data in byte object
        Returns:
            bytes object

        Raises FormatStringNotSupportedError
        """
        if format_type not in self.__class__.FORMAT_TYPE_SIZES:
            return FormatStringNotSupportedError(format_type)

        return struct.pack(value, format_type)

    def decode_int(self, bytes_int, format_type):
        if format_type not in self.__class__.FORMAT_TYPE_SIZES:
            return FormatStringNotSupportedError(format_type)
        return struct.unpack(format_type, bytes_int)

    def encode_table(self, table=None, format_type='b'):
        """
        Args:
            table (iterable(int)): representing the information
                                   in the allocation map
            format_type (string): one char representing the format string
                                  that will be used for the encoding and
                                  packing of the data in byte object
        Returns:
            bytes: the information given in table ready
                   to be writen in a binary file

        Raises FormatStringError and FormatStringNotSupportedError
        """

        element_size = self.__class__.FORMAT_TYPE_SIZES.get(format_type)
        map_size_in_bytes = self.allocation_map_size / 8
        number_of_elements = map_size_in_bytes / element_size

        if number_of_elements != len(table):
            raise FormatStringError

        if not element_size:
            raise FormatStringNotSupportedError(format_type)
        if not table:
            table = self.create_empty_table(number_of_elements)

        format_string = format_type * number_of_elements

        return struct.pack(format_string, *table)

    def decode_table(self, table_byte_string, format_type='b'):
        format_string = format_type * self.allocation_map_size
        return struct.unpack(format_string, table_byte_string)


class FileManagementMixin:
    """
    This class defines functionality for manging data location in files
    """

    def get_allocation_map_place(self, sequence_number):
        maps_size_in_bytes = self.allocation_map_size / 8
        return sequence_number * maps_size_in_bytes * (1 + self.element_size)

    def get_element_place(self, sequence_number):
        maps_size_in_bytes = self.allocation_map_size / 8
        offset_form_page_begining = sequence_number % \
            maps_size_in_bytes * self.element_size

        page_number = sequence_number // maps_size_in_bytes
        offset_from_file_begining = page_number * \
            maps_size_in_bytes * (1 + self.element_size)

        return offset_form_page_begining + offset_from_file_begining


class StoreBase(GlobalAllocationMapMixin, FileIOMixin,
                FileManagementMixin, DataConverterMixin):
    """
    This class is the base for the node, edge and property store classes.
    It defines basic file structure and
    API for saving, retrieving and updating data.
    """

    def __init__(self, file_name, element_size, allocation_map_size=1024):
        """
        Args:
            file_name (string): path to file store
            element_size: size of elements
            allocation_map_size: size of global allocation map
        """
        self.file_name = file_name
        self.element_size = element_size
        self.allocation_map_size = allocation_map_size

    def encode_element(self, element):
        """
        Hook to encode custom elements to be writen to files
        """

    def decode_element(self, byte_string):
        """
        Hook to decode custom elements read from file
        """

    def add_element(self, element):
        """
        Hook to add an element
        Should return the id of the new element
        """

    def remove_element(self, element_id):
        """
        Hook to remove elements
        """

    def get_element(self, element_id):
        """
        Hook to access elements in store
        by a given id
        """
