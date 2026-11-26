"""03 - Analisis exploratorio de datos (EDA) sobre la base curada.

Salidas:
    figures/fig01..fig07 (PNG)
    data/processed/eda_resumen.json   -> cifras para los informes
"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from comun import FIG, PROC

plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 100, "savefig.dpi": 200})
VERDE, MARRON, GRIS = "#2E7D32", "#8D6E63", "#9E9E9E"

df = pd.read_csv(PROC / "Dataset_Deforestacion_SERNANP_curado.csv", dtype={"UBIGEO": str})
TOTAL = df["AREA_DEFO"].sum()
res = {"n": int(len(df)), "total_ha": float(TOTAL)}


def tabla(col):
    t = df.groupby(col)["AREA_DEFO"].agg(registros="size", ha="sum", media="mean", mediana="median")
    t["pct_ha"] = 100 * t["ha"] / TOTAL
    return t.sort_values("ha", ascending=False)


for nombre, col in [("anio", "ANIO_REPORTE"), ("causa", "DEFO_CAUSA"), ("bosque", "TIPO_BOSQUE"),
                    ("zona", "ZONIFI_ANP"), ("anp", "ANP"), ("depto", "DEPARTAMENTO"),
                    ("categoria", "CATEGORIA"), ("fuente", "FUENTE_IMAG"), ("conf", "CONFIABILIDAD")]:
    res[nombre] = tabla(col).round(4).reset_index().to_dict(orient="records")

# estadisticos descriptivos
a = df["AREA_DEFO"]
res["desc"] = {"n": int(a.count()), "media": a.mean(), "mediana": a.median(), "sd": a.std(),
               "min": a.min(), "p25": a.quantile(.25), "p75": a.quantile(.75), "p95": a.quantile(.95),
               "max": a.max(), "asimetria": float(a.skew())}
res["desc_por_bosque"] = df.groupby("TIPO_BOSQUE")["AREA_DEFO"].describe().round(4).reset_index().to_dict(orient="records")

# pivote anio x tipo de bosque, anio x ANP
pv = df.pivot_table(index="ANIO_REPORTE", columns="TIPO_BOSQUE", values="AREA_DEFO", aggfunc="sum")
res["pivot_anio_bosque"] = pv.round(2).reset_index().to_dict(orient="records")
top = tabla("ANP").index[:10]
pa = df[df.ANP.isin(top)].pivot_table(index="ANP", columns="ANIO_REPORTE", values="AREA_DEFO", aggfunc="sum").loc[top]
res["pivot_anp_anio"] = pa.round(2).reset_index().to_dict(orient="records")
res["fuente_por_anio"] = df.pivot_table(index="ANIO_REPORTE", columns="FUENTE_IMAG", values="AREA_DEFO",
                                        aggfunc="sum").fillna(0).round(2).reset_index().to_dict(orient="records")
res["concentracion_top3_anp_pct"] = float(tabla("ANP")["pct_ha"].head(3).sum())
res["concentracion_top5_anp_pct"] = float(tabla("ANP")["pct_ha"].head(5).sum())
res["n_anp"] = int(df.ANP.nunique())
res["n_distritos"] = int(df.UBIGEO.nunique())
res["cambio_2021_2023_pct"] = float(100 * (pv.sum(axis=1).loc[2023] / pv.sum(axis=1).loc[2021] - 1))

# Figuras --------------------------------------------------------------------
# 1. superficie por anio y tipo de bosque
fig, ax = plt.subplots(figsize=(7, 4.2))
pv.plot(kind="bar", stacked=True, ax=ax, color=[VERDE, MARRON], width=.6)
for i, v in enumerate(pv.sum(axis=1)):
    ax.text(i, v + 40, f"{v:,.0f} ha", ha="center", fontsize=9)
ax.set(xlabel="Año de reporte", ylabel="Superficie deforestada (ha)",
       title="Fig. 1. Deforestación en ANP por año y tipo de bosque")
ax.tick_params(axis="x", rotation=0); ax.legend(title="Tipo de bosque", frameon=False)
fig.tight_layout(); fig.savefig(FIG / "fig01_area_por_anio_bosque.png"); plt.close(fig)

# 2. top 10 ANP
t = tabla("ANP").head(10).iloc[::-1]
fig, ax = plt.subplots(figsize=(7.5, 4.6))
ax.barh(t.index, t["ha"], color=VERDE)
for y, (v, p) in enumerate(zip(t["ha"], t["pct_ha"])):
    ax.text(v + 10, y, f"{v:,.0f} ha ({p:.1f}%)", va="center", fontsize=8)
ax.set(xlabel="Superficie deforestada 2021-2023 (ha)", title="Fig. 2. Diez ANP con mayor superficie deforestada")
ax.set_xlim(0, t["ha"].max() * 1.3); fig.tight_layout(); fig.savefig(FIG / "fig02_top10_anp.png"); plt.close(fig)

# 3. por causa (escala log por la dominancia de agricultura)
t = tabla("DEFO_CAUSA").iloc[::-1]
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.barh(t.index, t["ha"], color=MARRON)
for y, (v, p) in enumerate(zip(t["ha"], t["pct_ha"])):
    ax.text(v * 1.08, y, f"{v:,.0f} ha ({p:.1f}%)", va="center", fontsize=8)
ax.set_xscale("log"); ax.set_xlim(10, t["ha"].max() * 6)
ax.set(xlabel="Superficie deforestada (ha, escala logarítmica)", title="Fig. 3. Deforestación según causa registrada")
fig.tight_layout(); fig.savefig(FIG / "fig03_por_causa.png"); plt.close(fig)

# 4. por zonificacion
t = tabla("ZONIFI_ANP").iloc[::-1]
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(t.index.str.title(), t["ha"], color=VERDE)
for y, (v, p) in enumerate(zip(t["ha"], t["pct_ha"])):
    ax.text(v + 8, y, f"{p:.1f}%", va="center", fontsize=8)
ax.set(xlabel="Superficie deforestada (ha)", title="Fig. 4. Deforestación según zonificación interna del ANP")
ax.set_xlim(0, t["ha"].max() * 1.15); fig.tight_layout(); fig.savefig(FIG / "fig04_por_zonificacion.png"); plt.close(fig)

# 5. histograma log
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(np.log10(df["AREA_DEFO"]), bins=40, color=GRIS, edgecolor="white")
ax.axvline(np.log10(a.median()), color=VERDE, lw=2, label=f"Mediana = {a.median():.2f} ha")
ax.axvline(np.log10(a.mean()), color=MARRON, lw=2, ls="--", label=f"Media = {a.mean():.2f} ha")
ax.set(xlabel="log10(superficie del polígono, ha)", ylabel="Número de registros",
       title="Fig. 5. Distribución de la superficie por registro (asimétrica a la derecha)")
ax.legend(frameon=False); fig.tight_layout(); fig.savefig(FIG / "fig05_histograma_area.png"); plt.close(fig)

# 6. mapa de calor ANP x anio (top 10)
fig, ax = plt.subplots(figsize=(6.5, 4.6))
im = ax.imshow(pa.values, cmap="YlGn", aspect="auto")
ax.set_xticks(range(3), pa.columns); ax.set_yticks(range(len(pa)), pa.index, fontsize=8)
for i in range(pa.shape[0]):
    for j in range(pa.shape[1]):
        ax.text(j, i, f"{pa.values[i, j]:,.0f}", ha="center", va="center", fontsize=8)
ax.set_title("Fig. 6. Superficie deforestada (ha) en las 10 ANP principales")
fig.colorbar(im, ax=ax, shrink=.8); fig.tight_layout(); fig.savefig(FIG / "fig06_mapa_calor_anp_anio.png"); plt.close(fig)

# 7. fuente de imagen por anio (limitacion metodologica)
fp = df.pivot_table(index="ANIO_REPORTE", columns="FUENTE_IMAG", values="AREA_DEFO", aggfunc="sum").fillna(0)
fig, ax = plt.subplots(figsize=(7, 4))
fp.plot(kind="bar", stacked=True, ax=ax, colormap="Set2", width=.6)
ax.set(xlabel="Año de reporte", ylabel="Superficie (ha)", title="Fig. 7. Fuente de detección por año (cambia la composición)")
ax.tick_params(axis="x", rotation=0); ax.legend(title="Fuente", frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(FIG / "fig07_fuente_por_anio.png"); plt.close(fig)

(PROC / "eda_resumen.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=float), encoding="utf-8")
print("Total ha:", round(TOTAL, 2), "| cambio 2021-2023: %.1f%%" % res["cambio_2021_2023_pct"])
print("Top3 ANP: %.1f%% | Top5: %.1f%%" % (res["concentracion_top3_anp_pct"], res["concentracion_top5_anp_pct"]))
for k in ["anio", "causa", "bosque", "zona", "depto", "conf"]:
    print(k, [(r[[x for x in r if x not in ("registros","ha","media","mediana","pct_ha")][0]], round(r["ha"]), round(r["pct_ha"],1)) for r in res[k]])
print(res["desc"])
print([(r["ANP"], round(r["ha"]), round(r["pct_ha"],1)) for r in res["anp"][:10]])
