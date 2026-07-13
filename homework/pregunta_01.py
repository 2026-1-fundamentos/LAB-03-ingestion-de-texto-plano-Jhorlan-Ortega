"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.

    """
    import re

    import pandas as pd

    filas = []
    with open("files/input/clusters_report.txt", encoding="utf-8") as file:
        lines = file.readlines()

    fila_actual = None
    for line in lines:
        # Detecta el inicio de una nueva fila: cluster, cantidad y porcentaje
        m = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)", line)
        if m:
            if fila_actual is not None:
                filas.append(fila_actual)
            cluster, cantidad, porcentaje, palabras = m.groups()
            fila_actual = {
                "cluster": int(cluster),
                "cantidad_de_palabras_clave": int(cantidad),
                "porcentaje_de_palabras_clave": porcentaje.replace(",", ".") + " %",
                "principales_palabras_clave": palabras.strip(),
            }
        elif (
            fila_actual is not None
            and line.strip() != ""
            and not line.startswith("---")
        ):
            # Linea de continuacion (texto envuelto): se anexa a la fila actual
            fila_actual["principales_palabras_clave"] += " " + line.strip()

    if fila_actual is not None:
        filas.append(fila_actual)

    df = pd.DataFrame(filas)

    col = df["principales_palabras_clave"]
    col = col.str.replace(r"\s+", " ", regex=True)      # colapsa espacios multiples
    col = col.str.replace(r"\s*,\s*", ", ", regex=True)  # coma + un solo espacio
    col = col.str.rstrip(".").str.strip()                # quita punto final sobrante
    df["principales_palabras_clave"] = col

    return df