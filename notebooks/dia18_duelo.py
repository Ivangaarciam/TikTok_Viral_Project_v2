import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

print("========================================")
print("⚔️  EL DUELO: TÚ vs LA REFERENCIA (Día 18)")
print("========================================")

ARCHIVO_CSV = "cerebro_tiktok.csv"

if not os.path.exists(ARCHIVO_CSV):
    print("❌ No hay datos. Ejecuta main.py.")
    sys.exit()

try:
    # Cargar datos
    df = pd.read_csv(ARCHIVO_CSV, sep=';', decimal=',', encoding='utf-8-sig', on_bad_lines='skip')
    
    # Necesitamos al menos 2 videos para comparar
    if len(df) < 2:
        print("⚠️ Necesitas analizar al menos 2 videos para hacer un duelo.")
        print("   1. Analiza TU video.")
        print("   2. Analiza el video VIRAL de la competencia.")
        sys.exit()

    # Cogemos los dos últimos videos
    # Asumimos: El PENÚLTIMO (-2) es el tuyo, el ÚLTIMO (-1) es la referencia viral
    # (O al revés, el script los identifica por las vistas)
    
    v1 = df.iloc[-2] # Penúltimo
    v2 = df.iloc[-1] # Último
    
    # Ordenamos: El que tenga MÁS vistas será el "Campeón" (Referencia)
    if v2['VISTAS'] > v1['VISTAS']:
        campeon = v2
        aspirante = v1
    else:
        campeon = v1
        aspirante = v2

    print(f"\n🥊 RINCÓN ROJO (Aspirante): {aspirante['AUTOR']}")
    print(f"   Vistas: {aspirante['VISTAS']}")
    print(f"   Link: {aspirante['URL']}")
    
    print(f"\n🥊 RINCÓN AZUL (Campeón Viral): {campeon['AUTOR']}")
    print(f"   Vistas: {campeon['VISTAS']}")
    print(f"   Link: {campeon['URL']}")
    
    print("\n----------------------------------------")
    print("📊 ANÁLISIS DE LA BRECHA (GAP ANALYSIS)")
    print("----------------------------------------")
    
    # 1. RITMO (Cortes/Min)
    diff_ritmo = campeon['CORTES_MIN'] - aspirante['CORTES_MIN']
    print(f"✂️ RITMO DE EDICIÓN:")
    print(f"   • Tú: {aspirante['CORTES_MIN']:.1f} cpm")
    print(f"   • Viral: {campeon['CORTES_MIN']:.1f} cpm")
    
    if diff_ritmo > 5:
        print(f"   ❌ Eres muy LENTO. El viral tiene +{diff_ritmo:.1f} cortes/min.")
    elif diff_ritmo < -5:
        print(f"   ⚠️ Eres muy RÁPIDO. El viral es más pausado ({diff_ritmo:.1f} cpm).")
    else:
        print("   ✅ ¡Ritmo perfecto! Estás igualando al viral.")

    # 2. BRILLO
    diff_brillo = campeon['BRILLO'] - aspirante['BRILLO']
    print(f"\n💡 ILUMINACIÓN:")
    print(f"   • Tú: {aspirante['BRILLO']:.0f}")
    print(f"   • Viral: {campeon['BRILLO']:.0f}")
    
    if abs(diff_brillo) > 40:
        if diff_brillo > 0:
            print("   ❌ Tu video es demasiado OSCURO comparado con el éxito.")
        else:
            print("   ⚠️ Tu video está muy QUEMADO (luz) comparado con el éxito.")
    else:
        print("   ✅ Iluminación correcta.")

    # 3. DURACIÓN
    diff_duracion = campeon['DURACION'] - aspirante['DURACION']
    print(f"\n⏱️ DURACIÓN:")
    print(f"   • Tú: {aspirante['DURACION']:.1f}s")
    print(f"   • Viral: {campeon['DURACION']:.1f}s")
    
    if abs(diff_duracion) > 15:
        print(f"   ⚠️ Diferencia notable. El formato viral dura {abs(diff_duracion):.1f}s {'más' if diff_duracion > 0 else 'menos'}.")

    # --- GRÁFICA COMPARATIVA ---
    print("\n🎨 Generando gráfica del duelo...")
    
    categorias = ['Ritmo (CPM)', 'Brillo (/10)', 'Duración (s)']
    valores_aspirante = [aspirante['CORTES_MIN'], aspirante['BRILLO']/10, aspirante['DURACION']]
    valores_campeon = [campeon['CORTES_MIN'], campeon['BRILLO']/10, campeon['DURACION']]
    
    x = range(len(categorias))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 6))
    rects1 = ax.bar([i - width/2 for i in x], valores_aspirante, width, label='Tú (Aspirante)', color='gray')
    rects2 = ax.bar([i + width/2 for i in x], valores_campeon, width, label='Viral (Campeón)', color='gold')
    
    ax.set_ylabel('Valor')
    ax.set_title('Comparativa Técnica: Tú vs Viral')
    ax.set_xticks(x)
    ax.set_xticklabels(categorias)
    ax.legend()
    
    plt.savefig('duelo_resultado.png')
    print("✅ Gráfica guardada: 'duelo_resultado.png'")
    
    print("\n💡 CONSEJO FINAL:")
    print(f"Para igualar al video viral, ajusta tu próximo guion para que tenga un ritmo de {campeon['CORTES_MIN']:.0f} cortes y dure {campeon['DURACION']:.0f} segundos.")

except Exception as e:
    print(f"❌ Error: {e}")

input("\nPresiona ENTER para salir...")