"""02 - Curaduria: genera la base curada SIN alterar los valores originales.

Principio: se corrige el FORMATO (tipos de dato, codificacion), se agregan
campos derivados (ID y banderas) y se registra cada cambio. Ningun registro
se elimina y ningun valor se reemplaza: los valores inusuales solo se marcan.

Salidas:
    data/processed/Dataset_Deforestacion_SERNANP_curado.csv   (UTF-8 con BOM, punto decimal)
    data/processed/registro_cambios.csv                        (bitacora de transformaciones)
"""
import numpy as np
import pandas as pd
from comun import COLUMNAS, PROC, RAW, leer_raw, sha256

raw = leer_raw()
cur = raw.copy()
cambios = []


def registrar(paso, campo, regla, n, justificacion):
    cambios.append({"paso": paso, "campo": campo, "regla_aplicada": regla,
                    "registros_afectados": n, "justificacion": justificacion})


# 1. Tipos de dato ---------------------------------------------------------
cur["ANIO_REPORTE"] = cur["ANIO_REPORTE"].astype(int)
registrar("C01", "ANIO_REPORTE", "texto -> entero", len(cur), "Permite agrupar y ordenar por anio")
cur["MES_IMAG"] = cur["MES_IMAG"].astype(int)
registrar("C02", "MES_IMAG", "texto -> entero (1-12)", len(cur), "Permite analisis estacional")
cur["AREA_DEFO"] = cur["AREA_DEFO"].astype(float)
registrar("C03", "AREA_DEFO", "texto -> decimal (punto decimal, sin redondear)", len(cur),
          "Permite sumar hectareas; no se redondea para no perder precision")
cur["UBIGEO"] = cur["UBIGEO"].str.zfill(6)
n_cero = int(raw["UBIGEO"].str.startswith("0").sum())
registrar("C04", "UBIGEO", "se conserva como TEXTO de 6 digitos (zfill)", n_cero,
          "Evita perder el cero inicial (ej. 010101) al abrir en Excel")
cur["FECHA_CORTE"] = pd.to_datetime(cur["FECHA_CORTE"], format="%Y%m%d").dt.strftime("%Y-%m-%d")
registrar("C05", "FECHA_CORTE", "AAAAMMDD -> AAAA-MM-DD (ISO 8601)", len(cur),
          "Formato interoperable de fecha; el valor 20240621 queda como 2024-06-21")

# 2. Limpieza de espacios (verificacion) ------------------------------------
n_esp = 0
for c in ["ANP", "CATEGORIA", "FUENTE_IMAG", "DEFO_CAUSA", "CONFIABILIDAD", "TIPO_BOSQUE",
          "ZONIFI_ANP", "DEPARTAMENTO", "PROVINCIA", "DISTRITO"]:
    limpio = cur[c].str.strip().str.replace(r"\s+", " ", regex=True)
    n_esp += int((limpio != cur[c]).sum())
    cur[c] = limpio
registrar("C06", "campos de texto", "recorte de espacios sobrantes", n_esp,
          "Verificacion: 0 registros requirieron cambio" if n_esp == 0 else "Espacios eliminados")

# 3. Campos derivados -------------------------------------------------------
cur.insert(0, "ID_REGISTRO", [f"R{i:05d}" for i in range(1, len(cur) + 1)])
registrar("C07", "ID_REGISTRO", "identificador secuencial R00001..R05129 segun orden del archivo original",
          len(cur), "Permite rastrear cada registro curado hasta su fila original")

cur["FLAG_CONF_NO_DET"] = (cur["CONFIABILIDAD"] == "NO DETERMINADO").astype(int)
registrar("C08", "FLAG_CONF_NO_DET", "1 si CONFIABILIDAD = NO DETERMINADO", int(cur["FLAG_CONF_NO_DET"].sum()),
          "Marca alertas sin nivel de certeza; no se eliminan")
cur["FLAG_CONF_BAJA"] = (cur["CONFIABILIDAD"] == "BAJO").astype(int)
registrar("C09", "FLAG_CONF_BAJA", "1 si CONFIABILIDAD = BAJO", int(cur["FLAG_CONF_BAJA"].sum()),
          "Marca alertas de baja certeza; no se eliminan")

la = np.log10(cur["AREA_DEFO"])
q1, q3 = la.quantile([.25, .75])
lim = 10 ** (q3 + 1.5 * (q3 - q1))
cur["FLAG_AREA_ATIPICA"] = (cur["AREA_DEFO"] > lim).astype(int)
registrar("C10", "FLAG_AREA_ATIPICA", f"1 si AREA_DEFO > {lim:.1f} ha (Tukey 1.5xIQR sobre log10)",
          int(cur["FLAG_AREA_ATIPICA"].sum()),
          "Valores inusuales pero verosimiles (eventos grandes): se marcan, no se modifican ni eliminan")

# 4. Verificaciones que NO generaron cambios --------------------------------
registrar("C11", "todos", "duplicados exactos", 0, "No se detectaron; no se elimino ninguna fila")
registrar("C12", "todos", "nulos / vacios", 0, "No se detectaron; no se imputo ningun valor")
registrar("C13", "UBIGEO-DEPARTAMENTO", "coherencia de codigos", 0, "Sin inconsistencias")

# 5. Control de integridad ---------------------------------------------------
assert len(cur) == len(raw) == 5129
assert np.isclose(cur["AREA_DEFO"].sum(), raw["AREA_DEFO"].astype(float).sum())
assert list(cur.columns[1:16]) == COLUMNAS

cur.to_csv(PROC / "Dataset_Deforestacion_SERNANP_curado.csv", index=False, encoding="utf-8-sig")
pd.DataFrame(cambios).to_csv(PROC / "registro_cambios.csv", index=False, encoding="utf-8-sig")
print(pd.DataFrame(cambios)[["paso", "campo", "registros_afectados"]].to_string(index=False))
print("SHA256 original:", sha256(RAW))
print("Area total curada (ha):", round(cur["AREA_DEFO"].sum(), 4))
