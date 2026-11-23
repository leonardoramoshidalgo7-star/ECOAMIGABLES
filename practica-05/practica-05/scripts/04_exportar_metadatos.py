"""04 - Exporta metadatos y sumas de verificacion (SHA-256) para trazabilidad FAIR.

Salidas:
    data/processed/metadatos.json      -> ficha de metadatos del conjunto de datos
    data/processed/checksums.sha256    -> huellas digitales de original y curado
"""
import json
from datetime import date
import pandas as pd
from comun import PROC, RAW, sha256

cur_csv = PROC / "Dataset_Deforestacion_SERNANP_curado.csv"
df = pd.read_csv(cur_csv, dtype={"UBIGEO": str})

meta = {
    "titulo": "Deforestacion en Areas Naturales Protegidas del Peru, 2021-2023 (version curada)",
    "institucion_productora": "SERVICIO NACIONAL DE AREAS NATURALES PROTEGIDAS POR EL ESTADO (SERNANP)",
    "fuente_original": "Plataforma Nacional de Datos Abiertos / SINIA (completar URL exacta de descarga)",
    "fecha_corte_original": "2024-06-21",
    "licencia_declarada_por_el_grupo": "ODC-BY (CONFIRMAR en la ficha oficial antes de publicar)",
    "cobertura_temporal": "2021-2023",
    "cobertura_espacial": f"{df.ANP.nunique()} ANP; {df.DEPARTAMENTO.nunique()} departamentos; {df.UBIGEO.nunique()} distritos",
    "unidad_de_observacion": "poligono/alerta de deforestacion detectado (un registro por poligono, anio y tipo de bosque)",
    "numero_de_registros": int(len(df)),
    "superficie_total_ha": round(float(df.AREA_DEFO.sum()), 2),
    "formato": "CSV UTF-8 (con BOM), separador coma, punto decimal",
    "version_curada_generada": str(date.today()),
    "procedencia": "scripts/01_diagnostico.py -> 02_curaduria.py -> 03_analisis_exploratorio.py",
    "sha256_original": sha256(RAW),
    "sha256_curado": sha256(cur_csv),
}
(PROC / "metadatos.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
(PROC / "checksums.sha256").write_text(
    f"{meta['sha256_original']}  data/raw/{RAW.name}\n{meta['sha256_curado']}  data/processed/{cur_csv.name}\n")
print(json.dumps(meta, indent=2, ensure_ascii=False))
