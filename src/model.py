# src/model.py
import sqlite3
import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import config

def entrenar_oraculo():
    print("\n🧠 --- ENTRENANDO AL ORÁCULO 2.0 --- 🧠\n")
    
    if not os.path.exists(config.ARCHIVO_DB):
        print("❌ No se encontró la base de datos.")
        return None

    conn = sqlite3.connect(config.ARCHIVO_DB)
    try:
        df = pd.read_sql_query("SELECT * FROM videos_limpios", conn)
    except sqlite3.OperationalError:
        print("❌ Error: Ejecuta etl.py primero para crear los datos limpios.")
        conn.close()
        return None
    conn.close()

    # CORRECCIÓN: Usamos 'cortes_min' en lugar de 'cpm'
    columnas_x = ['wpm', 'cortes_min', 'pct_caras', 'brillo', 'rms_audio']
    X = df[columnas_x]
    y = df['es_viral']

    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    except ValueError:
        print("❌ Error: La IA necesita más ejemplos. Asegúrate de tener videos con más de 100k vistas (virales) y menos de 100k (no virales) en tu BD.")
        return None

    print("⏳ La IA está estudiando los patrones...")
    modelo = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
    modelo.fit(X_train, y_train)

    predicciones = modelo.predict(X_test)
    precision = accuracy_score(y_test, predicciones) * 100

    print(f"✅ ENTRENAMIENTO COMPLETADO")
    print(f"🎯 Precisión del modelo: {precision:.1f}%")

    # NUEVO: Guardar el modelo en disco
    ruta_modelo = os.path.join(config.DATA_DIR, "oraculo.pkl")
    joblib.dump(modelo, ruta_modelo)
    print(f"💾 Cerebro de la IA guardado en: {ruta_modelo}")

    return modelo

if __name__ == "__main__":
    entrenar_oraculo()