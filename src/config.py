# src/config.py
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# --- MAGIA PARA LA NUBE ---
# Buscamos el ejecutable local
FFMPEG_LOCAL = os.path.join(BASE_DIR, "ffmpeg.exe")

if os.path.exists(FFMPEG_LOCAL):
    FFMPEG_PATH = FFMPEG_LOCAL # Estamos en tu PC Windows
else:
    # Estamos en la Nube (Linux), buscamos el ffmpeg instalado en el servidor
    FFMPEG_PATH = shutil.which("ffmpeg") or "ffmpeg"

COOKIES_PATH = os.path.join(BASE_DIR, "cookies.txt")
VIDEOS_TXT_PATH = os.path.join(BASE_DIR, "videos.txt")

NOMBRE_CRUDO = os.path.join(DATA_DIR, "descarga_bruta")
NOMBRE_VIDEO_FINAL = os.path.join(DATA_DIR, "video_final.mp4")
NOMBRE_AUDIO_FINAL = os.path.join(DATA_DIR, "audio_final.wav")
ARCHIVO_CSV = os.path.join(DATA_DIR, "cerebro_tiktok.csv")
ARCHIVO_DB = os.path.join(DATA_DIR, "cerebro_tiktok.db")

ANCHO_ANALISIS = 64
ALTO_ANALISIS = 64
DURACION_TRANSCRIPCION = 60