# src/consultor.py
import sqlite3
import pandas as pd
import config
import os
import nlp  # <--- Necesitamos que el consultor sepa usar nuestro motor NLP

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

def obtener_metricas_exito(nicho):
    """
    Calcula el promedio de las métricas técnicas de los videos 
    con más engagement de un nicho concreto.
    """
    conn = sqlite3.connect(config.ARCHIVO_DB)
    # Seleccionamos el top 20% de videos del nicho por engagement
    query = f"""
    SELECT wpm, cortes_min, pct_caras, brillo, rms_audio
    FROM videos 
    WHERE nicho = '{nicho}' 
    ORDER BY (likes * 1.0 / vistas) DESC 
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        return None
        
    # Devolvemos un diccionario con los promedios "perfectos"
    return {
        "wpm_ideal": df['wpm'].mean(),
        "cpm_ideal": df['cortes_min'].mean(),
        "caras_ideal": df['pct_caras'].mean(),
        "brillo_ideal": df['brillo'].mean(),
        "rms_ideal": df['rms_audio'].mean()
    }

def evaluar_borrador_guion(texto_guion, nicho):
    """
    Lee un guion escrito por el usuario, extrae sus características (NLP)
    y lo compara con los líderes de su nicho en la base de datos.
    """
    if len(texto_guion.split()) < 10:
        return "⚠️ El guion es demasiado corto para ser evaluado. Necesito al menos 10 palabras."

    # 1. La IA analiza el borrador del usuario
    sentimiento_usuario = nlp.analizar_sentimiento(texto_guion)
    keywords_usuario = set(nlp.extraer_palabras_clave(texto_guion).split(", "))
    palabras_totales = len(texto_guion.split())

    # 2. Buscamos el estándar de oro en la base de datos
    conn = sqlite3.connect(config.ARCHIVO_DB)
    query = f"""
    SELECT wpm, sentimiento, palabras_clave
    FROM videos 
    WHERE nicho = '{nicho}' 
    ORDER BY (likes * 1.0 / vistas) DESC 
    LIMIT 5
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return f"No tengo suficientes datos del nicho '{nicho}' para evaluar tu guion."

    # 3. Extraemos los patrones ganadores
    wpm_promedio = int(df['wpm'].mean())
    sentimientos_top = df['sentimiento'].mode()[0] # El sentimiento que más se repite
    
    # Recopilamos todas las palabras clave ganadoras
    keywords_top = set()
    for kw_list in df['palabras_clave']:
        for word in str(kw_list).split(", "):
            if word: keywords_top.add(word)

    # 4. Construimos el veredicto (El Reporte)
    duracion_estimada = (palabras_totales / wpm_promedio) * 60

    reporte = f"### ⚖️ Auditoría de tu Guion (Nicho: {nicho})\n\n"
    reporte += f"⏱️ **Duración Estimada:** {duracion_estimada:.1f} segundos (a un ritmo viral de {wpm_promedio} WPM).\n\n"

    # Evaluación de Tono
    if sentimiento_usuario == sentimientos_top:
        reporte += f"✅ **Tono Emocional:** Perfecto. Tu guion es '{sentimiento_usuario}', igual que los líderes de tu nicho.\n"
    else:
        reporte += f"⚠️ **Tono Emocional:** Tu guion es '{sentimiento_usuario}', pero en este nicho funciona mejor el tono '{sentimientos_top}'. Considera ajustar la energía de tus palabras.\n"

    # Evaluación de SEO / Keywords
    aciertos_seo = keywords_usuario.intersection(keywords_top)
    if aciertos_seo:
        reporte += f"✅ **SEO de TikTok:** Muy bien. Has incluido términos ganadores: {', '.join(aciertos_seo)}.\n"
    else:
        sugerencias = list(keywords_top)[:5]
        reporte += f"❌ **SEO de TikTok:** No estás usando el vocabulario en tendencia. Intenta incluir términos como: {', '.join(sugerencias)}.\n"

    # Veredicto final
    if sentimiento_usuario == sentimientos_top and aciertos_seo:
        reporte += "\n🚀 **VEREDICTO:** Guion altamente optimizado. ¡Pasa a producción!"
    else:
        reporte += "\n🔧 **VEREDICTO:** El guion necesita un par de ajustes antes de grabar para maximizar la retención."

    return reporte


if __name__ == "__main__":
    # Script de prueba
    mi_guion = "Bienvenidos a un nuevo video. Hoy os voy a enseñar cómo automatizar tareas usando inteligencia artificial de forma muy triste y aburrida."
    nicho_prueba = "Content Creation" # Cambia esto a uno de los nichos que minaste ayer
    
    print("\nEvaluando borrador...")
    resultado = evaluar_borrador_guion(mi_guion, nicho_prueba)
    print("\n" + resultado)