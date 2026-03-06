# src/nlp.py
import re
from collections import Counter

# --- 1. STOPWORDS (Para palabras clave) ---
STOPWORDS = set([
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero", "si", 
    "por", "para", "como", "a", "de", "en", "con", "su", "sus", "te", "me", "se", 
    "es", "qué", "que", "lo", "del", "al", "este", "esta", "eso", "esto", "muy", 
    "más", "ya", "hay", "son", "nos", "mi", "mis", "tu", "tus", "yo", "nosotros",
    "porque", "cuando", "donde", "quien", "todo", "nada", "algo", "hacer", "tiene"
])

# --- 2. DICCIONARIOS DE SENTIMIENTO (Lexicon) ---
PALABRAS_POSITIVAS = set([
    "bueno", "excelente", "mejor", "increíble", "gracias", "feliz", "éxito", 
    "ganar", "bien", "genial", "fácil", "amor", "ayuda", "top", "viral", "secreto",
    "descubre", "aprende", "solución", "oportunidad", "crecer", "oro", "dinero"
])

PALABRAS_NEGATIVAS = set([
    "malo", "peor", "terrible", "error", "difícil", "problema", "fracaso", 
    "perder", "odio", "triste", "nunca", "mal", "cuidado", "estafa", "peligro",
    "mentira", "engaño", "tóxico", "culpa", "miedo", "riesgo", "ruina"
])

def extraer_palabras_clave(texto, top_n=3):
    if not texto or texto in ["Error Transcripción IA", "Error audio"]: return ""
    texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
    palabras = [p for p in texto_limpio.split() if p not in STOPWORDS and len(p) > 3]
    if not palabras: return ""
    top_palabras = [palabra for palabra, frec in Counter(palabras).most_common(top_n)]
    return ", ".join(top_palabras)

def analizar_sentimiento(texto):
    """
    Cuenta las palabras positivas y negativas para determinar la emoción del video.
    """
    if not texto or texto in ["Error Transcripción IA", "Error audio"]: return "Neutral ⚪"
    
    print("🎭 Analizando polaridad emocional...")
    texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
    palabras = texto_limpio.split()
    
    puntuacion = 0
    for palabra in palabras:
        if palabra in PALABRAS_POSITIVAS:
            puntuacion += 1
        elif palabra in PALABRAS_NEGATIVAS:
            puntuacion -= 1
            
    if puntuacion > 0:
        return "Positivo 🟢"
    elif puntuacion < 0:
        return "Polémico/Negativo 🔴"
    else:
        return "Neutral ⚪"