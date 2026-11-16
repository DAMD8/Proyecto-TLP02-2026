from nltk import Tree
L = {}  # palabra -> (cat, genero, numero, tiempo)
def add(w, c, g=None, n=None, t=None): L[w] = (c, g, n, t)

for w, g, n in [('el','m','s'),('la','f','s'),('los','m','p'),('las','f','p'),
                ('un','m','s'),('una','f','s'),('unos','m','p'),('unas','f','p')]: add(w, 'Det', g, n)
for s, g in [('niño','m'),('niña','f'),('perro','m'),('gato','m'),('libro','m'),
             ('casa','f'),('mesa','f'),('profesor','m'),('ciudad','f'),('parque','m'),('manzana','f')]:
    add(s, 'N', g, 's'); add(s + ('es' if s[-1] in 'dr' else 's'), 'N', g, 'p')
for s in ['bonit','rápid','pequeñ','nuev','viej','roj']:
    for suf, g, n in [('o','m','s'),('a','f','s'),('os','m','p'),('as','f','p')]: add(s+suf, 'Adj', g, n)
for s in ['grande','fácil']: add(s, 'Adj', None, 's'); add(s+'s', 'Adj', None, 'p')
for v in [('come','comen','comió','comieron'),('compra','compran','compró','compraron'),
          ('lee','leen','leyó','leyeron'),('ve','ven','vio','vieron'),
          ('corre','corren','corrió','corrieron'),('duerme','duermen','durmió','durmieron')]:
    for w, n, t in zip(v, 'spsp', ['pres','pres','pret','pret']): add(w, 'V', None, n, t)
for w in ['rápidamente','ayer','hoy','mucho']: add(w, 'Adv')
for w in ['en','con','de','a','para','sobre']: add(w, 'Prep')
for w in ['ana','luis']: add(w, 'Nom', None, 's')

def lex(s):
    toks = s.lower().replace('.', '').split()
    bad = [t for t in toks if t not in L]
    return toks, bad

def parse(toks):
    def t(i, c):
        if i < len(toks) and L[toks[i]][0] == c: return Tree(c, [toks[i]]), i + 1
    def SN(i):
        if r := t(i, 'Nom'): return Tree('SN', [r[0]]), r[1]
        d = t(i, 'Det'); n = d and t(d[1], 'N')
        if not n: return None
        ch, i = [d[0], n[0]], n[1]
        while a := t(i, 'Adj'): ch.append(a[0]); i = a[1]
        return Tree('SN', ch), i
    def SP(i):
        p = t(i, 'Prep'); s = p and SN(p[1])
        if s: return Tree('SP', [p[0], s[0]]), s[1]
    def SV(i):
        ch = []
        if a := t(i, 'Adv'): ch.append(a[0]); i = a[1]
        v = t(i, 'V')
        if not v: return None
        ch.append(v[0]); i = v[1]
        if o := SN(i): ch.append(o[0]); i = o[1]
        while True:
            if p := SP(i): ch.append(p[0]); i = p[1]
            elif a := t(i, 'Adv'): ch.append(a[0]); i = a[1]
            else: break
        return Tree('SV', ch), i
    s = SN(0); v = s and SV(s[1])
    if v and v[1] == len(toks): return Tree('O', [s[0], v[0]])

def check(tree):
    err = []
    for sn in tree.subtrees(lambda x: x.label() == 'SN'):
        ws = [L[c.leaves()[0]] for c in sn if c.label() in ('Det','N','Adj')]
        for k, nom in ((1,'género'),(2,'número')):
            if len({w[k] for w in ws if w[k]}) > 1: err.append(f"{nom} en {' '.join(sn.leaves())}")
    h = [c for c in tree[0] if c.label() in ('N','Nom')][0]
    v = [c for c in tree[1] if c.label() == 'V'][0]
    if L[h[0]][2] != L[v[0]][2]: err.append(f"sujeto-verbo: {h[0]} / {v[0]}")
    return err

if __name__ == '__main__':
    for s in ["El niño come una manzana", "El perro grande corre rápidamente en el parque",
              "Los niños come", "El niño come una manzana roja y", "Come el niño", "La niña vio un libro nuevo ayer"]:
        toks, bad = lex(s)
        if bad: print(s, '-> léxico desconocido:', bad); continue
        tr = parse(toks)
        if not tr: print(s, '-> RECHAZADA (sintaxis)'); continue
        e = check(tr); print(s, '->', 'ACEPTADA' if not e else f'RECHAZADA (concordancia: {e})')
        tr.pretty_print()