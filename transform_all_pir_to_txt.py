# Ivan Pupkin
# ipupkin@untref.edu.ar
# ivopupkin20@gmail.com

import csv
import logging
from multiprocessing import cpu_count
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
from pir import PirFile

SAVE_AS_CSV = False


def scan_for_pir_files_in_directory(directory: str | os.PathLike[str]):
    return set(filter(lambda filename: (filename[-3:].lower() == "pir"), os.listdir(directory)))


def transform_all_pir_files(directory: [str, os.PathLike] = "."):
    pir_files_set = {os.path.join(directory, pir_file_name)
                     for pir_file_name in scan_for_pir_files_in_directory(directory)}
    _workers: int = cpu_count()

    with ThreadPoolExecutor(_workers) as thread_pool:
        thread_pool.map(read_and_save_pir_as_txt, pir_files_set)

    print(f"Transformed the following .PIR files:")
    for filename in pir_files_set:
        print(filename)


def read_and_save_pir_as_txt(path_to_file: str | os.PathLike[str]) -> PirFile:
    pir_file_data = PirFile.of(path_to_file)
    output_file_name = str(path_to_file).split('.')[-2] + (".csv" if SAVE_AS_CSV else ".txt")
    if SAVE_AS_CSV:
        save_pir_data_as_csv(output_file_name, pir_file_data)
    else:
        save_pir_data_as_txt(output_file_name, pir_file_data)
    return pir_file_data


def save_pir_data_as_txt(path_to_file: str | os.PathLike[str], pir_file: PirFile):
    with open(path_to_file, 'w') as output_file:
        txt_writer = csv.writer(output_file, delimiter=',')
        for pir_row in pir_file.get_pir_data():
            txt_writer.writerow([pir_row])


def save_pir_data_as_csv(path_to_file: str | os.PathLike[str], pir_file: PirFile):
    with open(path_to_file, 'w') as output_file:
        txt_writer = csv.writer(output_file, delimiter=',')
        txt_writer.writerow(["Time [s]", "Amplitude [V]"])
        for pir_row in pir_file.get_ir():
            txt_writer.writerow(pir_row.tolist())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Enter a directory from which to source PIR files and transform them to .txt"
    )
    parser.add_argument("directory_path", help="Path to the PIR directory")
    parser.add_argument("--save_as_csv", "--csv", required=False, action='store_const', const=True, default=False,
                        help="Save the file as a CSV, with amplitude along with a time column")
    args = parser.parse_args()
    SAVE_AS_CSV = args.save_as_csv

    if args.directory_path is None:
        logging.error("Expected one directory")
        exit(1)
    else:
        absolute_path = os.path.abspath(os.path.expanduser(os.path.expandvars(args.directory_path)))
        if not os.path.exists(absolute_path):
            logging.error(f"Directory {absolute_path} does not exist")
            exit(2)
        else:
            print(f"Contents of {absolute_path}: {os.listdir(absolute_path)}")
            transform_all_pir_files(absolute_path)
