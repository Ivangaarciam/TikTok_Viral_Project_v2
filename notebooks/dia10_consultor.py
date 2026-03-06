import pandas as pd
import os
import sys

print("------------------------------------------")
print("🧠 INICIANDO CONSULTOR DE DATOS...")
print("------------------------------------------")

ARCHIVO_CSV = "cerebro_tiktok.csv"

# 1. Comprobación de seguridad
if not os.path.exists(ARCHIVO_CSV):
    print(f"❌ ERROR: No encuentro el archivo '{ARCHIVO_CSV}'.")
    print("👉 SOLUCIÓN: Ejecuta primero 'main.py' para analizar un video.")
    sys.exit()

print("📂 Archivo encontrado. Intentando leer...")

try:
    # Intentamos leer con punto y coma (Formato nuevo)
    # on_bad_lines='skip' salta las líneas rotas si las hubiera
    df = pd.read_csv(ARCHIVO_CSV, sep=';', decimal=',', encoding='utf-8-sig', on_bad_lines='skip')
    
    # Verificamos si las columnas existen
    if 'BRILLO' not in df.columns:
        print("❌ ERROR DE FORMATO: El archivo CSV tiene un formato antiguo.")
        print("👉 SOLUCIÓN: Borra el archivo 'cerebro_tiktok.csv' y genera uno nuevo con main.py")
        sys.exit()

    total_videos = len(df)
    print(f"✅ Lectura exitosa. Analizando {total_videos} videos...\n")

    if total_videos == 0:
        print("⚠️ El archivo está vacío. Analiza videos primero.")
        sys.exit()

    # --- ESTADÍSTICAS ---
    promedio_fps = df['FPS'].mean()
    promedio_brillo = df['BRILLO'].mean()
    promedio_audio = df['AUDIO_RMS'].mean()

    print("📊 --- TUS ESTADÍSTICAS ---")
    print(f"   • Videos analizados: {total_videos}")
    print(f"   • Fluidez media:     {promedio_fps:.1f} FPS")
    print(f"   • Brillo medio:      {promedio_brillo:.1f} (Ideal: 100-150)")
    print(f"   • Audio medio:       {promedio_audio:.4f} RMS")

    print("\n🚨 --- DIAGNÓSTICO ---")
    
    # Videos oscuros (< 60)
    oscuros = df[df['BRILLO'] < 60]
    if len(oscuros) > 0:
        print(f"⚠️  {len(oscuros)} videos son MUY OSCUROS.")
    else:
        print("✅  Iluminación correcta en general.")

    # Videos mudos (< 0.02)
    mudos = df[df['AUDIO_RMS'] < 0.02]
    if len(mudos) > 0:
        print(f"⚠️  {len(mudos)} videos tienen AUDIO MUY BAJO.")
    else:
        print("✅  Niveles de audio correctos.")

    print("\n------------------------------------------")
    print("🏁 ANÁLISIS FINALIZADO")
    
except PermissionError:
    print("❌ ERROR DE PERMISOS: Tienes el archivo Excel abierto.")
    print("👉 SOLUCIÓN: Cierra el Excel y vuelve a ejecutar este script.")
except Exception as e:
    print(f"❌ ERROR INESPERADO: {e}")

# Esto evita que la ventana se cierre de golpe si lo ejecutas fuera de VS Code
input("\nPresiona ENTER para cerrar...")