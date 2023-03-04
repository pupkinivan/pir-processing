from pathlib import Path

from pir_processing.pir import PirFile

path = Path("./tests/mock_data/untitled_ver_deg0.pir")
PIR_FILE = PirFile.from_file_path(path)
