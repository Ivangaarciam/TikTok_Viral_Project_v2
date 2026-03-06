# src/benchmarking.py

def comparar_con_virales(datos_tecnicos, datos_audio):
    """
    Compara las métricas del video actual con los estándares virales
    de TikTok y genera feedback accionable.
    """
    print("\n⚔️ --- EL DUELO: TU VIDEO VS EL ALGORITMO --- ⚔️")
    
    # Estándares de retención de la industria (Aproximados para formato corto)
    estandar_wpm = 145    # Palabras por minuto (Ritmo rápido)
    estandar_cpm = 12     # Cortes por minuto (Dinamismo visual)
    estandar_caras = 40.0 # Porcentaje de tiempo con cara en pantalla (Conexión)

    tu_wpm = datos_audio.get('wpm', 0)
    tu_cpm = datos_tecnicos.get('cpm', 0)
    tu_caras = datos_tecnicos.get('pct_caras', 0)

    # 1. ANÁLISIS DE RITMO DE VOZ (WPM)
    if tu_wpm >= estandar_wpm:
        print(f"✅ RITMO DE VOZ: Excelente ({tu_wpm} WPM). Hablas rápido, ideal para evitar que hagan scroll.")
    elif tu_wpm > 0:
        print(f"❌ RITMO DE VOZ: Lento ({tu_wpm} WPM). Intenta acercarte a {estandar_wpm} WPM. Elimina los silencios al editar.")
    else:
        print(f"⚠️ RITMO DE VOZ: No detectado (¿Es solo música?).")

    # 2. ANÁLISIS DE EDICIÓN (Cortes por Minuto)
    if tu_cpm >= estandar_cpm:
        print(f"✅ EDICIÓN: Dinámica ({round(tu_cpm, 1)} cortes/min). Mantienes un buen nivel de estímulo visual.")
    else:
        print(f"❌ EDICIÓN: Estática ({round(tu_cpm, 1)} cortes/min). Añade más zoom, texto en pantalla o cambios de plano. Meta: {estandar_cpm}+")

    # 3. ANÁLISIS DE CONEXIÓN HUMANA (Rostros)
    if tu_caras >= estandar_caras:
        print(f"✅ CONEXIÓN HUMANA: Fuerte ({tu_caras}% del video). La cara retiene la atención y genera confianza.")
    else:
        print(f"⚠️ CONEXIÓN HUMANA: Baja ({tu_caras}%). Considera mostrar más tu rostro, los videos de 'solo voz en off' penalizan la retención.")
        
    print("==============================================\n")