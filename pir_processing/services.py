""" Module with several services for diverse PIR processing fashions."""

from concurrent.futures import ThreadPoolExecutor
import csv
import logging as logger
from multiprocessing import cpu_count
import os
from typing import Union

from pir_processing.pir import PirFile

SAVE_AS_CSV = False
EXTENSION = "txt"


def scan_for_pir_files_in_directory(directory: Union[str, os.PathLike]):
    """Scan the directory for files with .pir extension"""
    return set(
        filter(lambda filename: (filename[-3:].lower() == "pir"), os.listdir(directory))
    )


def transform_all_pir_files(directory: Union[str, os.PathLike] = "."):
    """Orchestrator method. Scans the directory for .pir files and calls the
    transforming function."""
    pir_files_set = {
        os.path.join(directory, pir_file_name)
        for pir_file_name in scan_for_pir_files_in_directory(directory)
    }
    _workers: int = cpu_count()

    with ThreadPoolExecutor(_workers) as thread_pool:
        thread_pool.map(read_and_save_pir_in_ascii, pir_files_set)


def read_and_save_pir_in_ascii(path_to_file: Union[str, os.PathLike]) -> PirFile:
    """Read the PIR file info from the given path and save it in a new CSV or TXT file."""
    pir_file_data = PirFile.from_file_path(path_to_file)
    output_file_name = str(path_to_file).split(".")[-2] + (
        ".csv" if SAVE_AS_CSV else ".txt"
    )
    if SAVE_AS_CSV:
        save_pir_data_as_csv(output_file_name, pir_file_data)
    else:
        save_pir_data_as_txt(output_file_name, pir_file_data)
    return pir_file_data


def save_pir_data_as_txt(path_to_file: Union[str, os.PathLike], pir_file: PirFile):
    """Saves the contents of a PirFile to a .txt file in the given path."""
    try:
        with open(path_to_file, "w", encoding="utf-8") as output_file:
            txt_writer = csv.writer(output_file, delimiter=",")
            for pir_row in pir_file.get_pir_data():
                txt_writer.writerow([pir_row])
    except IOError:
        logger.error(
            "An error occurred while saving the transformed PIR", exc_info=True
        )
    else:
        logger.info("Transformed PIR into file %s", path_to_file)


def save_pir_data_as_csv(path_to_file: Union[str, os.PathLike], pir_file: PirFile):
    """Saves the contents of a PirFile to a .csv file in the given path."""
    try:
        with open(path_to_file, "w", encoding="utf-8") as output_file:
            txt_writer = csv.writer(output_file, delimiter=",")
            txt_writer.writerow(["Time [s]", "Amplitude [V]"])
            for pir_row in pir_file.get_ir():
                txt_writer.writerow(pir_row.tolist())
    except IOError:
        logger.error(
            "An error occurred while saving the transformed PIR", exc_info=True
        )
    else:
        logger.info("Transformed PIR into file %s", path_to_file)


def service_directory(path: os.PathLike):
    """Process all .pir files in the given directory path."""
    log_message = f"About to transform {path}:\n"
    for filename in os.scandir(path):
        if filename.is_file() and str(filename.name).lower().endswith("pir"):
            log_message += f"  - {filename.name}\n"
    logger.info(log_message)
    transform_all_pir_files(path)


def service_file(path: os.PathLike):
    """Process a .pir file at the given path."""
    logger.info("Transforming %s", path)
    read_and_save_pir_in_ascii(path)
