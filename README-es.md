# pir-processing

[Readme en castellano 🇪🇸](https://github.com/pupkinivan/pir-processing/README-es.md)

Herramientas de procesamiento de archivos de formato PIR (de ARTA) en Python. Incluye un conversor de PIR a CSV, a _.txt_ y clases para la lectura programática de archivos de la primera extensión.

## Requisitos:
- Python >= 3.8
- NumPy ~= 1.22.4

## Instrucciones

### Conversión a TXT

Para convertir un conjunto de archivos PIR que estén dentro de un mismo directorio a formato _.txt_, hace falta usar el script del archivo `transform_all_pir_to_ascii.py` de la siguiente forma. En una terminal ("Símbolo de sistema" en Windows, "Terminal" en Linux o macOS), ejecutar dicho script:

```python3 transform_all_pir_to_ascii.py RUTA_DEL_DIRECTORIO```

donde `RUTA_DEL_DIRECTORIO` debe ser reemplazada con la ruta _absoluta_ a tus archivos PIR. Esto quiere decir, incluyendo el nombre del disco en el caso de Windows (C:, D:, etc.), `/home` y demás en Linux (o donde se haya montado el disco), etc. Como resultado de la ejecución, los archivos _txt_ se encontrarán en la misma carpeta que los PIR.

### Conversión a CSV

La conversión a CSV se puede hacer de la misma manera que a _txt_, con el agregado de una _flag_ `--csv` en el llamado al script:

```python3 transform_all_pir_to_ascii.py RUTA_DEL_DIRECTORIO --csv```

A diferencia del TXT, los CSV incluyen una columna para el eje temporal. Cabe aclarar que este es generado artificialmente, ya que los archivos PIR no lo incluyen. Para ello, se asume que la grabación comienza en el instante 00:00:00.000000.
