# src/app.py
import streamlit as st
import sqlite3
import pandas as pd
import os
import joblib
import plotly.express as px
from datetime import datetime
from zoneinfo import ZoneInfo
import config

# --- NUESTRO ESCUADRÓN BACKEND ---
import downloader
import processor
import analyzer
import nlp
import datamanager
import scoring
import predictor
import consultor  # <--- NUEVO INTEGRANTE (DÍA 34)

st.set_page_config(page_title="TikTok Viral Analyzer SaaS", page_icon="📱", layout="wide")
st.title("📱 Analizador de Viralidad TikTok (v3.0 SaaS)")
st.markdown("Bienvenido al centro de mando. Aquí evaluamos el ADN técnico de los videos cortos y extraemos patrones de éxito.")

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
        if len(modelo.classes_) < 2:
            st.sidebar.warning("⚠️ Necesito entrenar con más videos variados (éxitos y fracasos) para poder predecir.")
        else:
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
        st.sidebar.error("⚠️ Falta el cerebro. Entrena la IA primero.")

st.divider()

# --- SECCIÓN: ANALIZADOR EN VIVO (Mantenido por compatibilidad v2) ---
with st.expander("⚡ Analizador Manual en Vivo (Pegar URL individual)"):
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        url_input = st.text_input("URL del video de TikTok:", label_visibility="collapsed", placeholder="https://www.tiktok.com/@usuario/video/123456789")
    with col_btn:
        btn_analizar = st.button("Analizar Video", type="primary", use_container_width=True)

    if btn_analizar and url_input:
        st.warning("Para minería masiva y categorización por nicho, utiliza el archivo main.py en tu terminal.")

st.divider()

# --- SECCIÓN PRINCIPAL: TABS DE DATOS, GRÁFICOS Y CONSULTOR IA ---
if not os.path.exists(config.ARCHIVO_DB):
    st.info("La base de datos se creará en cuanto analices tu primer video desde main.py")
else:
    try:
        conn = sqlite3.connect(config.ARCHIVO_DB)
        df = pd.read_sql_query("SELECT * FROM videos", conn)
        conn.close()

        df = pd.read_sql_query("SELECT * FROM videos", conn)
        conn.close()

        if not df.empty:
            st.subheader("📊 Panel de Control SaaS")
            
            # --- NUEVO: EL MURO DE PAGO (SaaS) ---
            # Convertimos la fecha de texto a formato fecha real para poder filtrar
            df['fecha_proceso'] = pd.to_datetime(df['fecha_proceso'])
            ahora = pd.Timestamp.now()

            col_plan1, col_plan2 = st.columns([1, 2])
            with col_plan1:
                st.markdown("### 💳 Tu Suscripción")
                plan = st.radio(
                    "Selecciona nivel de acceso:",
                    ["🟢 Plan Básico (Histórico)", "👑 Plan PRO (Últimas 24h)"],
                    label_visibility="collapsed"
                )
            
            with col_plan2:
                if "👑 Plan PRO" in plan:
                    st.success("✅ Acceso PRO activado. Viendo tendencias de las últimas 24 horas.")
                    # Filtramos los datos para mostrar SOLO los de las últimas 24h
                    limite_24h = ahora - pd.Timedelta(hours=24)
                    df = df[df['fecha_proceso'] >= limite_24h]
                else:
                    st.info("ℹ️ Plan Básico. Viendo patrones históricos (sin datos de las últimas 24h).")
                    # Filtramos para mostrar SOLO lo que es más antiguo de 24h
                    limite_24h = ahora - pd.Timedelta(hours=24)
                    df = df[df['fecha_proceso'] < limite_24h]

            st.divider()

            if df.empty:
                st.warning("No hay videos en este rango de tiempo. (Si elegiste Básico y acabas de crear la base de datos hoy, todos tus videos son 'PRO' porque tienen menos de 24h de antigüedad).")
            else:
                # --- MÉTRICAS GENERALES ---
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Videos Analizados", len(df))
                col2.metric("Ritmo Promedio", f"{df['wpm'].mean():.0f} WPM")
                col3.metric("Edición", f"{df['cortes_min'].mean():.1f} Cortes/min")
                col4.metric("Presencia", f"{df['pct_caras'].mean():.1f}%")

                if 'interacciones' not in df.columns:
                    df['interacciones'] = df['likes'] + df['guardados'] + df['comentarios'] + df['shares']
                df['engagement_rate'] = (df['interacciones'] / df['vistas'] * 100).fillna(0)

                tab_datos, tab_graficos, tab_ia = st.tabs(["🗂️ Base de Datos", "📈 Análisis Visual", "🤖 Consultor AI"])

                with tab_datos:
                    columnas_mostrar = ['autor', 'nicho', 'fecha_proceso', 'vistas', 'likes', 'wpm', 'cortes_min', 'pct_caras', 'sentimiento', 'gancho']
                    columnas_reales = [c for c in columnas_mostrar if c in df.columns]
                    
                    df_mostrar = df[columnas_reales].copy()
                    df_mostrar = df_mostrar.sort_values(by='vistas', ascending=False)
                    st.dataframe(df_mostrar, use_container_width=True)

                with tab_graficos:
                    col_graf1, col_graf2 = st.columns(2)
                    with col_graf1:
                        fig1 = px.scatter(df, x="wpm", y="engagement_rate", size="vistas", color="nicho" if 'nicho' in df.columns else "pct_caras",
                                          hover_name="autor", hover_data=["cortes_min", "gancho"],
                                          title="Ritmo vs Engagement (Por Nicho)")
                        st.plotly_chart(fig1, use_container_width=True)
                    with col_graf2:
                        fig2 = px.scatter(df, x="cortes_min", y="vistas", color="nicho" if 'nicho' in df.columns else "autor",
                                          hover_name="autor", hover_data=["wpm", "gancho"],
                                          title="Dinamismo de Edición vs Vistas", log_y=True)
                        st.plotly_chart(fig2, use_container_width=True)

                with tab_ia:
                    st.header("🧠 Asesor Estratégico de Contenido")
                    st.write("Selecciona un nicho. La IA buscará patrones de éxito basados en tu nivel de suscripción.")
                    
                    if 'nicho' in df.columns:
                        nichos_disponibles = df[df['nicho'] != 'Desconocido']['nicho'].dropna().unique().tolist()
                        
                        if nichos_disponibles:
                            nicho_elegido = st.selectbox("🎯 Elige el Nicho a auditar:", nichos_disponibles)
                            
                            col_btn1, col_btn2 = st.columns(2)
                            with col_btn1:
                                if st.button("Generar Informe Top 5", type="primary", use_container_width=True):
                                    with st.spinner(f"Analizando métricas del nicho '{nicho_elegido}'..."):
                                        informe = consultor.obtener_mejores_consejos(nicho_elegido)
                                        with st.chat_message("assistant"):
                                            st.markdown(informe)
                                        
                            with col_btn2:
                                if st.button("🤖 Generar Prompt Optimizado", use_container_width=True):
                                    prompt_magico = consultor.generar_prompt_creador(nicho_elegido)
                                    st.success("Copia el texto de abajo y pégalo en ChatGPT:")
                                    st.code(prompt_magico, language="markdown")
                                        
                        else:
                            st.info("Aún no tienes videos con un nicho clasificado.")

    except Exception as e:
        st.error(f"Error al leer los datos: {e}")