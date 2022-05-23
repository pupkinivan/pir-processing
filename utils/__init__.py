import os
import struct
from functools import reduce


def expand_absolute_path(absolute_path: str | os.PathLike[str]):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(absolute_path)))

def inverted_bytes_to_int(byte_array: list[bytes]):
    def reduce_function(accumulator_tuple: tuple[int, int], byte: bytes):
        """ The tuple carries the index in the first element and the cumulative value in the second one. """
        return accumulator_tuple[0] + 1, \
               accumulator_tuple[1] + byte * (16 ** (2 * accumulator_tuple[0]))

    return reduce(reduce_function, byte_array, (0, 0))[1]


def read_float_little_endian(file_object):
    return struct.unpack("<f", file_object.read(4))[0]


def read_int_little_endian(file_object):
    return struct.unpack("<i", file_object.read(4))[0]
