import sys, time, csv, re
from google import genai
from google.genai import types
from espanol import L
from corpus import SET

MODEL = "gemini-4-hydrogen"
modo = sys.argv[1]
client = genai.Client(http_options=types.HttpOptions(timeout=120000))

voc = {}
for w, v in L.items():
    voc.setdefault(v[0], []).append(w)
vocab = "\n".join(f"{c}: {', '.join(ws)}" for c, ws in voc.items())

REGLAS = f"""Eres un analizador sintáctico formal. Usa SOLO esta gramática y este vocabulario, no tu conocimiento general del español.
O -> SN SV
SN -> Nom | Det N Adj*
SV -> Adv? V SN? (SP | Adv)*
SP -> Prep SN
Vocabulario (una palabra fuera de la lista => RECHAZA):
{vocab}
Además, RECHAZA si dentro de un SN no concuerdan género o número, o si el sujeto no concuerda en número con el verbo.
Para cada oración numerada, responde en UNA sola línea con el formato exacto:
N | ACEPTA o RECHAZA | razón breve"""

EJ = """Ejemplos:
1 | El gato lee un libro nuevo => 1 | ACEPTA | cumple reglas y concordancia
2 | Ana ve la mesa roja => 2 | ACEPTA | cumple reglas y concordancia
3 | Las niñas corre en el parque => 3 | RECHAZA | sujeto plural, verbo singular
4 | El profesor lee unas mesa => 4 | RECHAZA | número en el SN
5 | Come el gato => 5 | RECHAZA | la gramática exige SN antes de SV
6 | El perro quiere una casa => 6 | RECHAZA | 'quiere' no está en el vocabulario"""

prompt_base = REGLAS + ("\n" + EJ if modo == "few" else "")
cfg = types.GenerateContentConfig(
    temperature=0,
    thinking_config=types.ThinkingConfig(thinking_level="low")
)

filas = []
for niv in (1, 2, 3):
    lote = [(i, gold, s) for i, (nv, gold, s) in enumerate(SET, 1) if nv == niv]
    bloque_oraciones = "\n".join(f"{i} | {s}" for i, _, s in lote)
    
    r = None
    for intento in range(5):
        try:
            print(f"[{modo}] Procesando Nivel {niv} ({len(lote)} oraciones)...")
            resp = client.models.generate_content(
                model=MODEL,
                contents=f"{prompt_base}\n\nAnaliza estas oraciones:\n{bloque_oraciones}",
                config=cfg
            )
            r = resp.text.strip()
            break
        except Exception as e:
            espera = 15 * (intento + 1)
            print(f"Error en Nivel {niv} (intento {intento+1}/5), esperando {espera}s: {str(e)[:60]}")
            time.sleep(espera)
            
    if not r:
        print(f"Fallo crítico en Nivel {niv}")
        sys.exit(1)

    respuestas = {}
    for linea in r.splitlines():
        m = re.match(r"^\s*(\d+)\s*\|\s*(ACEPTA|RECHAZA)\s*\|\s*(.*)$", linea, re.IGNORECASE)
        if m:
            idx, veredicto, razon = int(m.group(1)), m.group(2).upper(), m.group(3).strip()
            respuestas[idx] = (veredicto, razon)

    for i, gold, s in lote:
        veredicto, razon = respuestas.get(i, ("RECHAZA", "sin respuesta parseada"))
        pred = 'ok' if veredicto == 'ACEPTA' else 'no'
        tipo = {('ok','ok'):'TP', ('ok','no'):'FN', ('no','ok'):'FP', ('no','no'):'TN'}[(gold, pred)]
        filas.append((modo, niv, s, gold, pred, tipo, f"{veredicto} | {razon}"))
    
    if niv < 3:
        time.sleep(10)

with open(f'llm_{modo}.csv', 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows([('modo', 'nivel', 'oracion', 'gold', 'pred', 'tipo', 'respuesta')] + filas)

d = lambda a, b: round(a / b, 2) if b else 0
print(f"\n--- RESUMEN {modo.upper()} ---")
for niv in (1, 2, 3, 'TOTAL'):
    x = [r for r in filas if niv == 'TOTAL' or r[1] == niv]
    c = {t: sum(r[5] == t for r in x) for t in ('TP', 'FN', 'FP', 'TN')}
    print(f"[{modo}] Nivel {niv}: {c} precisión={d(c['TP'], c['TP']+c['FP'])} recall={d(c['TP'], c['TP']+c['FN'])} rechazo_correcto={d(c['TN'], c['TN']+c['FP'])}")