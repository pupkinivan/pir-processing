import os
import numpy as np

import utils
from utils import expand_absolute_path, read_float_little_endian, read_int_little_endian


class PirFile:
    def __init__(
            self,
            file_signature: list[bytes],
            unsigned_int_version: int,
            info_size: int,
            reserved_1: int,
            reserved_2: int,
            sample_rate_float: float,
            sample_rate_int: float,
            pir_length: int,
            input_device: int,
            device_sensitivity: float,
            measurement_type: int,
            averaging_type: int,
            number_of_averages: int,
            bfiltered: int,
            generator_type: int,
            peak_left: float,
            peak_right: float,
            generator_subtype: int,
            pir_data: list[float],
            info_text: str,
            cursor_position: int | None = None,
            marker_position: int | None = None,
            reserved_3: float | None = None,
            reserved_4: float | None = None
    ):
        """
        Instantiate a PIR file data from all of its fields. In order to read from a given file, use the '.of(file_path)'
        factory method.

        Input parameters:
        :param file_signature: list[bytes], 'PIR'.encode('utf-8').hex() + '\0'.
        :param unsigned_int_version: int, int('0x0100').
        :param info_size: int, the length of the user-defined info at the end of the file.
        :param reserved_1: int, Reserved 1 = 0.
        :param reserved_2: int, Reserved 2 = 0.
        :param sample_rate_float: float, Sampling rate as a float in kilohertz, fs [kHz].
        :param sample_rate_int: float, Sampling rate as an int in Hertz, fs [Hz].
        :param pir_length: int, length of the PIR data per se.
        :param input_device: int, Type of the input device: 0 - voltage probe; 1 - mic; 2 - accelerometer
        :param device_sensitivity: float,device_sensitivity  # Device sensitivity [V/V or V/Pa] for microphone input
        :param measurement_type: int, 0 - Recorded signal (external excitation)
                                      1 - IR in single-channel mode
                                      2 - IR in dual-channel mode
        :param averaging_type: int, 0 - Time; 1 - Frequency
        :param number_of_averages: int, number of averages used in measurements
        :param bfiltered: int, forced antialiasing filtering in 2 ch
        :param generator_type: int. Generator types (gentype) are:
            - SIG_NONE 0
            - SIG_NOISE_WHITE 1
            - SIG_NOISE_PINK 2
            - SIG_RPMS_WHITE 3
            - SIG_RPMS_PINK 4
            - SIG_RPMS_SPEECH 5
            - SIG_SINE 6
            - SIG_SINE_TWO_FR 7
            - SIG_MULTITONE 8
            - SIG_TYPE_SQUARE 9
            - SIG_TYPE_TRIANGLE 10
            - SIG_TYPE_JITTER 11
            - SIG_TYPE_MLS 12
            - SIG_TYPE_SWEEP_LIN 13
            - SIG_TYPE_SWEEP_LOG 14
            - SIG_TYPE_PULSE 15
            - SIG_TYPE_BURST 16
        :param peak_left: float, peak value(ref. 1.0) in left input channel
        :param peak_right: float, peak value(ref. 1.0) in right input channel
        :param generator_subtype: int. Generator subtypes are defined for generator_type SIG_RPMS_SPEECH (5) as:
            - 0, male,
            - 1, female
        :param pir_data: list[float], IR data itself
        :param info_text: str, the user-defined text, of length info_size
        :param cursor_position: int | None = None, if unsigned_int_version >= 5, cursor position
        :param marker_position: int | None = None, if unsigned_int_version >= 5, marker position
        :param reserved_3: float | None = None, if unsigned_int_version < 5, reserved float
        :param reserved_4: float | None = None, if unsigned_int_version < 5, reserved float
        """
        self.__file_signature = file_signature
        self.__unsigned_int_version: int = unsigned_int_version
        self.__info_size: int = info_size
        self.__reserved_1: int = reserved_1
        self.__reserved_2: int = reserved_2
        self.__sample_rate_float: float = sample_rate_float
        self.__sample_rate_int: float = sample_rate_int
        self.__pir_length: int = pir_length
        self.__input_device: int = input_device
        self.__device_sensitivity: float = device_sensitivity
        self.__measurement_type: int = measurement_type
        self.__averaging_type: int = averaging_type
        self.__number_of_averages: int = number_of_averages
        self.__bfiltered: int = bfiltered
        self.__generator_type: int = generator_type
        self.__peak_left: float = peak_left
        self.__peak_right: float = peak_right
        self.__generator_subtype: int = generator_subtype
        self.__cursor_position: int = cursor_position
        self.__marker_position: int = marker_position
        self.__reserved_3: float = reserved_3
        self.__reserved_4: float = reserved_4
        self.__pir_data: list[float] = pir_data
        self.__info_text: str = info_text

    @classmethod
    def of(cls, path_to_pir_file):
        return PirUtils.read_pir_file(path_to_pir_file)

    def get_time_vector(self):
        return [i / self.__sample_rate_int for i in range(len(self.__pir_data))]

    def get_ir(self):
        return np.array(
            [
                self.get_time_vector(),
                self.__pir_data,
            ]
        ).T

    def get_pir_data(self):
        return self.__pir_data

    def get_sample_rate(self):
        return self.__sample_rate_int


class PirUtils:

    @staticmethod
    def read_pir_file(file_path: str | os.PathLike[str]) -> PirFile:
        # Initialize nullables
        cursor_position = None
        marker_position = None
        reserved_3 = None
        reserved_4 = None

        absolute_path = expand_absolute_path(file_path)

        with open(absolute_path, 'rb') as file:
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
            info_text = ''.join(file.read())

        return PirFile(
            file_signature,
            unsigned_int_version,
            reserved_1,
            reserved_2,
            info_size,
            sample_rate_float,
            sample_rate_int,
            pir_length,
            input_device,
            device_sensitivity,
            measurement_type,
            averaging_type,
            number_of_averages,
            bfiltered,
            generator_type,
            peak_left,
            peak_right,
            generator_subtype,
            pir_data,
            info_text,
            cursor_position,
            marker_position,
            reserved_3,
            reserved_4
        )
