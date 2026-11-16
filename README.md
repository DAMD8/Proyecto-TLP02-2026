# Proyecto-TLP02-2026: Gramáticas Formales y Lenguaje Natural
Implementación y evaluación experimental de los límites de las Gramáticas Libres de Contexto (CFG) frente al español natural, comparando un parser descendente recursivo propio (con verificación semántica de concordancia) contra modelos estadísticos/neuronales de NLP (**spaCy** y **Stanza**) y un Modelo de Lenguaje Grande (**Gemini**) bajo esquemas *Zero-Shot* y *Few-Shot*.

## Estructura del Repositorio
```text
├── espanol.py              # Lexer, parser descendente recursivo (CFG) y analizador semántico
├── corpus.py               # Conjunto de prueba etiquetado (60 oraciones en 3 niveles)
├── evaluar.py              # Evaluación del parser propio y generación de métricas
├── comparar_spacy.py       # Evaluación con spaCy (es_core_news_sm)
├── comparar_stanza.py      # Evaluación con Stanza (Universal Dependencies - español)
├── llm_gemini.py           # Evaluación vía API de Gemini (modos zero-shot y few-shot)
├── arboles.py              # Generador de árboles sintácticos visuales en PNG
├── graficas.py             # Generador de tablas comparativas y gráficas en PNG
├── resultados_*.csv        # Logs y resultados experimentales por enfoque
├── llm_*.csv               # Respuestas y veredictos registrados de la API de Gemini
├── arboles_png/            # Árboles de derivación sintáctica exportados
└── graficas_png/           # Gráficas comparativas de Precisión, Recall y Rechazo
```

## Requisitos e Instalación
### Se recomienda utilizar Python 3.10* dentro de un entorno virtual (para este proyecto se utilizo VS con WSL: Ubuntu)
```text
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install nltk spacy stanza matplotlib numpy google-genai
python -m spacy download es_core_news_sm
```
### Para ejecutar el experimento con el LLM, configure su clave de API de Google Gemini:
```text
export GEMINI_API_KEY="tu_api_key_aqui"  # En Windows (PowerShell): $env:GEMINI_API_KEY="tu_api_key_aqui"
```
## Reproducción de los experimentos y como se obtuvieron los datos para el proyecto
### Probar el paiser propio y visualizar árboles en consola:
```text
python espanol.py
```
### Generar árboles sintácticos visuales (arboles_png/):
```text
python arboles.py
```
### Evaluar el parser propio sobre el corpus de 60 oraciones (resultados_propio.csv):
```text
python evaluar.py
```
### Ejecutar comparativas con herramientas modernas de NLP:
```text
python comparar_spacy.py
python comparar_stanza.py
```
### Ejecutar evaluación formal con Gemini API (llm_zero.csv y llm_few.csv):
```text
python llm_gemini.py zero
python llm_gemini.py few
```
###  Generar tabla comparativa final y gráficas (graficas_png/):
```text
python graficas.py
```
