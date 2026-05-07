# src/consultor.py
import sqlite3
import pandas as pd
import config
import os

def analizar_base_datos():
    print("\n📊 --- CONSULTOR DE DATOS TIKTOK --- 📊\n")
    
    if not os.path.exists(config.ARCHIVO_DB):
        print("❌ No se encuentra la base de datos. ¡Procesa algún video primero!")
        return

    try:
        # 1. Conectamos a SQLite
        conn = sqlite3.connect(config.ARCHIVO_DB)
        
        # 2. Magia de Pandas: Leemos la tabla entera y la metemos en un DataFrame
        df = pd.read_sql_query("SELECT * FROM videos", conn)
        conn.close()
        
        if df.empty:
            print("⚠️ La base de datos está vacía.")
            return

        # --- REPORTE GENERAL ---
        print(f"✅ Total de videos en el cerebro: {len(df)}")
        print(f"🗣️ Ritmo promedio (WPM): {df['wpm'].mean():.0f} palabras/minuto")
        print(f"👤 Presencia humana promedio: {df['pct_caras'].mean():.1f}%\n")

        # --- ANÁLISIS DEL GANCHO (Retención) ---
        print("🔥 TOP 3 VIDEOS CON MAYOR RITMO (WPM):")
        # Ordenamos los videos por WPM de mayor a menor y cogemos los 3 primeros
        top_ritmo = df.sort_values(by='wpm', ascending=False).head(3)
        
        for index, row in top_ritmo.iterrows():
            print(f"\n🥇 Autor: @{row['autor']} | 👀 Vistas: {row['vistas']:,}")
            print(f"   ⏱️ Ritmo: {row['wpm']} WPM | 🎬 Cortes/min: {row['cortes_min']}")
            print(f"   🪝 Gancho (5s): \"{row['gancho']}\"")
            print(f"   🔗 URL: {row['url']}")
            
    except Exception as e:
        print(f"❌ Error al leer la base de datos: {e}")

if __name__ == "__main__":
    analizar_base_datos()

def generar_prompt_creador(nicho):
    """
    Crea una instrucción hiper-optimizada para que el usuario la copie
    y se la pegue a ChatGPT (o Claude) para generar un guion viral.
    """
    conn = sqlite3.connect(config.ARCHIVO_DB)
    
    # Buscamos los patrones del MEJOR video del nicho
    query = f"""
    SELECT wpm, cortes_min, palabras_clave, sentimiento
    FROM videos 
    WHERE nicho = '{nicho}' 
    ORDER BY (likes * 1.0 / vistas) DESC 
    LIMIT 1
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        return "No hay suficientes datos del nicho para generar un guion."

    mejor = df.iloc[0]
    
    prompt = f"""
Actúa como un experto creador de contenido de TikTok especializado en el nicho de {nicho}.
Basado en el análisis de datos de los videos más virales de la competencia, necesito que me escribas un guion para un video corto (menos de 60 segundos) que cumpla ESTRICTAMENTE con estas métricas técnicas:

1. RITMO DE HABLA: El guion debe estar pensado para leerse a {mejor['wpm']} palabras por minuto (muy importante para la retención).
2. DINAMISMO VISUAL: El video tendrá {mejor['cortes_min']} cortes de cámara por minuto. Escribe indicaciones visuales [en corchetes] a lo largo del guion para indicar cada cambio de plano o aparición de texto en pantalla.
3. TONO EMOCIONAL: El tono general del video debe ser '{mejor['sentimiento']}'.
4. PALABRAS CLAVE OBLIGATORIAS: Debes incluir estas palabras en los primeros 10 segundos para activar el SEO de TikTok: {mejor['palabras_clave']}.

El guion debe empezar con un gancho disruptivo. Dame solo el guion final, sin texto de introducción.
    """
    
    return prompt.strip()