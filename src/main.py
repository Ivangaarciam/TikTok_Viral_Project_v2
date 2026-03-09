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
    print(f"\n🎬 INICIANDO PROCESO: {url}")
    limpiar_area()

    stats_sociales = downloader.descargar_video(url)
    if not stats_sociales: return

    if not processor.convertir_medios():
        print("❌ Fallo en conversión de medios.")
        return

    datos_audio = processor.transcribir_audio()
    if not datos_audio: return

    palabras_clave = nlp.extraer_palabras_clave(datos_audio['texto'])
    sentimiento = nlp.analizar_sentimiento(datos_audio['texto'])

    datos_tecnicos = analyzer.calcular_metricas(config.NOMBRE_VIDEO_FINAL, config.NOMBRE_AUDIO_FINAL)
    if not datos_tecnicos: return

    # Guardamos todos los datos (incluyendo el sentimiento)
    guardado_exitoso = datamanager.guardar_datos(url, datos_tecnicos, datos_audio, palabras_clave, sentimiento, stats_sociales)
    
    if guardado_exitoso:
        scoring.calcular_score_viral(datos_tecnicos, datos_audio, stats_sociales)
        benchmarking.comparar_con_virales(datos_tecnicos, datos_audio)
        predictor.predecir_viralidad(datos_tecnicos, datos_audio)

def main():
    if not os.path.exists(config.FFMPEG_PATH):
        print(f"⛔ ERROR: No encuentro ffmpeg.exe en: {config.FFMPEG_PATH}")
        return

    # --- EL FIX DE HOY: ACTUALIZAR LA BASE DE DATOS ANTES DE EMPEZAR ---
    datamanager.crear_tablas()

    print("--- TIKTOK REVERSE ENGINEER v2.0 ---")
    print("1. Modo Manual (Pegar Link)")
    print("2. Modo Automático (Leer videos.txt)")
    op = input("👉 Opción: ")
    
    urls = []
    if op == "1": 
        link = input("Link: ").strip()
        if link: urls.append(link)
    elif op == "2" and os.path.exists(config.VIDEOS_TXT_PATH):
        with open(config.VIDEOS_TXT_PATH, "r") as f: 
            urls = [x.strip() for x in f.readlines() if x.strip()]
    else:
        print(f"⚠️ Opción inválida o no encuentro {config.VIDEOS_TXT_PATH}")
            
    total = len(urls)
    for i, u in enumerate(urls):
        print(f"\n--- VIDEO {i+1} de {total} ---")
        procesar_video(u)
    
    print("\n🏁 CICLO TERMINADO.")
    limpiar_area()

if __name__ == "__main__":
    main()