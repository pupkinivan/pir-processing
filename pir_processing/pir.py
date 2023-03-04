""" Module for PIR data class and utility classes for reading and processing files."""

from dataclasses import dataclass
from typing import List

import numpy as np

from pir_processing.utils import (
    expand_absolute_path,
    read_float_little_endian,
    read_int_little_endian,
)


@dataclass
# pylint: disable=too-many-instance-attributes
class PirFile:
    """Data class for storing a PIR file metadata."""

    file_signature: List[bytes]
    unsigned_int_version: int
    info_size: int
    reserved_1: int
    reserved_2: int
    sample_rate_float: float
    sample_rate_int: float
    pir_length: int
    input_device: int
    device_sensitivity: float
    measurement_type: int
    averaging_type: int
    number_of_averages: int
    bfiltered: int
    generator_type: int
    peak_left: float
    peak_right: float
    generator_subtype: int
    cursor_position: int
    marker_position: int
    reserved_3: float
    reserved_4: float
    pir_data: List[float]
    info_text: str

    @classmethod
    # pylint: disable=too-many-locals
    def from_file_path(cls, path_to_pir_file):
        """Factory method for reading a PIR file from a given path."""

        # Initialize nullables
        cursor_position = None
        marker_position = None
        reserved_3 = None
        reserved_4 = None

        absolute_path = expand_absolute_path(path_to_pir_file)

        with open(absolute_path, "rb") as file:
            file_signature = [bytes(file.read(1)) for i in range(4)]
            unsigned_int_version = read_int_little_endian(file)
            info_size = read_int_little_endian(file)
            reserved_1 = read_int_little_endian(file)
            reserved_2 = read_int_little_endian(file)
            sample_rate_float = read_float_little_endian(file)
            sample_rate_int = read_int_little_endian(file)
            pir_length = read_int_little_endian(file)
            input_device = read_int_little_endian(file)
            device_sensitivity = read_float_little_endian(file)
            measurement_type = read_int_little_endian(file)
            averaging_type = read_int_little_endian(file)
            number_of_averages = read_int_little_endian(file)
            bfiltered = read_int_little_endian(file)
            generator_type = read_int_little_endian(file)
            peak_left = read_float_little_endian(file)
            peak_right = read_float_little_endian(file)
            generator_subtype = read_int_little_endian(file)

            if unsigned_int_version >= 5:
                cursor_position = read_int_little_endian(file)
                marker_position = read_int_little_endian(file)
            else:
                reserved_3 = read_float_little_endian(file)
                reserved_4 = read_float_little_endian(file)

            pir_data = [read_float_little_endian(file) for i in range(pir_length)]
            info_text = "".join(file.read())

        return cls(
            file_signature=file_signature,
            unsigned_int_version=unsigned_int_version,
            reserved_1=reserved_1,
            reserved_2=reserved_2,
            info_size=info_size,
            sample_rate_float=sample_rate_float,
            sample_rate_int=sample_rate_int,
            pir_length=pir_length,
            input_device=input_device,
            device_sensitivity=device_sensitivity,
            measurement_type=measurement_type,
            averaging_type=averaging_type,
            number_of_averages=number_of_averages,
            bfiltered=bfiltered,
            generator_type=generator_type,
            peak_left=peak_left,
            peak_right=peak_right,
            generator_subtype=generator_subtype,
            pir_data=pir_data,
            info_text=info_text,
            cursor_position=cursor_position,
            marker_position=marker_position,
            reserved_3=reserved_3,
            reserved_4=reserved_4,
        )

    def get_time_vector(self):
        """Generate time instants for the impulse response."""
        return [i / self.sample_rate_int for i in range(len(self.pir_data))]

    def get_ir(self):
        """Get an IR along with its time instants."""
        return np.array(
            [
                self.get_time_vector(),
                self.pir_data,
            ]
        ).T

    def get_pir_data(self):
        """Get an IR by itself (no time axis)."""
        return self.pir_data

    def get_sample_rate(self):
        """Get the sample rate of the measurement."""
        return self.sample_rate_int
