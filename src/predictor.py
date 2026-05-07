# src/predictor.py
import joblib
import pandas as pd
import os
import config

def predecir_viralidad(datos_tecnicos, datos_audio):
    ruta_modelo = os.path.join(config.DATA_DIR, "oraculo.pkl")
    
    if not os.path.exists(ruta_modelo):
        print("🔮 ORÁCULO: Aún no tengo un cerebro entrenado. Entrena el modelo primero.")
        return
        
    try:
        modelo = joblib.load(ruta_modelo)
        
        datos_sim = pd.DataFrame([{
            'wpm': datos_audio['wpm'],
            'cortes_min': datos_tecnicos['cpm'],
            'pct_caras': datos_tecnicos['pct_caras'],
            'brillo': datos_tecnicos['brillo'],
            'rms_audio': datos_tecnicos['rms']
        }])
        
        # --- EL FIX DE HOY: Evitar el Síndrome de Visión de Túnel ---
        if len(modelo.classes_) < 2:
            print("\n🔮 PREDICCIÓN DE IA: ⚠️ Necesito entrenar con más vídeos. Ahora mismo mi base de datos es demasiado pequeña o todos los vídeos tienen el mismo resultado para mí.")
            return

        # Si el modelo conoce ambas clases (0 y 1), predecimos normalmente
        probabilidades = modelo.predict_proba(datos_sim)[0]
        prob_viral = probabilidades[1] * 100
        
        print("\n🔮 PREDICCIÓN DE LA IA (ORÁCULO):")
        if prob_viral > 70:
            print(f"🚀 ¡POTENCIAL VIRAL ALTÍSIMO! ({prob_viral:.1f}%)")
        elif prob_viral > 40:
            print(f"📈 Buen video, depende mucho del nicho ({prob_viral:.1f}%)")
        else:
            print(f"🧊 El algoritmo probablemente no lo empuje ({prob_viral:.1f}%)")
            
    except Exception as e:
        print(f"⚠️ Error en el Oráculo: {e}")