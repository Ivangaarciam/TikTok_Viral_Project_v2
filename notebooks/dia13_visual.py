import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

print("--- 🎨 GENERADOR DE GRÁFICAS TIKTOK ---")

ARCHIVO_CSV = "cerebro_tiktok.csv"

if not os.path.exists(ARCHIVO_CSV):
    print("❌ No encuentro el CSV. Analiza videos primero.")
    sys.exit()

try:
    # 1. Cargar Datos
    df = pd.read_csv(ARCHIVO_CSV, sep=';', decimal=',', encoding='utf-8-sig', on_bad_lines='skip')
    
    # Filtramos videos con muy pocas vistas para no ensuciar el gráfico
    # (Opcional, pero ayuda a ver mejor los datos importantes)
    df = df[df['VISTAS'] > 0]

    if len(df) < 3:
        print("⚠️ Necesitas al menos 3 videos para hacer una gráfica decente.")
        sys.exit()

    print(f"📊 Generando gráficas con {len(df)} videos...")

    # --- GRÁFICA 1: ILUMINACIÓN VS ÉXITO ---
    plt.figure(figsize=(10, 6)) # Tamaño de la imagen
    
    # Eje X: Brillo (0 a 255)
    # Eje Y: Vistas
    # s=100 es el tamaño de los puntos
    # alpha=0.7 hace los puntos semitransparentes
    plt.scatter(df['BRILLO'], df['VISTAS'], color='orange', s=100, alpha=0.7, edgecolors='black')
    
    plt.title('¿Influye la LUZ en las VISTAS?', fontsize=16)
    plt.xlabel('Nivel de Brillo (0=Oscuro, 255=Blanco)', fontsize=12)
    plt.ylabel('Cantidad de Vistas', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5) # Cuadrícula de fondo
    
    # Dibujar línea de "Zona Ideal" (Entre 80 y 180 suele ser buena luz)
    plt.axvline(x=80, color='red', linestyle='--', label='Muy Oscuro')
    plt.axvline(x=180, color='red', linestyle='--', label='Muy Quemado')
    plt.legend()
    
    # Guardar imagen
    plt.savefig('grafica_iluminacion.png')
    print("✅ Gráfica 1 guardada: 'grafica_iluminacion.png'")
    
    # Limpiamos para la siguiente gráfica
    plt.clf() 

    # --- GRÁFICA 2: AUDIO VS ÉXITO ---
    plt.figure(figsize=(10, 6))
    
    # Eje X: Audio RMS
    # Eje Y: Vistas
    plt.scatter(df['AUDIO_RMS'], df['VISTAS'], color='blue', s=100, alpha=0.7, edgecolors='black')
    
    plt.title('¿Influye el VOLUMEN en las VISTAS?', fontsize=16)
    plt.xlabel('Potencia de Audio (RMS)', fontsize=12)
    plt.ylabel('Cantidad de Vistas', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Zona de Audio Bajo
    plt.axvline(x=0.05, color='red', linestyle='--', label='Audio Bajo/Mudo')
    plt.legend()
    
    plt.savefig('grafica_audio.png')
    print("✅ Gráfica 2 guardada: 'grafica_audio.png'")

    print("\n🚀 ¡Listo! Ve a tu carpeta y abre las imágenes PNG.")

except Exception as e:
    print(f"❌ Error generando gráficas: {e}")

input("\nPresiona ENTER para salir...")