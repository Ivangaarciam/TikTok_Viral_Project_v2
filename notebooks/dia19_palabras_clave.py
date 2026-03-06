import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os
import sys
import re

print("========================================")
print("🗣️  DETECTOR DE PALABRAS MÁGICAS (Día 19)")
print("========================================")

ARCHIVO_CSV = "cerebro_tiktok.csv"

# LISTA DE "PALABRAS BASURA" (Stopwords) en Español
# Estas palabras no aportan significado y las borraremos del análisis
STOPWORDS = {
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o', 'pero', 'si', 
    'de', 'del', 'al', 'en', 'con', 'por', 'para', 'sin', 'sobre', 'a', 'ante', 
    'bajo', 'entre', 'hacia', 'hasta', 'que', 'qué', 'cual', 'quien', 'donde', 
    'cuando', 'como', 'más', 'mas', 'muy', 'todo', 'nada', 'algo', 'esto', 'eso', 
    'aquello', 'yo', 'tu', 'el', 'ella', 'nosotros', 'vosotros', 'ellos', 'mi', 
    'tu', 'su', 'mis', 'tus', 'sus', 'es', 'son', 'fue', 'era', 'está', 'están', 
    'ser', 'estar', 'haber', 'tener', 'hacer', 'ir', 'venir', 'decir', 'poder', 
    'dar', 'ver', 'ya', 'no', 'si', 'sí', 'ni', 'video', 'vídeo', 'tiktok', 'gracias',
    'hola', 'bueno', 'pues', 'entonces', 'aquí', 'ahí', 'allí', 'hoy', 'ahora'
}

if not os.path.exists(ARCHIVO_CSV):
    print("❌ No encuentro el CSV.")
    sys.exit()

try:
    # 1. CARGAR DATOS
    df = pd.read_csv(ARCHIVO_CSV, sep=';', decimal=',', encoding='utf-8-sig', on_bad_lines='skip')
    
    if 'TRANSCRIPCION' not in df.columns:
        print("❌ No tienes transcripciones. Usa main.py para analizar videos con audio.")
        sys.exit()

    # Limpiamos vacíos
    df = df.dropna(subset=['TRANSCRIPCION'])
    
    if len(df) == 0:
        print("⚠️ No hay transcripciones guardadas.")
        sys.exit()

    # 2. FILTRAR LOS MEJORES VIDEOS
    # Consideramos "Buenos" al Top 50% de tus videos con más vistas
    mediana_vistas = df['VISTAS'].median()
    df_top = df[df['VISTAS'] >= mediana_vistas]
    
    print(f"📂 Analizando vocabulario del Top {len(df_top)} videos (Vistas > {mediana_vistas:.0f})...")

    # 3. PROCESAMIENTO DE TEXTO
    texto_total = " ".join(df_top['TRANSCRIPCION'].tolist())
    
    # Limpieza: minúsculas y quitar símbolos raros
    texto_limpio = re.sub(r'[^\w\s]', '', texto_total.lower())
    
    palabras = texto_limpio.split()
    
    # Filtrado: Quitamos las stopwords y palabras cortas (menos de 3 letras)
    palabras_clave = [p for p in palabras if p not in STOPWORDS and len(p) > 2]
    
    # Contamos frecuencia
    contador = Counter(palabras_clave)
    top_10 = contador.most_common(10)
    
    print("\n🏆 TOP 10 PALABRAS MÁS REPETIDAS EN TUS VÍDEOS DE ÉXITO:")
    for palabra, cantidad in top_10:
        print(f"   • {palabra.upper()}: {cantidad} veces")

    # 4. GRÁFICA VISUAL
    palabras_graf = [x[0] for x in top_10]
    conteos_graf = [x[1] for x in top_10]
    
    plt.figure(figsize=(10, 6))
    # Invertimos para que la más usada salga arriba en la gráfica horizontal
    plt.barh(palabras_graf[::-1], conteos_graf[::-1], color='skyblue', edgecolor='black')
    
    plt.title('Vocabulario de tus Videos Virales', fontsize=16)
    plt.xlabel('Frecuencia de uso', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    
    plt.savefig('grafica_palabras_clave.png')
    print("\n✅ Gráfica guardada: 'grafica_palabras_clave.png'")
    
    # CONSEJO AUTOMÁTICO
    if top_10:
        word1 = top_10[0][0]
        print(f"\n💡 IDEA DE GUION: Intenta empezar tu próximo video diciendo '{word1.upper()}' en los primeros 3 segundos.")

except Exception as e:
    print(f"❌ Error: {e}")

input("\nPresiona ENTER para salir...")