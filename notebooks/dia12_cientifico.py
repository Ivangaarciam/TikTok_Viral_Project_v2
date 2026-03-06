import pandas as pd
import os
import sys

print("========================================")
print("🧪 LABORATORIO DE DATOS TIKTOK (Día 12)")
print("========================================")

ARCHIVO_CSV = "cerebro_tiktok.csv"

# 1. CARGA DE DATOS BLINDADA
if not os.path.exists(ARCHIVO_CSV):
    print("❌ ERROR: No encuentro 'cerebro_tiktok.csv'.")
    print("👉 Ejecuta main.py y analiza al menos 3 videos antes de venir aquí.")
    sys.exit()

try:
    # Leemos el CSV con formato español (punto y coma)
    df = pd.read_csv(ARCHIVO_CSV, sep=';', decimal=',', encoding='utf-8-sig', on_bad_lines='skip')
    
    num_videos = len(df)
    print(f"📂 Base de datos cargada: {num_videos} videos analizados.\n")
    
    if num_videos < 2:
        print("⚠️ Hacen falta más datos para encontrar patrones. Analiza al menos 5 videos.")

    # 2. DEFINICIÓN DE "ÉXITO" (La Fórmula Viral)
    # Detectamos si tenemos datos de Guardados reales
    suma_guardados = df['GUARDADOS'].sum()
    
    if suma_guardados > 0:
        print("✅ Datos de 'Guardados' detectados. Usando Fórmula Avanzada.")
        # Fórmula: (Likes + Guardados*3) / Vistas * 100
        # Multiplicamos guardados por 3 porque valen más para el algoritmo
        df['PUNTUACION'] = ((df['LIKES'] + (df['GUARDADOS'] * 3)) / df['VISTAS']) * 100
    else:
        print("⚠️ No hay datos de 'Guardados' (o son 0). Usando Fórmula Básica (Likes).")
        print("💡 Pista: Usa las cookies para desbloquear los Guardados.")
        df['PUNTUACION'] = (df['LIKES'] / df['VISTAS']) * 100

    # Limpiamos posibles infinitos si Vistas es 0
    df = df.fillna(0)

    # 3. ANÁLISIS DE CORRELACIONES (El Cerebro)
    print("\n📊 --- RESULTADOS DEL ANÁLISIS ---")

    # A) ILUMINACIÓN (Brillo)
    # Dividimos los videos en dos grupos: Claros (>80) y Oscuros (<80)
    claros = df[df['BRILLO'] > 80]['PUNTUACION'].mean()
    oscuros = df[df['BRILLO'] <= 80]['PUNTUACION'].mean()
    
    print(f"💡 IMPACTO VISUAL:")
    print(f"   • Videos Claros:  {claros:.2f} puntos de éxito")
    print(f"   • Videos Oscuros: {oscuros:.2f} puntos de éxito")
    
    if claros > (oscuros * 1.1): # Si son un 10% mejores
        print("   -> 🚀 CONCLUSIÓN: Tu audiencia prefiere videos BIEN ILUMINADOS.")
    elif oscuros > (claros * 1.1):
        print("   -> 🌑 CONCLUSIÓN: Sorprendente. Tus videos OSCUROS funcionan mejor.")
    else:
        print("   -> 🤷‍♂️ CONCLUSIÓN: La iluminación no está siendo el factor decisivo.")

    # B) AUDIO (Volumen RMS)
    # Audio fuerte (>0.05) vs Audio bajo (<0.05)
    fuerte = df[df['AUDIO_RMS'] > 0.05]['PUNTUACION'].mean()
    bajo = df[df['AUDIO_RMS'] <= 0.05]['PUNTUACION'].mean()
    
    print(f"\n🔊 IMPACTO SONORO:")
    print(f"   • Audio Fuerte: {fuerte:.2f} puntos")
    print(f"   • Audio Bajo:   {bajo:.2f} puntos")
    
    if bajo > fuerte:
        print("   -> ⚠️ ALERTA: Tus videos con audio bajo tienen mejor nota. ¿Quizás la música estaba muy alta en los otros?")
    elif fuerte > bajo:
        print("   -> ✅ CONCLUSIÓN: El audio nítido ayuda a retener audiencia.")

    # 4. HALL DE LA FAMA
    best_video = df.loc[df['PUNTUACION'].idxmax()]
    
    print(f"\n🏆 TU MEJOR VIDEO (Score: {best_video['PUNTUACION']:.2f})")
    print(f"   🎬 Link: {best_video['URL']}")
    print(f"   ⚙️ Técnica: Brillo {best_video['BRILLO']} | Audio {best_video['AUDIO_RMS']}")
    print(f"   ❤️ Social: {best_video['LIKES']} Likes | {best_video['GUARDADOS']} Guardados")

except Exception as e:
    print(f"❌ Ocurrió un error al analizar: {e}")
    print("Revisa que el archivo CSV no esté abierto en Excel.")

input("\nPresiona ENTER para cerrar...")