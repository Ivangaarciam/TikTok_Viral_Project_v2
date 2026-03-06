# src/predictor.py
import os
import joblib
import pandas as pd
import config

def predecir_viralidad(datos_tecnicos, datos_audio):
    ruta_modelo = os.path.join(config.DATA_DIR, "oraculo.pkl")
    
    if not os.path.exists(ruta_modelo):
        # Si el modelo no existe, salimos en silencio
        return None
        
    # 1. Despertar a la IA
    modelo = joblib.load(ruta_modelo)
    
    # 2. Empaquetar los datos del nuevo video igual que en el entrenamiento
    # Usamos los nombres que espera el modelo: 'wpm', 'cortes_min', etc.
    datos_prediccion = pd.DataFrame([{
        'wpm': datos_audio.get('wpm', 0),
        'cortes_min': datos_tecnicos.get('cpm', 0), # Viene como cpm del analyzer
        'pct_caras': datos_tecnicos.get('pct_caras', 0),
        'brillo': datos_tecnicos.get('brillo', 0),
        'rms_audio': datos_tecnicos.get('rms', 0)
    }])
    
    # 3. Preguntar a la IA la probabilidad (predict_proba devuelve % de 0 y de 1)
    probabilidades = modelo.predict_proba(datos_prediccion)[0]
    prob_viral = probabilidades[1] * 100 
    
    print("\n🔮 --- PREDICCIÓN DE LA IA (MACHINE LEARNING) --- 🔮")
    print(f"   Probabilidad matemática de viralidad: {prob_viral:.1f}%")
    
    if prob_viral > 70:
        print("   🚀 ¡Este video tiene el ADN exacto de tus videos virales!")
    elif prob_viral > 40:
        print("   📈 Tiene potencial, pero el nicho o el horario decidirán el resto.")
    else:
        print("   🧊 El algoritmo lo descartará pronto. Patrones técnicos pobres.")
    print("==================================================\n")
    
    return prob_viral