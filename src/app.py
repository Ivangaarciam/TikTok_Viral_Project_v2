# src/app.py
import streamlit as st
import sqlite3
import pandas as pd
import os
import joblib
import plotly.express as px
import config

# --- NUESTRO ESCUADRÓN BACKEND ---
import downloader
import processor
import analyzer
import nlp
import datamanager
import scoring
import predictor

st.set_page_config(page_title="TikTok Viral Analyzer", page_icon="📱", layout="wide")
st.title("📱 Analizador de Viralidad TikTok")
st.markdown("Bienvenido al centro de mando. Aquí evaluamos el ADN técnico de los videos cortos.")

# --- SIDEBAR: SIMULADOR CON IA ---
st.sidebar.header("🔮 Simulador de Viralidad")
st.sidebar.markdown("Ajusta los parámetros para ver qué opina la IA **antes** de publicar.")

sim_wpm = st.sidebar.slider("🗣️ Ritmo (WPM)", 50, 250, 150)
sim_cpm = st.sidebar.slider("🎬 Cortes por Minuto", 0, 40, 12)
sim_caras = st.sidebar.slider("👤 % Presencia Humana", 0, 100, 50)
sim_brillo = st.sidebar.slider("☀️ Brillo Promedio", 0, 255, 120)
sim_rms = st.sidebar.slider("🔊 Volumen (RMS)", 0.0, 1.0, 0.1, step=0.05)

ruta_modelo = os.path.join(config.DATA_DIR, "oraculo.pkl")

if st.sidebar.button("Predecir Éxito", use_container_width=True):
    if os.path.exists(ruta_modelo):
        modelo = joblib.load(ruta_modelo)
        datos_sim = pd.DataFrame([{'wpm': sim_wpm, 'cortes_min': sim_cpm, 'pct_caras': sim_caras, 'brillo': sim_brillo, 'rms_audio': sim_rms}])
        prob_viral = modelo.predict_proba(datos_sim)[0][1] * 100
        
        st.sidebar.divider()
        if prob_viral > 70:
            st.sidebar.success(f"🚀 Probabilidad: {prob_viral:.1f}%\n\n¡Potencial Viral Altísimo!")
        elif prob_viral > 40:
            st.sidebar.warning(f"📈 Probabilidad: {prob_viral:.1f}%\n\nBuen video, depende del nicho.")
        else:
            st.sidebar.error(f"🧊 Probabilidad: {prob_viral:.1f}%\n\nEl algoritmo no lo empujará.")
    else:
        st.sidebar.error("⚠️ Falta el cerebro. Entrena la IA con model.py primero.")

st.divider()

# --- SECCIÓN: ANALIZADOR EN VIVO ---
st.subheader("⚡ Analizador en Vivo")
col_input, col_btn = st.columns([4, 1])
with col_input:
    url_input = st.text_input("URL del video de TikTok:", label_visibility="collapsed", placeholder="https://www.tiktok.com/@usuario/video/123456789")
with col_btn:
    btn_analizar = st.button("Analizar Video", type="primary", use_container_width=True)

