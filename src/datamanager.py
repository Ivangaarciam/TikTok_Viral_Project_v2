# src/datamanager.py
import sqlite3
import os
from datetime import datetime
import config

def migrar_base_datos():
    if not os.path.exists(config.ARCHIVO_DB): return
    conn = sqlite3.connect(config.ARCHIVO_DB)
    cursor = conn.cursor()
    # Migración de ayer
    try: cursor.execute("ALTER TABLE videos ADD COLUMN palabras_clave TEXT")
    except sqlite3.OperationalError: pass
    
    # Migración de HOY
    try:
        cursor.execute("ALTER TABLE videos ADD COLUMN sentimiento TEXT")
        print("⚙️ Base de datos actualizada: Columna 'sentimiento' añadida.")
    except sqlite3.OperationalError: pass
    
    conn.commit()
    conn.close()

def crear_tablas():
    conn = sqlite3.connect(config.ARCHIVO_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_proceso TEXT, url TEXT UNIQUE, autor TEXT,
            vistas INTEGER, likes INTEGER, guardados INTEGER, comentarios INTEGER, shares INTEGER,
            resolucion TEXT, fps REAL, duracion REAL, brillo REAL, rms_audio REAL, cortes_min REAL,
            pct_caras REAL, wpm INTEGER, gancho TEXT, transcripcion TEXT,
            palabras_clave TEXT, sentimiento TEXT
        )
    ''')
    conn.commit()
    conn.close()
    migrar_base_datos()

def guardar_datos(url, datos_tecnicos, datos_audio, palabras_clave, sentimiento, stats_sociales):
    print(f"💾  Guardando en Base de Datos SQL...")
    try:
        conn = sqlite3.connect(config.ARCHIVO_DB)
        cursor = conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        sql = '''INSERT INTO videos (fecha_proceso, url, autor, vistas, likes, guardados, 
                 comentarios, shares, resolucion, fps, duracion, brillo, rms_audio, cortes_min, 
                 pct_caras, wpm, gancho, transcripcion, palabras_clave, sentimiento) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        
        datos = (
            fecha, url, stats_sociales['autor'], stats_sociales['vistas'], stats_sociales['likes'],
            stats_sociales['guardados'], stats_sociales['comentarios'], stats_sociales['shares'],
            datos_tecnicos['resolucion'], datos_tecnicos['fps'], datos_tecnicos['duracion'],
            datos_tecnicos['brillo'], datos_tecnicos['rms'], datos_tecnicos['cpm'],
            datos_tecnicos['pct_caras'], datos_audio['wpm'], datos_audio['gancho'], 
            datos_audio['texto'], palabras_clave, sentimiento # <--- Nuevo dato al final
        )
        cursor.execute(sql, datos)
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        print("⚠️  AVISO: Este video ya existía.")
        return False
    except Exception as e:
        print(f"❌ Error guardando en SQL: {e}")
        return False