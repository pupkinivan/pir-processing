""" Entry point for the PyPIR package."""
import argparse
import logging
import os
from traceback import print_exception

from pir_processing import services


def get_parser():
    parser = argparse.ArgumentParser(
        description="Enter a directory to PIR files or a single PIR file path."
    )
    parser.add_argument(
        "--directory", "-d", help="Path to the PIR directory", required=False
    )
    parser.add_argument("--file", "-f", help="Path to a PIR file", required=False)
    parser.add_argument(
        "--save_as_csv",
        "--csv",
        required=False,
        action="store_const",
        const=True,
        default=False,
        help="Save the file as a CSV, with amplitude along with a time column",
    )
    return parser


def route_command(path: os.PathLike):
    """Redirect the call to the file-processing service or the directory one."""
    if os.path.isdir(path):
        services.service_directory(path)
    elif os.path.isfile(path):
        services.service_file(path)


def validate_arguments(arguments):
    """Validate the arguments passed to the CLI."""
    if (arguments.directory is None) and (arguments.file is None):
        logging.error("Expected a file or directory path")
        raise ValueError("Expected a file or directory path")
    if (arguments.directory is not None) and (arguments.file is not None):
        logging.error("Expected a single path (either to a file or a directory)")
        raise ValueError("Expected a file or directory path")

    path = arguments.directory if arguments.directory is not None else arguments.file
    absolute_path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
    if not os.path.exists(absolute_path):
        logging.error("Path %s does not exist" % absolute_path)
        raise ValueError("Expected a file or directory path")
    return path


if __name__ == "__main__":
    args = get_parser().parse_args()

    SAVE_AS_CSV = bool(args.save_as_csv)
    EXTENSION = "csv" if SAVE_AS_CSV else "txt"

    try:
        path = validate_arguments(args)
    except ValueError:
        print_exception()
    else:
        services.EXTENSION = EXTENSION
        services.SAVE_AS_CSV = SAVE_AS_CSV
        route_command(path)
