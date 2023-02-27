# pir-processing

Python tools for processing ARTA's .pir files.

## Installation

`pip install pir-processing`

## Requirements

`python >=3.8,<3.10`

## Usage

In order to transform a single PIR file to .txt, run the tool as follows:

```python -m pir_processing --directory PATH_TO_THE_PIR_FILE [--csv]```


In order to transform a series of PIR files to TXT, run the tool as follows:

```python -m pir_processing --directory PATH_TO_YOUR_PIR_FILES [--csv]```

where you need to replace `PATH_TO_YOUR_PIR_FILES` with guess what... the path to your god forsaken PIR files.

The `--csv` flag lets you transform them to CSV instead, which includes a synthetic time axis starting at 0 seconds.


The output files are saved in the same directory that was passed as input.
