"""01 - Diagnostico inicial de calidad del archivo ORIGINAL (no modifica nada).

Salidas:
    data/processed/diagnostico_pruebas.csv   -> una fila por prueba de calidad
    data/processed/diagnostico_resumen.json  -> cifras clave para el informe
"""
import json
import pandas as pd
from comun import (COLUMNAS, COD_DEPARTAMENTO, PROC, RAW, VOCABULARIOS,
                   leer_raw, sha256)

df = leer_raw()
pruebas = []


def anotar(codigo, descripcion, resultado, n_afectados, tratamiento):
    pruebas.append({"codigo": codigo, "prueba": descripcion, "resultado": resultado,
                    "registros_afectados": n_afectados, "tratamiento": tratamiento})


# D01 estructura
ok_cols = list(df.columns) == COLUMNAS
anotar("D01", "Estructura: 15 columnas esperadas y en el orden del diccionario",
       "Cumple" if ok_cols else "No cumple", 0 if ok_cols else len(df), "Ninguno")

# D02 vacios
vacios = int((df.apply(lambda s: s.str.strip() == "")).sum().sum())
anotar("D02", "Valores nulos o vacios en cualquier campo",
       "Cumple" if vacios == 0 else "No cumple", vacios, "Ninguno" if vacios == 0 else "Revisar")

# D03 duplicados exactos
dup = int(df.duplicated().sum())
anotar("D03", "Filas duplicadas exactas", "Cumple" if dup == 0 else "No cumple", dup,
       "Ninguno" if dup == 0 else "Marcar, no eliminar")

# D04 duplicados con misma area (mismo poligono repetido)
dup_area = int(df.duplicated(subset=["AREA_DEFO", "DISTRITO", "ANIO_REPORTE", "MES_IMAG"], keep=False).sum())
anotar("D04", "Posibles poligonos repetidos (misma area, distrito, anio y mes)",
       "Sin hallazgos" if dup_area == 0 else "Revisar", dup_area, "Marcar si existe")

# D05 vocabularios controlados
for campo, validos in VOCABULARIOS.items():
    fuera = int((~df[campo].isin(validos)).sum())
    anotar("D05-" + campo, f"{campo}: valores dentro del vocabulario observado/esperado",
           "Cumple" if fuera == 0 else "No cumple", fuera, "Ninguno" if fuera == 0 else "Revisar")

# D06 numericos
area = pd.to_numeric(df["AREA_DEFO"], errors="coerce")
anotar("D06", "AREA_DEFO numerica con punto decimal", "Cumple" if area.notna().all() else "No cumple",
       int(area.isna().sum()), "Convertir a decimal")
anotar("D07", "AREA_DEFO > 0 ha", "Cumple" if (area > 0).all() else "No cumple", int((area <= 0).sum()), "Ninguno")
mes = pd.to_numeric(df["MES_IMAG"], errors="coerce")
anotar("D08", "MES_IMAG entre 1 y 12", "Cumple" if mes.between(1, 12).all() else "No cumple",
       int((~mes.between(1, 12)).sum()), "Convertir a entero")
anio = pd.to_numeric(df["ANIO_REPORTE"], errors="coerce")
anotar("D09", "ANIO_REPORTE entre 2021 y 2023", "Cumple" if anio.between(2021, 2023).all() else "No cumple",
       int((~anio.between(2021, 2023)).sum()), "Convertir a entero")

# D10 UBIGEO
largo = int((df["UBIGEO"].str.len() != 6).sum())
anotar("D10", "UBIGEO con 6 digitos (ceros iniciales conservados)", "Cumple" if largo == 0 else "No cumple",
       largo, "Leer siempre como texto")
n_cero = int(df["UBIGEO"].str.startswith("0").sum())
anotar("D11", "UBIGEO que empieza en 0 (se pierde el cero al abrir en Excel sin formato texto)",
       "Riesgo de interoperabilidad", n_cero, "Mantener como texto")

# D12 coherencia UBIGEO - DEPARTAMENTO
cod = df["DEPARTAMENTO"].map(COD_DEPARTAMENTO)
incoh = int((df["UBIGEO"].str[:2] != cod).sum())
anotar("D12", "Los 2 primeros digitos de UBIGEO coinciden con DEPARTAMENTO",
       "Cumple" if incoh == 0 else "No cumple", incoh, "Ninguno" if incoh == 0 else "Revisar")

# D13 UBIGEO -> unico distrito
n_ub = df.groupby("UBIGEO")[["DEPARTAMENTO", "PROVINCIA", "DISTRITO"]].nunique().max(axis=1)
anotar("D13", "Cada UBIGEO corresponde a un unico departamento-provincia-distrito",
       "Cumple" if (n_ub == 1).all() else "No cumple", int((n_ub > 1).sum()), "Ninguno")

# D14 FECHA_CORTE unica
fechas = df["FECHA_CORTE"].unique().tolist()
anotar("D14", "FECHA_CORTE unica (un solo corte oficial)", "Cumple" if len(fechas) == 1 else "No cumple",
       0, f"Valor: {fechas}")

# D15 confiabilidad
nd = int((df["CONFIABILIDAD"] == "NO DETERMINADO").sum())
bajo = int((df["CONFIABILIDAD"] == "BAJO").sum())
anotar("D15", "Alertas con CONFIABILIDAD 'NO DETERMINADO' o 'BAJO'", "Hallazgo (no es error)",
       nd + bajo, "Marcar con bandera; NO eliminar")

# D16 atipicos (regla de Tukey 3 x IQR sobre log10)
import numpy as np
la = np.log10(area)
q1, q3 = la.quantile([.25, .75])
lim = q3 + 1.5 * (q3 - q1)
atip = int((la > lim).sum())
anotar("D16", f"Superficies atipicas altas (log10 > Q3+1.5*IQR = {10**lim:.1f} ha)", "Hallazgo (no es error)",
       atip, "Marcar con bandera; son eventos grandes verosimiles, NO eliminar")

pd.DataFrame(pruebas).to_csv(PROC / "diagnostico_pruebas.csv", index=False, encoding="utf-8-sig")

resumen = {
    "archivo_original": RAW.name,
    "sha256_original": sha256(RAW),
    "filas": int(len(df)), "columnas": int(df.shape[1]),
    "area_total_ha": round(float(area.sum()), 2),
    "limite_atipico_ha": round(float(10 ** lim), 2),
    "n_atipicos": atip, "n_no_determinado": nd, "n_bajo": bajo,
    "ubigeo_con_cero_inicial": n_cero,
}
(PROC / "diagnostico_resumen.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")
print(pd.DataFrame(pruebas)[["codigo", "resultado", "registros_afectados"]].to_string(index=False))
print(resumen)
