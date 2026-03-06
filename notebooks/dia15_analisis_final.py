import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Ajustes visuales para la terminal
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("========================================")
print("🎬 DIRECTOR DE DATOS (Análisis Ritmo)")
print("========================================")

ARCHIVO_CSV = "cerebro_tiktok.csv"

if not os.path.exists(ARCHIVO_CSV):
    print("❌ No encuentro el CSV. Usa main.py primero.")
    sys.exit()

try:
    # 1. CARGA DE DATOS
    df = pd.read_csv(ARCHIVO_CSV, sep=';', decimal=',', encoding='utf-8-sig', on_bad_lines='skip')
    
    # Verificamos que tengas la columna nueva
    if 'CORTES_MIN' not in df.columns:
        print("❌ Tu CSV es antiguo (no tiene columna de cortes).")
        print("👉 Borra el CSV y analiza videos nuevos con el main.py de ayer.")
        sys.exit()

    # Limpieza
    df = df.dropna(subset=['URL'])
    df = df.fillna(0) # Rellenar huecos con 0

    print(f"📂 Analizando {len(df)} videos.\n")

    # 2. CÁLCULO DE PUNTUACIÓN VIRAL
    # Si hay guardados, fórmula completa. Si no, fórmula simple.
    suma_guardados = df['GUARDADOS'].sum()
    
    if suma_guardados > 0:
        # Fórmula VIP: (Likes + Comentarios*2 + Guardados*3) / Vistas * 1000
        df['PUNTUACION'] = ((df['LIKES'] + (df['COMENTARIOS']*2) + (df['GUARDADOS']*3)) / df['VISTAS']) * 1000
    else:
        # Fórmula LITE
        df['PUNTUACION'] = ((df['LIKES'] + (df['SHARES']*2)) / df['VISTAS']) * 1000

    # 3. ANÁLISIS DE RITMO (CPM)
    print("📊 --- IMPACTO DEL RITMO DE EDICIÓN ---")
    
    # Creamos 3 categorías de velocidad
    # Lento: 0-8 cortes/min | Medio: 8-20 cortes/min | Frenético: >20
    bins = [0, 8, 20, 1000]
    labels = ['Lento (Talk)', 'Dinámico', 'Frenético']
    df['TIPO_RITMO'] = pd.cut(df['CORTES_MIN'], bins=bins, labels=labels, right=False)
    
    # Promedio de éxito por grupo
    grupo_ritmo = df.groupby('TIPO_RITMO', observed=False)['PUNTUACION'].mean()
    
    print(grupo_ritmo)
    print("\n--------------------------------")
    
    mejor_ritmo = grupo_ritmo.idxmax()
    print(f"🚀 CONCLUSIÓN: Tu estilo ganador es: {mejor_ritmo.upper()}")
    
    if mejor_ritmo == 'Lento (Talk)':
        print("   -> Tu audiencia valora el contenido pausado/hablado.")
    elif mejor_ritmo == 'Dinámico':
        print("   -> El equilibrio perfecto. Ni te duermes ni te mareas.")
    elif mejor_ritmo == 'Frenético':
        print("   -> Tu nicho quiere estímulos constantes (estilo MrBeast).")

    # 4. GENERACIÓN DE GRÁFICA VISUAL
    print("\n🎨 Generando mapa visual del ritmo...")
    
    plt.figure(figsize=(10, 6))
    
    # Eje X: Cortes por Minuto
    # Eje Y: Puntuación Viral (Éxito)
    plt.scatter(df['CORTES_MIN'], df['PUNTUACION'], c='purple', s=100, alpha=0.6, edgecolors='black')
    
    plt.title('¿A más Velocidad, más Éxito?', fontsize=16)
    plt.xlabel('Cortes por Minuto (CPM)', fontsize=12)
    plt.ylabel('Puntuación Viral', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Marcar las zonas
    plt.axvline(x=8, color='green', linestyle='--', label='Frontera Lento/Medio')
    plt.axvline(x=20, color='red', linestyle='--', label='Frontera Frenético')
    plt.legend()
    
    nombre_img = 'grafica_ritmo_edicion.png'
    plt.savefig(nombre_img)
    print(f"✅ Imagen guardada: {nombre_img}")
    
    # 5. EL VIDEO MÁS EFICIENTE
    best = df.loc[df['PUNTUACION'].idxmax()]
    print(f"\n🏆 REFERENCIA DE EDICIÓN (Mejor Video):")
    print(f"   🎬 Link: {best['URL']}")
    print(f"   ✂️ Ritmo: {best['CORTES_MIN']:.1f} cortes/min")
    print(f"   💡 Luz: {best['BRILLO']} | 🔊 Audio: {best['AUDIO_RMS']}")

except Exception as e:
    print(f"❌ Error: {e}")
    print("Consejo: Cierra el Excel antes de ejecutar esto.")

input("\nPresiona ENTER para salir...")