# src/main.py
import os
import glob
import config

# --- NUESTRO EQUIPO DE EXPERTOS ---
import downloader   
import processor    
import analyzer     
import datamanager  
import nlp
import scoring
import benchmarking
import predictor

def limpiar_area():
    archivos = [config.NOMBRE_VIDEO_FINAL, config.NOMBRE_AUDIO_FINAL]
    for f in glob.glob(f"{config.NOMBRE_CRUDO}*"):
        archivos.append(f)
    for f in archivos:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

def procesar_video(url):
    print(f"\n🎬 INICIANDO PROCESO V3: {url}")
    limpiar_area()

    # 1. Descarga de video y metadatos sociales
    stats_sociales = downloader.descargar_video(url)
    if not stats_sociales: 
        print("❌ Error en la descarga.")
        return

    # 2. Conversión a formatos de trabajo (Audio/Video optimizado)
    if not processor.convertir_medios():
        print("❌ Fallo en conversión de medios.")
        return

    # 3. Transcripción con IA (Whisper)
    datos_audio = processor.transcribir_audio()
    if not datos_audio: 
        print("❌ Fallo en la transcripción.")
        return

    # 4. Inteligencia de Lenguaje (Keywords, Sentimiento y Nicho)
    palabras_clave = nlp.extraer_palabras_clave(datos_audio['texto'])
    sentimiento = nlp.analizar_sentimiento(datos_audio['texto'])
    
    # NUEVO: Clasificación automática basada en el diccionario de nichos
    nicho_info = nlp.clasificar_nicho(datos_audio['texto'], url)
    print(f"🏷️ Nicho Detectado: {nicho_info['cat_general']} > {nicho_info['nicho']}")

    # 5. Análisis de Visión y Audio (Métricas técnicas)
    datos_tecnicos = analyzer.calcular_metricas(config.NOMBRE_VIDEO_FINAL, config.NOMBRE_AUDIO_FINAL)
    if not datos_tecnicos: 
        print("❌ Fallo en el análisis técnico.")
        return

    # 6. Guardado Estructurado en SQL (Versión 3.0)
    nlp_info = {
        'keywords': palabras_clave, 
        'sentiment': sentimiento
    }
    
    guardado_exitoso = datamanager.guardar_datos_v3(
        url, 
        datos_tecnicos, 
        datos_audio, 
        nlp_info, 
        stats_sociales, 
        nicho_info
    )
    
    # 7. Feedback y Predicción Final
    if guardado_exitoso:
        print("✅ ¡Datos guardados y clasificados con éxito!")
        scoring.calcular_score_viral(datos_tecnicos, datos_audio, stats_sociales)
        benchmarking.comparar_con_virales(datos_tecnicos, datos_audio)
        predictor.predecir_viralidad(datos_tecnicos, datos_audio)
    else:
        print("⚠️ El video ya existe o hubo un error al guardar.")

def main():
    if not os.path.exists(config.FFMPEG_PATH):
        print(f"⛔ ERROR: No encuentro ffmpeg.exe en: {config.FFMPEG_PATH}")
        return

    # --- ACTUALIZAR LA BASE DE DATOS ANTES DE EMPEZAR ---
    datamanager.crear_tablas()

    print("\n--- TIKTOK REVERSE ENGINEER v3.0 (SaaS Ready) ---")
    print("1. Modo Manual (Pegar Link)")
    print("2. Modo Automático (Leer videos.txt)")
    print("3. Modo MINERÍA (Por Creador/Competidor) ⛏️")
    op = input("👉 Opción: ")
    
    urls = []
    if op == "1": 
        link = input("Link: ").strip()
        if link: urls.append(link)
    elif op == "2" and os.path.exists(config.VIDEOS_TXT_PATH):
        with open(config.VIDEOS_TXT_PATH, "r") as f: 
            urls = [x.strip() for x in f.readlines() if x.strip()]
    elif op == "3":
        # --- NUEVA MINERÍA POR COMPETIDOR ---
        creador = input("Usuario de TikTok a analizar (ej. midudev o nike): ").strip()
        cantidad = int(input("¿Cuántos videos analizar? (Recomendado 3-5): ") or 5)
        urls = downloader.buscar_videos_perfil(creador, cantidad)
    else:
        print("⚠️ Opción inválida.")
            
    total = len(urls)
    if total == 0:
        print("⚠️ No se encontraron videos para procesar.")
    else:
        for i, u in enumerate(urls):
            print(f"\n--- VIDEO {i+1} de {total} ---")
            procesar_video(u)
    
    print("\n🏁 CICLO TERMINADO.")
    limpiar_area()

if __name__ == "__main__":
    main()