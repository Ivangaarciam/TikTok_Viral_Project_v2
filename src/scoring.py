# src/scoring.py

def calcular_score_viral(datos_tecnicos, datos_audio, stats_sociales):
    """
    Calcula una puntuación de 0 a 100 basada en los factores que 
    correlacionan con la viralidad en formato vertical.
    """
    print("📊 Calculando Puntuación de ADN Viral...")
    score = 0
    
    # 1. Tasa de Interacción (Engagement Rate) - PESA UN 40%
    vistas = stats_sociales.get('vistas', 1)
    if vistas == 0: vistas = 1
    interacciones = stats_sociales['likes'] + stats_sociales['guardados'] + stats_sociales['comentarios'] + stats_sociales['shares']
    engagement_rate = (interacciones / vistas) * 100
    
    # Un ER mayor al 10% es excelente en TikTok
    puntos_engagement = min((engagement_rate / 10) * 40, 40)
    score += puntos_engagement

    # 2. Ritmo de Habla (WPM) - PESA UN 25%
    wpm = datos_audio.get('wpm', 0)
    # Lo ideal suele estar entre 150 y 180 palabras por minuto
    if 130 <= wpm <= 190:
        score += 25
    elif wpm > 190 or (100 <= wpm < 130):
        score += 15
    else:
        score += 5 # Habla muy lento o es solo música

    # 3. Retención Visual (Cortes por Minuto) - PESA UN 20%
    cpm = datos_tecnicos.get('cpm', 0)
    # Un buen ritmo de edición en TikTok son más de 12 cortes por minuto
    puntos_cpm = min((cpm / 15) * 20, 20)
    score += puntos_cpm

    # 4. Conexión Humana (% Caras en pantalla) - PESA UN 15%
    pct_caras = datos_tecnicos.get('pct_caras', 0)
    # Si hay una cara el 50% del tiempo, te llevas los puntos
    puntos_caras = min((pct_caras / 50) * 15, 15)
    score += puntos_caras

    score_final = round(score, 1)
    
    # Imprimir el veredicto
    print("\n" + "="*40)
    print(f"🧬 ADN VIRAL DEL VIDEO: {score_final}/100")
    if score_final >= 80:
        print("🔥 Rango: POTENCIAL ALTÍSIMO (Cumple todos los patrones)")
    elif score_final >= 60:
        print("📈 Rango: BUENO (Tiene tracción y buen ritmo)")
    elif score_final >= 40:
        print("🟡 Rango: REGULAR (Falla en retención o engagement)")
    else:
        print("🧊 Rango: BAJO (Lejos del estándar del algoritmo)")
    print("="*40 + "\n")

    return score_final