import csv
from espanol import lex, parse, check
from corpus import SET

def predecir(s):
    toks, bad = lex(s.replace('¿','').replace('?',''))
    if bad: return 'no', 'léxico'
    tr = parse(toks)
    if not tr: return 'no', 'sintaxis'
    return ('no', 'concordancia') if check(tr) else ('ok', '-')

filas = []
for niv, gold, s in SET:
    pred, motivo = predecir(s)
    tipo = {('ok','ok'):'TP', ('ok','no'):'FN', ('no','ok'):'FP', ('no','no'):'TN'}[(gold, pred)]
    filas.append((niv, s, gold, pred, motivo, tipo))

with open('resultados_propio.csv', 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows([('nivel','oracion','gold','pred','motivo','tipo')] + filas)

def met(rows):
    c = {t: sum(r[5] == t for r in rows) for t in ('TP','FN','FP','TN')}
    d = lambda a, b: round(a / b, 2) if b else 0
    return c, d(c['TP'], c['TP']+c['FP']), d(c['TP'], c['TP']+c['FN']), d(c['TN'], c['TN']+c['FP'])

for niv in (1, 2, 3, 'TOTAL'):
    rows = [r for r in filas if niv == 'TOTAL' or r[0] == niv]
    c, p, r, rc = met(rows)
    print(f"Nivel {niv}: {c} precisión={p} recall={r} rechazo_correcto={rc}")
print("\nErrores:")
for r in filas:
    if r[5] in ('FN', 'FP'): print(r[5], r[0], r[1], '->', r[4])