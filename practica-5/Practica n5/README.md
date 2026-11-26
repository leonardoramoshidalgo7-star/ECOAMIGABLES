# Práctica 04: Base de datos, secuestro de carbono e inteligencia artificial

Curaduría, evaluación FAIR y análisis exploratorio de la base **Deforestación en Áreas Naturales Protegidas (ANP) del Perú, 2021-2023** (SERNANP), como insumo para una investigación sobre emisiones potenciales de carbono.

> Universidad Nacional Federico Villarreal (UNFV) · Curso: (completar) · Grupo: (completar integrantes)

## Resumen

| Elemento | Valor |
|---|---|
| Institución productora | Servicio Nacional de Áreas Naturales Protegidas por el Estado (SERNANP) |
| Datos | 5 129 registros (polígonos) × 15 campos; 31 ANP; 11 departamentos; 62 distritos |
| Superficie total | 7 233,30 ha (2021: 3 304,48 · 2022: 2 341,89 · 2023: 1 586,92) |
| Fecha de corte oficial | 21/06/2024 |
| Licencia de los datos | ODC-BY declarada por el grupo (**confirmar** en la ficha oficial) |
| Fuente de descarga | (completar URL exacta y fecha de descarga) |

**Alcance sobre carbono:** la base contiene *datos de actividad* (hectáreas deforestadas). Permite estimar *emisiones brutas potenciales* si se agregan factores de emisión externos; **no** permite estimar reservas, remociones ni tasas de secuestro.

## Estructura

```
data/raw/         Original sin modificar (con huella SHA-256)
data/processed/   Base curada, bitácora de cambios, diagnóstico, metadatos, checksums
docs/             Entregables 1 a 11 (Word/Excel), PROCEDENCIA.md, REGISTRO_DECISIONES.md
figures/          Gráficos del análisis exploratorio
scripts/          Código numerado en el orden de ejecución
```

## Cómo reproducir

1. Clonar el repositorio y entrar a la carpeta raíz.
2. Crear un entorno e instalar dependencias:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # en Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Ejecutar **desde la raíz** y en orden:
   ```bash
   python scripts/01_diagnostico.py
   python scripts/02_curaduria.py
   python scripts/03_analisis_exploratorio.py
   python scripts/04_exportar_metadatos.py
   ```
4. Comprobar integridad: la huella del original debe coincidir con `data/processed/checksums.sha256`.

| Script | Qué hace | Salidas |
|---|---|---|
| `01_diagnostico.py` | 16 pruebas de calidad sobre el original (no lo modifica) | `diagnostico_pruebas.csv`, `diagnostico_resumen.json` |
| `02_curaduria.py` | Corrige formato, agrega ID y banderas; no elimina registros | `Dataset_Deforestacion_SERNANP_curado.csv`, `registro_cambios.csv` |
| `03_analisis_exploratorio.py` | Tablas y figuras 1 a 7 | `figures/`, `eda_resumen.json` |
| `04_exportar_metadatos.py` | Metadatos y SHA-256 | `metadatos.json`, `checksums.sha256` |

## Entregables (carpeta `docs/`)

| N.º | Entregable | Archivo |
|---|---|---|
| 1 | Inventario de repositorios institucionales | `ENTREGABLE_1.docx` |
| 2 | Base original y curada | `ENTREGABLE_2_Base_original_y_curada.xlsx` + `data/` |
| 3 | Informe de curaduría | `ENTREGABLE_3_Informe_de_curaduria.docx` |
| 4 | Matriz FAIR | `ENTREGABLE_4_Matriz_FAIR.xlsx` |
| 5 | Diccionario de datos y metadatos | `ENTREGABLE_5_Diccionario_de_datos.xlsx` |
| 6 | Repositorio GitHub | este repositorio + `ENTREGABLE_6_Repositorio_GitHub_guia.docx` |
| 7 | Registro de uso de IA | `ENTREGABLE_7_Registro_uso_IA.xlsx` |
| 8 | Matriz comparativa de metodologías de carbono | `ENTREGABLE_8_Matriz_metodologias_carbono.xlsx` |
| 9 | Análisis exploratorio | `ENTREGABLE_9_Analisis_exploratorio.docx` + `ENTREGABLE_9_EDA_tablas.xlsx` + `figures/` |
| 10 | Proyecto de investigación | `ENTREGABLE_10_Proyecto_de_investigacion.docx` |
| 11 | Presentación y defensa | `ENTREGABLE_11_Guion_de_defensa.docx` |

## Principios de curaduría

- El original en `data/raw/` **nunca se edita**.
- Se corrige el formato, no los valores: lo dudoso se **marca** con banderas (`FLAG_*`), no se elimina.
- Cada transformación queda en `registro_cambios.csv`.
- Todo uso de IA se registra y se verifica (ENTREGABLE 7).

## Cómo citar

Ver `CITATION.cff`. Referencia FAIR: Wilkinson et al. (2016), https://doi.org/10.1038/sdata.2016.18

## Licencia

Código y documentación: MIT (`LICENSE`). Datos: según la licencia del SERNANP.
