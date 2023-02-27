# pir-processing

[![Linting and codestyle](https://github.com/pupkinivan/pir-processing/actions/workflows/linting-and-codestyle.yml/badge.svg)](https://github.com/pupkinivan/pir-processing/actions/workflows/linting-and-codestyle.yml)
[![PyPI deployment](https://github.com/pupkinivan/pir-processing/actions/workflows/pypi-deploy.yml/badge.svg)](https://github.com/pupkinivan/pir-processing/actions/workflows/pypi-deploy.yml)

Python tools for reading the binary information inside ARTA's .pir files. It's implemented with multiprocessing, in order to leverage multi-core processors and handle large amounts of files. 

## Installation

`pip install pir-processing`

## Requirements

`python >=3.8,<3.10`

## Usage

### Single file

In order to transform a single PIR file to .txt, run the tool as follows:

```python -m pir_processing --file PATH_TO_THE_PIR_FILE [--csv]```

where you need to replace `PATH_TO_THE_PIR_FILE` with the path to your god forsaken PIR files.

The `--csv` flag lets you transform them to CSV instead, which includes a synthetic time axis starting at 0 seconds.

### Multiple files

In order to transform a series of PIR files to .txt, run the tool as follows:

```python -m pir_processing --directory PATH_TO_YOUR_PIR_FILES [--csv]```

where you need to replace `PATH_TO_YOUR_PIR_FILES` with the path to your god forsaken PIR files.

The `--csv` flag lets you transform them to CSV instead, which includes a synthetic time axis starting at 0 seconds.

The output files are saved in the same directory that was passed as input.
