# pir-processing

Python processing tools for ARTA's .pir files.

## Requirements:
- NumPy ~= 1.22.4

## Instructions

In order to transform a series of PIR files to TXT, run the tool as follows:

```python3 transform_all_pir_to_ascii PATH_TO_YOUR_PIR_FILES [--csv]```

where you need to replace `PATH_TO_YOUR_PIR_FILES` with guess what... the path to your god forsaken PIR files. The `--csv` flag lets you transform them to CSV instead, which includes a synthetic time axis starting at 0 seconds.

You'll find the output files in the same directory you gave as input.