if btn_analizar and url_input:
    with st.status("Iniciando cadena de montaje...", expanded=True) as status:
        st.write("⬇️ Descargando video y metadatos...")
        stats = downloader.descargar_video(url_input)
        if stats:
            st.write("⚙️ Separando audio y video...")
            if processor.convertir_medios():
                st.write("👂 Transcribiendo con Whisper AI...")
                datos_audio = processor.transcribir_audio()
                if datos_audio:
                    st.write("🧠 Extrayendo semántica y emociones...")
                    palabras_clave = nlp.extraer_palabras_clave(datos_audio['texto'])
                    sentimiento = nlp.analizar_sentimiento(datos_audio['texto'])
                    
                    st.write("👁️ Analizando visión por computadora...")
                    datos_tecnicos = analyzer.calcular_metricas(config.NOMBRE_VIDEO_FINAL, config.NOMBRE_AUDIO_FINAL)
                    
                    if datos_tecnicos:
                        st.write("💾 Guardando en el Cerebro (SQLite)...")
                        datamanager.guardar_datos(url_input, datos_tecnicos, datos_audio, palabras_clave, sentimiento, stats)
                        status.update(label="¡Análisis completado!", state="complete", expanded=False)
                        st.success("✅ Video procesado y añadido con éxito.")
                        
                        st.markdown("### 🎬 Resultado del Análisis")
                        col_vid, col_txt = st.columns([1, 2])
                        with col_vid:
                            if os.path.exists(config.NOMBRE_VIDEO_FINAL):
                                st.video(config.NOMBRE_VIDEO_FINAL)
                        with col_txt:
                            st.info(f"**🪝 Gancho detectado:** {datos_audio['gancho']}")
                            st.success(f"**🏷️ Palabras clave:** {palabras_clave}")
                            st.warning(f"**🎭 Tono del video:** {sentimiento}")
                            with st.expander("Ver transcripción completa de Whisper"):
                                st.write(datos_audio['texto'])
                                
                    else: status.update(label="Fallo en el análisis visual.", state="error")
                else: status.update(label="Fallo en la transcripción.", state="error")
            else: status.update(label="Fallo al procesar medios.", state="error")
        else: status.update(label="Fallo al descargar. Verifica la URL o las cookies.", state="error")

st.divider()

# --- SECCIÓN PRINCIPAL: TABS DE DATOS Y GRÁFICOS ---
if not os.path.exists(config.ARCHIVO_DB):
    st.info("La base de datos se creará en cuanto analices tu primer video.")
else:
    try:
        conn = sqlite3.connect(config.ARCHIVO_DB)
        df = pd.read_sql_query("SELECT * FROM videos", conn)
        conn.close()

        if not df.empty:
            st.subheader("📊 Resumen del Cerebro")
            
            # --- NUEVO: CHIVATO DE ACTUALIZACIÓN ---
            from datetime import datetime
            fecha_mod = datetime.fromtimestamp(os.path.getmtime(config.ARCHIVO_DB))
            st.caption(f"Última sincronización de datos: {fecha_mod.strftime('%d/%m/%Y %H:%M')}")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Videos Analizados", len(df))
            col2.metric("Ritmo Promedio", f"{df['wpm'].mean():.0f} WPM")
            col3.metric("Edición", f"{df['cortes_min'].mean():.1f} Cortes/min")
            col4.metric("Presencia", f"{df['pct_caras'].mean():.1f}%")

            if 'interacciones' not in df.columns:
                df['interacciones'] = df['likes'] + df['guardados'] + df['comentarios'] + df['shares']
            df['engagement_rate'] = (df['interacciones'] / df['vistas'] * 100).fillna(0)

            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Exportar Base de Datos a CSV",
                data=csv,
                file_name='cerebro_tiktok_export.csv',
                mime='text/csv',
            )

            st.write("") 
            
            tab_datos, tab_graficos = st.tabs(["🗂️ Base de Datos", "📈 Análisis Visual"])

            with tab_datos:
                columnas_mostrar = ['autor', 'vistas', 'likes', 'wpm', 'cortes_min', 'pct_caras', 'sentimiento', 'gancho']
                columnas_reales = [c for c in columnas_mostrar if c in df.columns]
                
                df_mostrar = df[columnas_reales].copy()
                df_mostrar = df_mostrar.sort_values(by='vistas', ascending=False)
                st.dataframe(df_mostrar, use_container_width=True)

            with tab_graficos:
                col_graf1, col_graf2 = st.columns(2)
                with col_graf1:
                    fig1 = px.scatter(df, x="wpm", y="engagement_rate", size="vistas", color="pct_caras",
                                      hover_name="autor", hover_data=["cortes_min", "gancho"],
                                      title="¿Hablar más rápido genera más engagement?")
                    st.plotly_chart(fig1, use_container_width=True)
                with col_graf2:
                    fig2 = px.scatter(df, x="cortes_min", y="vistas", color="autor",
                                      hover_name="autor", hover_data=["wpm", "gancho"],
                                      title="Dinamismo de Edición vs Vistas", log_y=True)
                    st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Error al leer los datos: {e}")