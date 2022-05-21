import os
import PirFile
from binascii import hexlify


class PirUtils:
    @staticmethod
    def read_pir_file(file_path: str | os.PathLike[str]) -> PirFile:
        with open(file_path, 'rb') as file:
            file_signature = [bytes(file.read(1)) for i in range(4)]
            unsigned_int_version = int(hexlify(file.read(4)), 16)
            info_size = int(hexlify(file.read(4)), 16)
            reserved_1 = int(hexlify(file.read(4)), 16)
            reserved_2 = int(hexlify(file.read(4)), 16)
            sample_rate_float = float(hexlify(file.read(4)))
            sample_rate_int = int(hexlify(file.read(4)), 16)
            pir_length = int(hexlify(file.read(4)), 16)
            input_device = int(hexlify(file.read(4)), 16)
            device_sensitivity = float(hexlify(file.read(4)))
            measurement_type = int(hexlify(file.read(4)), 16)
            averaging_type = int(hexlify(file.read(4)), 16)
            number_of_averages = int(hexlify(file.read(4)), 16)
            bfiltered = int(hexlify(file.read(4)), 16)
            generator_type = int(hexlify(file.read(4)), 16)
            peak_left = float(hexlify(file.read(4)))
            peak_right = float(hexlify(file.read(4)))
            generator_subtype = int(hexlify(file.read(4)), 16)

            if unsigned_int_version >= 5:
                cursor_position = int(hexlify(file.read(4)), 16)
                marker_position = int(hexlify(file.read(4)), 16)
            else:
                reserved_3 = float(hexlify(file.read(4)))
                reserved_4 = float(hexlify(file.read(4)))

            pir_data = [float(hexlify(file.read(4))) for i in range(pir_length)]
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
