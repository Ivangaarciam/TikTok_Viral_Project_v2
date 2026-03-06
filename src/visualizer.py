# src/visualizer.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import config

def generar_graficos():
    print("\n📈 --- GENERADOR DE GRÁFICOS TIKTOK --- 📈\n")
    
    if not os.path.exists(config.ARCHIVO_DB):
        print("❌ No hay base de datos para analizar.")
        return

    # 1. Extraer Datos
    conn = sqlite3.connect(config.ARCHIVO_DB)
    df = pd.read_sql_query("SELECT * FROM videos", conn)
    conn.close()
    
    if len(df) < 3:
        print("⚠️ Necesitas al menos 3 videos en la base de datos para ver gráficos interesantes.")
        print(f"Actualmente tienes {len(df)}.")
        return

    print("⏳ Calculando métricas avanzadas y dibujando...")

    # 2. Feature Engineering (Crear nuevas variables)
    # Calculamos el Engagement Rate: (Likes + Guardados + Comentarios + Shares) / Vistas * 100
    df['interacciones'] = df['likes'] + df['guardados'] + df['comentarios'] + df['shares']
    # Evitamos dividir por cero
    df['engagement_rate'] = df.apply(lambda row: (row['interacciones'] / row['vistas'] * 100) if row['vistas'] > 0 else 0, axis=1)

    # 3. Configurar el estilo visual (Modo oscuro y profesional)
    plt.style.use('dark_background')
    sns.set_palette("pastel")
    
    # Creamos una figura grande con 2 gráficos (1 fila, 2 columnas)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Análisis de Viralidad: Ritmo vs Interacción', fontsize=16, fontweight='bold')

    # --- GRÁFICO 1: Ritmo de Habla (WPM) vs Engagement ---
    sns.regplot(
        data=df, 
        x='wpm', 
        y='engagement_rate', 
        ax=axes[0],
        scatter_kws={'s': 100, 'alpha': 0.7}, # Tamaño y transparencia de los puntos
        line_kws={'color': 'red'}             # Línea de tendencia
    )
    axes[0].set_title('¿Hablar más rápido genera más engagement?')
    axes[0].set_xlabel('Ritmo (Palabras por Minuto)')
    axes[0].set_ylabel('Engagement Rate (%)')

    # --- GRÁFICO 2: Cortes por Minuto (CPM) vs Vistas ---
    # Usamos escala logarítmica en Vistas porque la diferencia entre videos puede ser enorme
    sns.scatterplot(
        data=df, 
        x='cortes_min', 
        y='vistas', 
        size='pct_caras', # El tamaño del punto depende de cuánto sale la cara
        sizes=(20, 300),
        ax=axes[1],
        alpha=0.8
    )
    axes[1].set_yscale('log') # Eje Y en logaritmo para ver mejor videos pequeños vs gigantes
    axes[1].set_title('Cortes de Edición vs Vistas Totales')
    axes[1].set_xlabel('Cortes por Minuto (CPM)')
    axes[1].set_ylabel('Vistas (Escala Logarítmica)')

    # Ajustar el diseño para que no se superpongan los textos
    plt.tight_layout()
    
    # Guardar la imagen en la carpeta data
    ruta_imagen = os.path.join(config.DATA_DIR, "reporte_viralidad.png")
    plt.savefig(ruta_imagen, dpi=300)
    print(f"✅ Gráfico guardado en: {ruta_imagen}")
    
    # Mostrar el gráfico en pantalla
    plt.show()

if __name__ == "__main__":
    generar_graficos()