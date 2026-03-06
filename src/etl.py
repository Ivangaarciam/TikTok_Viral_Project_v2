# src/etl.py
import sqlite3
import pandas as pd
import os
import config

def ejecutar_pipeline_limpieza():
    print("\n🧹 --- INICIANDO PIPELINE ETL (Limpieza de Datos) --- 🧹")
    
    if not os.path.exists(config.ARCHIVO_DB):
        print("❌ No se encontró la base de datos.")
        return None

    # 1. EXTRACT (Extraer)
    print("📥 1. Extrayendo datos en bruto...")
    conn = sqlite3.connect(config.ARCHIVO_DB)
    df = pd.read_sql_query("SELECT * FROM videos", conn)
    
    if df.empty:
        print("⚠️ La base de datos está vacía.")
        conn.close()
        return None

    # 2. TRANSFORM (Transformar y Limpiar)
    print("🧬 2. Transformando y limpiando (Feature Engineering)...")
    
    # A) Eliminar duplicados (por si procesaste el mismo link dos veces por error)
    filas_antes = len(df)
    df = df.drop_duplicates(subset=['url'], keep='last')
    duplicados_borrados = filas_antes - len(df)
    
    # B) Manejo de Valores Nulos (NaN)
    # Si algún video no tiene WPM o no se detectaron caras, rellenamos con 0 en vez de dejar un vacío que rompa la IA
    columnas_numericas = ['wpm', 'pct_caras', 'cortes_min', 'brillo', 'rms_audio']
    df[columnas_numericas] = df[columnas_numericas].fillna(0)
    
    # C) Crear variables "Target" (Lo que la IA intentará predecir luego)
    # Creamos la columna 'es_viral': 1 si tiene más de 100k vistas (puedes ajustar este número), 0 si no.
    UMBRAL_VIRAL = 100000 
    df['es_viral'] = (df['vistas'] >= UMBRAL_VIRAL).astype(int)
    
    # Calculamos el Engagement Rate para tenerlo listo
    df['interacciones'] = df['likes'] + df['guardados'] + df['comentarios'] + df['shares']
    df['engagement_rate'] = (df['interacciones'] / df['vistas'] * 100).fillna(0)

    # 3. LOAD (Cargar datos limpios)
    print("📤 3. Guardando datos listos para Machine Learning...")
    # Guardamos esta versión limpia en una NUEVA tabla para no romper los datos originales
    df.to_sql('videos_limpios', conn, if_exists='replace', index=False)
    conn.close()

    print("\n✅ --- RESUMEN DE LIMPIEZA ---")
    print(f"   🗑️ Duplicados eliminados: {duplicados_borrados}")
    print(f"   ✨ Total de videos listos para entrenar IA: {len(df)}")
    print(f"   🎯 Videos etiquetados como 'Virales': {df['es_viral'].sum()}")
    print("----------------------------------\n")
    
    return df

if __name__ == "__main__":
    ejecutar_pipeline_limpieza()