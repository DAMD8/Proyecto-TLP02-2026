import csv, spacy
from corpus import SET
nlp = spacy.load('es_core_news_sm')

def acepta(s):
    raiz = [t for t in nlp(s) if t.dep_ == 'ROOT'][0]
    ok = raiz.pos_ in ('VERB', 'AUX') and any(t.dep_.startswith('nsubj') for t in raiz.children)
    return 'ok' if ok else 'no'

filas = []
for niv, gold, s in SET:
    pred = acepta(s)
    tipo = {('ok','ok'):'TP', ('ok','no'):'FN', ('no','ok'):'FP', ('no','no'):'TN'}[(gold, pred)]
    filas.append((niv, s, gold, pred, tipo))

with open('resultados_spacy.csv', 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows([('nivel','oracion','gold','pred','tipo')] + filas)

for niv in (1, 2, 3, 'TOTAL'):
    r = [x for x in filas if niv == 'TOTAL' or x[0] == niv]
    c = {t: sum(x[4] == t for x in r) for t in ('TP','FN','FP','TN')}
    d = lambda a, b: round(a / b, 2) if b else 0
    print(f"Nivel {niv}: {c} precisión={d(c['TP'], c['TP']+c['FP'])} recall={d(c['TP'], c['TP']+c['FN'])} rechazo_correcto={d(c['TN'], c['TN']+c['FP'])}")
print("\nErrores:")
for x in filas:
    if x[4] in ('FN', 'FP'): print(x[4], x[0], x[1])