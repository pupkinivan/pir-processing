# Ivan Pupkin
# ipupkin@untref.edu.ar
# ivopupkin20@gmail.com

import csv
import logging
from multiprocessing import cpu_count
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
from PirFile import PirFile


def scan_for_pir_files_in_directory(directory: str | os.PathLike[str]):
    return filter(lambda filename: (filename[-3:].lower() == "pir"), os.listdir(directory))


def transform_all_pir_files(directory: [str, os.PathLike] = "."):
    pir_files_list = scan_for_pir_files_in_directory(directory)
    _workers: int = cpu_count()

    with ThreadPoolExecutor(_workers) as thread_pool:
        thread_pool.map(read_and_save_pir_as_txt, pir_files_list)
        for pir_file_path in pir_files_list:
            read_and_save_pir_as_txt(pir_file_path)

    print(f"Transformed the following .PIR files:")
    for filename in pir_files_list:
        print(filename)


def read_and_save_pir_as_txt(path_to_file: str | os.PathLike[str]) -> PirFile:
    pir_file_data = PirFile.of(path_to_file)
    txt_file_name = str(path_to_file).split('.')[-2] + ".txt"
    save_pir_data_as_txt(txt_file_name, pir_file_data)
    return pir_file_data


def save_pir_data_as_txt(path_to_file: str | os.PathLike[str], pir_file: PirFile):
    with open(path_to_file, 'w') as output_file:
        txt_writer = csv.writer(output_file, delimiter=',')
        for pir_row in pir_file.get_pir_data():
            txt_writer.writerow(pir_row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Enter a directory from which to source PIR files and transform them to .txt"
    )
    parser.add_argument("directory_path", help="Path to the PIR directory")
    args = parser.parse_args()

    if args.directory_path is None:
        logging.error("Expected one directory")
        exit(1)
    else:
        if not os.path.exists(args.directory_path):
            logging.error("The given directory does not exist")
            exit(2)
        else:
            transform_all_pir_files(args.directory_path)
