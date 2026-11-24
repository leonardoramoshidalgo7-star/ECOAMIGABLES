#!/usr/bin/env bash
# Publica practica-04 con un historial de 8 commits.
# 1) Crea en GitHub un repositorio VACIO llamado practica-04-deforestacion-anp
# 2) Cambia TU_USUARIO abajo y ejecuta este archivo DESDE la carpeta practica-04:
#       bash docs/subir_a_github.sh
set -e
USUARIO="TU_USUARIO"
git init
git branch -M main
git add .gitignore LICENSE && git commit -m "Estructura inicial, licencia y gitignore"
git add data/raw && git commit -m "Agregar datos originales de SERNANP sin modificar"
git add scripts/comun.py scripts/01_diagnostico.py && git commit -m "Agregar modulo comun y diagnostico de calidad"
git add scripts/02_curaduria.py data/processed && git commit -m "Agregar script de curaduria y base curada"
git add scripts/03_analisis_exploratorio.py figures && git commit -m "Analisis exploratorio y figuras"
git add scripts/04_exportar_metadatos.py docs/ENTREGABLE_5_Diccionario_de_datos.xlsx && git commit -m "Metadatos, checksums y diccionario de datos"
git add docs && git commit -m "Documentacion: informe de curaduria, FAIR y registro de IA"
git add README.md requirements.txt CITATION.cff && git commit -m "README, dependencias y citacion"
git remote add origin "https://github.com/${USUARIO}/practica-04-deforestacion-anp.git"
git push -u origin main
