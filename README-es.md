# pir-processing

[Readme in English 🇬🇧](https://github.com/pupkinivan/pir-processing/README.md)

[![Linting and codestyle](https://github.com/pupkinivan/pir-processing/actions/workflows/linting-and-codestyle.yml/badg
e.svg)](https://github.com/pupkinivan/pir-processing/actions/workflows/linting-and-codestyle.yml)
[![PyPI deployment](https://github.com/pupkinivan/pir-processing/actions/workflows/pypi-deploy.yml/badge.svg)](https://github.com/pupkinivan/pir-processing/actions/workflows/pypi-deploy.yml)

`pir-processing` es una herramienta de Python para leer archivos de formato PIR de ARTA y convertirlos a .txt o .csv. Está pensada para poder procesar múltiples archivos en paralelo con procesadores multi-núcleo, gracias a `multiprocessing`.

## Instalación

`pip install pir-processing`

## Requisitos

`python >=3.8,<3.10`

## Instrucciones de uso

### Convertir un solo archivo PIR a .txt o .csv

Para convertir un único archivo PIR a formato _.txt_, hace falta usar la herramienta una terminal de la siguiente forma:

```python -m pir_processing --file RUTA_DEL_ARCHIVO_PIR```

donde `RUTA_DEL_ARCHIVO_PIR` debe ser reemplazada con la ruta absoluta al archivo PIR. Esto se puede hacer arrastrando y soltando el archivo en la terminal. Como resultado de la ejecución, el archivo _txt_ se encontrará en la misma carpeta que el PIR de entrada.

La conversión a CSV se puede hacer de la misma manera que a _txt_, con el agregado de una _flag_ `--csv` en el llamado
 al script:

```python -m pir_processing --csv --file RUTA_DEL_ARCHIVO_PIR```

A diferencia del TXT, los CSV incluyen una columna para el eje temporal. Cabe aclarar que este es generado artificialmente, ya que los archivos PIR no lo incluyen. Para ello, se asume que la grabación comienza en el instante 00:00:00.00
0000.

### Convertir un conjunto de archivos PIR

Para convertir un conjunto de archivos PIR que estén dentro de un mismo directorio a formato _.txt_, hace falta usar la herramienta una terminal de la siguiente forma:

```python -m pir_processing --directory PATH_TO_YOUR_PIR_FILES```

La conversión a CSV se puede hacer de la misma manera que a _txt_, con el agregado de una _flag_ `--csv` en el llamado
 al script:

```python -m pir_processing --csv --directory PATH_TO_YOUR_PIR_FILES```

A diferencia del TXT, los CSV incluyen una columna para el eje temporal. Cabe aclarar que este es generado artificialmente, ya que los archivos PIR no lo incluyen. Para ello, se asume que la grabación comienza en el instante 00:00:00.00
0000.

A diferencia del TXT, los CSV incluyen una columna para el eje temporal. Cabe aclarar que este es generado artificialmente, ya que los archivos PIR no lo incluyen. Para ello, se asume que la grabación comienza en el instante 00:00:00.000000.
