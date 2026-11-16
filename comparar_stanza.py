import csv
import stanza
from corpus import SET

stanza.download('es', processors='tokenize,mwt,pos,lemma,depparse', verbose=False)
nlp = stanza.Pipeline('es', processors='tokenize,mwt,pos,lemma,depparse', verbose=False)

def acepta(s):
    doc = nlp(s)
    if not doc.sentences:
        return 'no', 'sin oraciones'
    words = doc.sentences[0].words
    raices = [w for w in words if w.deprel == 'root']
    if not raices:
        return 'no', 'sin raíz'
    raiz = raices[0]
    tiene_sujeto = any(w.head == raiz.id and w.deprel.startswith('nsubj') for w in words)
    ok = raiz.upos in ('VERB', 'AUX') and tiene_sujeto
    motivo = '-' if ok else f"root={raiz.upos}, nsubj={tiene_sujeto}"
    return ('ok' if ok else 'no'), motivo

filas = []
for niv, gold, s in SET:
    pred, motivo = acepta(s)
    tipo = {('ok','ok'):'TP', ('ok','no'):'FN', ('no','ok'):'FP', ('no','no'):'TN'}[(gold, pred)]
    filas.append((niv, s, gold, pred, motivo, tipo))

with open('resultados_stanza.csv', 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows([('nivel','oracion','gold','pred','motivo','tipo')] + filas)

d = lambda a, b: round(a / b, 2) if b else 0
for niv in (1, 2, 3, 'TOTAL'):
    r = [x for x in filas if niv == 'TOTAL' or x[0] == niv]
    c = {t: sum(x[5] == t for x in r) for t in ('TP','FN','FP','TN')}
    print(f"Nivel {niv}: {c} precisión={d(c['TP'], c['TP']+c['FP'])} recall={d(c['TP'], c['TP']+c['FN'])} rechazo_correcto={d(c['TN'], c['TN']+c['FP'])}")

print("\nErrores Stanza:")
for x in filas:
    if x[5] in ('FN', 'FP'):
        print(x[5], x[0], x[1], '->', x[4])