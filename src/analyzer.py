# src/analyzer.py
import cv2
import numpy as np
import os
from moviepy import AudioFileClip
import config

def calcular_metricas(ruta_video, ruta_audio):
    print(f"🕵️  Analizando video: {os.path.basename(ruta_video)}...")
    
    cap = cv2.VideoCapture(ruta_video)
    if not cap.isOpened(): return None

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0: fps = 30
    
    # --- IA DE ROSTROS DE OPENCV ---
    ruta_cascade = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    detector_caras = cv2.CascadeClassifier(ruta_cascade)
    
    suma_brillo, muestras_brillo, cortes = 0, 0, 0
    frames_con_cara, muestras_caras = 0, 0
    frame_anterior = None
    frame_count = 0
    tamano_analisis = (config.ANCHO_ANALISIS, config.ALTO_ANALISIS) 
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 1. Brillo
        if frame_count % 30 == 0:
            suma_brillo += np.mean(gray_frame)
            muestras_brillo += 1
            
        # 2. Cortes
        if frame_count % 5 == 0:
            frame_mini = cv2.resize(gray_frame, tamano_analisis)
            if frame_anterior is not None:
                if np.mean(cv2.absdiff(frame_mini, frame_anterior)) > 30: 
                    cortes += 1
            frame_anterior = frame_mini
            
        # 3. ROSTROS (Analizamos 2 veces por segundo para no saturar el PC)
        intervalo_caras = int(fps / 2) if fps > 0 else 15
        if frame_count % intervalo_caras == 0:
            muestras_caras += 1
            # Detectar caras en la imagen gris
            caras = detector_caras.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(caras) > 0:
                frames_con_cara += 1

        frame_count += 1
    cap.release()
    
    duracion_real = frame_count / fps
    cpm = (cortes / duracion_real) * 60 if duracion_real > 0 else 0
    porcentaje_caras = round((frames_con_cara / muestras_caras) * 100, 2) if muestras_caras > 0 else 0

    rms = 0
    try:
        if os.path.exists(ruta_audio):
            clip = AudioFileClip(ruta_audio)
            arr = clip.to_soundarray(fps=44100)
            limit = 20 * 44100
            if len(arr) > limit: arr = arr[:limit]
            rms = np.sqrt(np.mean(arr.astype(float)**2))
            clip.close()
    except: pass

    print(f"   👤 Presencia humana detectada: {porcentaje_caras}% del video")

    return {
        "resolucion": f"{w}x{h}", "fps": fps, "duracion": duracion_real,
        "brillo": round(suma_brillo / max(1, muestras_brillo), 2),
        "cpm": cpm, "rms": rms, 
        "pct_caras": porcentaje_caras # <--- NUEVO DATO
    }