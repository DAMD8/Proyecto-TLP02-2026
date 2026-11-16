from google import genai
from google.genai import types
c = genai.Client(http_options=types.HttpOptions(timeout=30000))
print(c.models.generate_content(model="gemini-4-hydrogen", contents="Di hola").text)