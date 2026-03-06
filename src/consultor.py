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