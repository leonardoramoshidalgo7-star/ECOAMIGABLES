# Registro de procedencia

| Campo | Detalle |
|---|---|
| Conjunto de datos | Deforestación en Áreas Naturales Protegidas, 2021-2023 |
| Institución | SERNANP |
| Repositorio de descarga | Plataforma Nacional de Datos Abiertos / SINIA (completar URL exacta) |
| Fecha de descarga | (completar) |
| Fecha de corte oficial | 2024-06-21 |
| Archivo original | `data/raw/Dataset_Deforestacion_SERNANP_0.csv` |
| SHA-256 original | `e4492fbfc6486e6c29cc6225123349ca90caea22e4c114968d956aabfbb2b11e` |
| Licencia declarada | ODC-BY (confirmar en la ficha oficial) |

## Cadena de transformación

`raw CSV` → `01_diagnostico.py` (solo lectura) → `02_curaduria.py` → `data/processed/Dataset_Deforestacion_SERNANP_curado.csv` → `03_analisis_exploratorio.py` → `figures/`

Versión paralela hecha por el grupo con Power Query: `data/processed/Dataset_Deforestacion_SERNANP_curado_PowerQuery.xlsx` (contiene hojas auxiliares de trabajo; los datos coinciden con la versión de scripts).
