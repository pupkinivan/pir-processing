""" Utitilies for reading low level data types and processing absolute paths."""

from functools import reduce
import os
import struct
from typing import List, Tuple, Union


def expand_absolute_path(absolute_path: Union[str, os.PathLike]):
    """Expand a path."""
    return os.path.abspath(os.path.expanduser(os.path.expandvars(absolute_path)))


def inverted_bytes_to_int(byte_array: List[bytes]):
    """Transform a list of bytes which carries a little endian? into an int"""

    def reduce_function(accumulator_tuple: Tuple[int, int], byte: bytes):
        """The tuple carries the index in the first element and the cumulative
        value in the second one."""
        return accumulator_tuple[0] + 1, accumulator_tuple[1] + byte * (
            16 ** (2 * accumulator_tuple[0])
        )

    return reduce(reduce_function, byte_array, (0, 0))[1]


def read_float_little_endian(file_object):
    """Read four bytes from a file object as a little endian float."""
    return struct.unpack("<f", file_object.read(4))[0]


def read_int_little_endian(file_object):
    """Read four bytes from a file object as a little endian int."""
    return struct.unpack("<i", file_object.read(4))[0]
