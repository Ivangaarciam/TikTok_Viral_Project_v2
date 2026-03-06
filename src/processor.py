# src/processor.py
import os
import glob
import subprocess
import whisper
import config

os.environ["PATH"] += os.pathsep + config.BASE_DIR

def convertir_medios():
    print("\n⚙️  Fase 2: SEPARANDO AUDIO Y VIDEO...")
    files = glob.glob(f"{config.NOMBRE_CRUDO}*")
    if not files: return False
    archivo_origen = files[0]

    subprocess.run([config.FFMPEG_PATH, "-y", "-i", archivo_origen, "-vn", "-ac", "1", "-ar", "16000", config.NOMBRE_AUDIO_FINAL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([config.FFMPEG_PATH, "-y", "-i", archivo_origen, "-c:v", "libx264", "-an", config.NOMBRE_VIDEO_FINAL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(config.NOMBRE_AUDIO_FINAL) and os.path.exists(config.NOMBRE_VIDEO_FINAL):
        try: os.remove(archivo_origen)
        except: pass
        return True
    return False

def transcribir_audio():
    print(f"\n👂 Fase 3.1: ESCUCHANDO CON WHISPER AI...")
    if not os.path.exists(config.NOMBRE_AUDIO_FINAL):
        print("❌ Error: No encuentro el archivo de audio.")
        return None
    
    try:
        print("   ⏳ Analizando el guion y los tiempos...")
        model = whisper.load_model("base")
        result = model.transcribe(config.NOMBRE_AUDIO_FINAL, fp16=False)
        
        texto_completo = result["text"].strip()
        
        # 1. Extraer el GANCHO (Primeros 5 segundos)
        gancho = ""
        for segment in result["segments"]:
            if segment["start"] < 5.0:
                gancho += segment["text"] + " "
                
        # 2. Calcular WPM (Palabras por minuto)
        # Tomamos el tiempo de fin del último segmento para saber cuánto dura la voz
        duracion_voz = result["segments"][-1]["end"] if result["segments"] else 1
        num_palabras = len(texto_completo.split())
        wpm = round((num_palabras / duracion_voz) * 60) if duracion_voz > 0 else 0
        
        print(f"   🎣 Gancho detectado: \"{gancho.strip()}\"")
        print(f"   🗣️ Ritmo de habla: {wpm} Palabras Por Minuto")
        
        return {
            "texto": texto_completo,
            "gancho": gancho.strip(),
            "wpm": wpm
        }
        
    except Exception as e:
        print(f"   ⚠️ Error crítico en Whisper: {e}")
        return None