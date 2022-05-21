import os
import PirFile


class PirUtils:
    @staticmethod
    def read_pir_file(file_path: str | os.PathLike[str]) -> PirFile:
        with open(file_path, 'rb') as file:
            file_signature = [bytes(file.read(2)) for i in range(4)]
            unsigned_int_version = int(file.read(4))
            info_size = int(file.read(4))
            reserved_1 = int(file.read(4))
            reserved_2 = int(file.read(4))
            sample_rate_float = float(file.read(4))
            sample_rate_int = int(file.read(4))
            pir_length = int(file.read(4))
            input_device = int(file.read(4))
            device_sensitivity = float(file.read(4))
            measurement_type = int(file.read(4))
            averaging_type = int(file.read(4))
            number_of_averages = int(file.read(4))
            bfiltered = int(file.read(4))
            generator_type = int(file.read(4))
            peak_left = float(file.read(4))
            peak_right = float(file.read(4))
            generator_subtype = int(file.read(4))

            if unsigned_int_version >= 5:
                cursor_position = int(file.read(4))
                marker_position = int(file.read(4))
            else:
                reserved_3 = float(file.read(4))
                reserved_4 = float(file.read(4))

            pir_data = [float(file.read(4)) for i in range(pir_length)]
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
