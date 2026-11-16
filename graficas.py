import os, csv
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('graficas_png', exist_ok=True)

archivos = [
    ('Parser Propio (CFG)', 'resultados_propio.csv', 5),
    ('spaCy (es_core_news_sm)', 'resultados_spacy.csv', 4),
    ('Stanza (UD Español)', 'resultados_stanza.csv', 5),
    ('LLM Zero-Shot', 'llm_zero.csv', 5),
    ('LLM Few-Shot', 'llm_few.csv', 5),
]

datos = {}
for nombre, path, col_tipo in archivos:
    if not os.path.exists(path):
        print(f"Aviso: aún no existe {path}, se omitirá temporalmente.")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        rows = list(csv.reader(f))[1:]
    datos[nombre] = {}
    for niv in (1, 2, 3, 'TOTAL'):
        sub = [r for r in rows if niv == 'TOTAL' or int(r[1 if 'llm_' in path else 0]) == niv]
        c = {t: sum(r[col_tipo] == t for r in sub) for t in ('TP', 'FN', 'FP', 'TN')}
        prec = c['TP'] / (c['TP'] + c['FP']) if (c['TP'] + c['FP']) else 0
        rec  = c['TP'] / (c['TP'] + c['FN']) if (c['TP'] + c['FN']) else 0
        rech = c['TN'] / (c['TN'] + c['FP']) if (c['TN'] + c['FP']) else 0
        datos[nombre][niv] = {'c': c, 'prec': round(prec, 2), 'rec': round(rec, 2), 'rech': round(rech, 2)}

# Imprimir tabla resumen para copiar al informe
print("\n=== TABLA COMPARATIVA TOTAL ===")
print(f"{'Enfoque':<26} | {'TP':>2} {'TN':>2} {'FP':>2} {'FN':>2} | {'Prec':>5} | {'Rec':>5} | {'Rech':>5}")
print("-" * 68)
for nombre, d in datos.items():
    t = d['TOTAL']
    c = t['c']
    print(f"{nombre:<26} | {c['TP']:>2} {c['TN']:>2} {c['FP']:>2} {c['FN']:>2} | {t['prec']:>5.2f} | {t['rec']:>5.2f} | {t['rech']:>5.2f}")

# GRÁFICA 1: Métricas Globales
modelos = list(datos.keys())
x = np.arange(len(modelos))
w = 0.25

fig, ax = plt.subplots(figsize=(11, 5.5))
b1 = ax.bar(x - w, [datos[m]['TOTAL']['prec'] for m in modelos], w, label='Precisión', color='#2b6cb0')
b2 = ax.bar(x,     [datos[m]['TOTAL']['rec']  for m in modelos], w, label='Recall (Cobertura)', color='#38a169')
b3 = ax.bar(x + w, [datos[m]['TOTAL']['rech'] for m in modelos], w, label='Rechazo Correcto', color='#dd6b20')

ax.set_ylabel('Puntuación (0.0 - 1.0)')
ax.set_title('Comparación Global de Desempeño por Enfoque (60 oraciones)', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(modelos, rotation=12, ha='right')
ax.set_ylim(0, 1.12)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.legend()

for bars in (b1, b2, b3):
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.2f}', xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('graficas_png/comparacion_total.png', dpi=300)
plt.close()

# GRÁFICA 2: Recall por Nivel de Complejidad
fig, ax = plt.subplots(figsize=(9, 5))
niveles = [1, 2, 3]
for m in modelos:
    vals = [datos[m][n]['rec'] for n in niveles]
    ax.plot(['Nivel 1 (Simple)', 'Nivel 2 (Intermedio)', 'Nivel 3 (Complejo)'], vals, marker='o', linewidth=2.2, label=m)

ax.set_ylabel('Recall (Cobertura)')
ax.set_title('Degradación del Recall según Complejidad Lingüística', fontweight='bold')
ax.set_ylim(-0.05, 1.1)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend()
plt.tight_layout()
plt.savefig('graficas_png/recall_por_nivel.png', dpi=300)
plt.close()

# GRÁFICA 3: Distribución de Acierto vs Error (TP, TN, FP, FN)
fig, ax = plt.subplots(figsize=(10, 5.5))
tp = np.array([datos[m]['TOTAL']['c']['TP'] for m in modelos])
tn = np.array([datos[m]['TOTAL']['c']['TN'] for m in modelos])
fp = np.array([datos[m]['TOTAL']['c']['FP'] for m in modelos])
fn = np.array([datos[m]['TOTAL']['c']['FN'] for m in modelos])

ax.bar(modelos, tp, label='TP (Aceptadas correctamente)', color='#2f855a')
ax.bar(modelos, tn, bottom=tp, label='TN (Rechazadas correctamente)', color='#68d391')
ax.bar(modelos, fp, bottom=tp+tn, label='FP (Inválidas aceptadas)', color='#e53e3e')
ax.bar(modelos, fn, bottom=tp+tn+fp, label='FN (Válidas rechazadas)', color='#f6ad55')

ax.set_ylabel('Cantidad de Oraciones (Total = 60)')
ax.set_title('Distribución de Clasificación y Errores por Enfoque', fontweight='bold')
plt.xticks(rotation=12, ha='right')
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig('graficas_png/distribucion_errores.png', dpi=300)
plt.close()

print("\nGráficas guardadas en graficas_png/")