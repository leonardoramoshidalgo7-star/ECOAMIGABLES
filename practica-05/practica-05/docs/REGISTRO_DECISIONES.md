# Registro de decisiones metodológicas

| N.º | Decisión | Motivo | Alternativa descartada |
|---|---|---|---|
| D1 | Elegir la base de deforestación del SERNANP | Tabular, abierta, sin datos personales, conectada con carbono (tipo de bosque, causa, zonificación) | SERFOR (datos personales), OEFA, INAIGEM, SENACE (datos en PDF/capas pesadas o sin variables de biomasa) |
| D2 | No eliminar ningún registro | Sin duplicados ni nulos; lo dudoso no es error verificable | Eliminar alertas de baja confiabilidad o atípicas |
| D3 | Marcar con banderas FLAG_CONF_NO_DET, FLAG_CONF_BAJA y FLAG_AREA_ATIPICA | Permite análisis de sensibilidad sin perder información | Imputar o corregir valores |
| D4 | Umbral de atípicos: Tukey 1,5×IQR sobre log10(área) = 41,67 ha | Distribución muy asimétrica; en escala log la regla es adecuada | Regla sobre la escala lineal |
| D5 | UBIGEO como texto de 6 dígitos | Evitar pérdida del cero inicial | Convertir a entero |
| D6 | CSV curado en UTF-8 con BOM y punto decimal | Interoperabilidad con Excel en configuración regional española | UTF-8 sin BOM |
| D7 | No estimar reservas ni secuestro | La base no contiene biomasa ni series de crecimiento | Usar supuestos sin respaldo |
| D8 | Estimar solo emisiones brutas potenciales con factores externos citados y rango | Es la única magnitud de carbono alcanzable con datos de actividad | Valor único sin incertidumbre |
| D9 | Rechazar la definición de curaduría de IA con 7 componentes de otro proyecto | Describía inventarios de vegetación, no esta base | Pegarla sin verificar |
