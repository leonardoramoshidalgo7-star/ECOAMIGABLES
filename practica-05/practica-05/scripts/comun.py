"""Rutas, constantes y funciones compartidas por todos los scripts.

Ejecutar siempre los scripts desde la raiz del repositorio:
    python scripts/01_diagnostico.py
"""
from pathlib import Path
import hashlib
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw" / "Dataset_Deforestacion_SERNANP_0.csv"
PROC = RAIZ / "data" / "processed"
FIG = RAIZ / "figures"
DOCS = RAIZ / "docs"

COLUMNAS = [
    "ANP", "CATEGORIA", "ANIO_REPORTE", "FUENTE_IMAG", "MES_IMAG", "DEFO_CAUSA",
    "CONFIABILIDAD", "TIPO_BOSQUE", "ZONIFI_ANP", "AREA_DEFO", "DEPARTAMENTO",
    "PROVINCIA", "DISTRITO", "UBIGEO", "FECHA_CORTE",
]

# Codigo INEI de departamento (2 primeros digitos del UBIGEO)
COD_DEPARTAMENTO = {
    "AMAZONAS": "01", "CAJAMARCA": "06", "CUSCO": "08", "HUANUCO": "10",
    "JUNIN": "12", "LORETO": "16", "MADRE DE DIOS": "17", "PASCO": "19",
    "PUNO": "21", "SAN MARTIN": "22", "UCAYALI": "25",
}

VOCABULARIOS = {
    "TIPO_BOSQUE": {"PRIMARIO", "SECUNDARIO"},
    "CONFIABILIDAD": {"ALTO", "BAJO", "NO DETERMINADO"},
    "DEFO_CAUSA": {"AGRICULTURA", "TRANSPORTE", "MINERIA", "OCUPACION HUMANA"},
    "FUENTE_IMAG": {"GLADS2", "PNCB LANDSAT", "PLANET", "GFW INTEGRADAS"},
}


def leer_raw() -> pd.DataFrame:
    """Lee el CSV original SIN inferir tipos (todo texto) para no alterar nada."""
    return pd.read_csv(RAW, dtype=str, encoding="utf-8", keep_default_na=False)


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()
