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

import downloader
import processor
import analyzer
import nlp
import datamanager
import scoring
import predictor
import consultor

st.set_page_config(page_title="TikTok Viral Analyzer SaaS", page_icon="📱", layout="wide")

# --- SISTEMA DE SESIÓN ---
if 'usuario_logueado' not in st.session_state:
    st.session_state['usuario_logueado'] = False
    st.session_state['tipo_plan'] = "Básico"

# --- DÍA 39: LA LANDING PAGE Y SELECCIÓN DE PLANES ---
if not st.session_state['usuario_logueado']:
    st.title("🚀 Bienvenido a TikTok Viral Analyzer")
    st.markdown("La herramienta definitiva para descifrar el algoritmo. Selecciona un plan para comenzar:")
    
    st.write("") # Espaciador
    
    # Creamos dos columnas para las tarjetas de precios
    col_basico, col_pro = st.columns(2)
    
    with col_basico:
        st.info("### 🟢 Plan Básico\nIdeal para empezar y explorar patrones.\n\n* Acceso a datos históricos (> 24h)\n* Simulador de viralidad base\n* Gráficos de tendencias generales")
        st.write("") 
        if st.button("Entrar Gratis", use_container_width=True):
            st.session_state['usuario_logueado'] = True
            st.session_state['tipo_plan'] = "Básico"
            st.rerun()
            
    with col_pro:
        st.success("### 👑 Plan PRO\nPara creadores serios y agencias.\n\n* Datos frescos en Tiempo Real (< 24h)\n* Benchmarking y métricas de competidores\n* Generador de guiones con IA")
        password = st.text_input("Introduce tu clave VIP:", type="password", placeholder="Escribe VIP2026 para desbloquear")
        if st.button("Desbloquear PRO", use_container_width=True, type="primary"):
            if password == "VIP2026":
                st.session_state['usuario_logueado'] = True
                st.session_state['tipo_plan'] = "PRO"
                st.rerun()
            else:
                st.error("Contraseña incorrecta. Vuelve a intentarlo.")

else:
    # --- DASHBOARD PRINCIPAL ---
    col_header, col_salir = st.columns([5, 1])
    with col_header:
        st.title("📱 Analizador de Viralidad TikTok (v3.0 SaaS)")
    with col_salir:
        st.markdown(f"**👑 Plan: {st.session_state['tipo_plan']}**")
        if st.button("Cerrar Sesión"):
            st.session_state['usuario_logueado'] = False
            st.rerun()

    st.markdown("Bienvenido al centro de mando. Aquí evaluamos el ADN técnico de los videos cortos y extraemos patrones de éxito.")

    # --- SIDEBAR: SIMULADOR CON INTELIGENCIA DE NICHO ---
    st.sidebar.header("🔮 Simulador de Viralidad")

    # Selección de nicho para comparar
    if os.path.exists(config.ARCHIVO_DB):
        conn = sqlite3.connect(config.ARCHIVO_DB)
        df_nichos = pd.read_sql_query("SELECT DISTINCT nicho FROM videos WHERE nicho != 'Desconocido'", conn)
        conn.close()
        nicho_sim = st.sidebar.selectbox("🎯 Nicho de referencia:", df_nichos['nicho'].tolist() if not df_nichos.empty else ["General"])
    else:
        nicho_sim = "General"

    sim_wpm = st.sidebar.slider("🗣️ Ritmo (WPM)", 50, 250, 150)
    sim_cpm = st.sidebar.slider("🎬 Cortes por Minuto", 0, 40, 12)
    sim_caras = st.sidebar.slider("👤 % Presencia Humana", 0, 100, 50)
    sim_brillo = st.sidebar.slider("☀️ Brillo Promedio", 0, 255, 120)
    sim_rms = st.sidebar.slider("🔊 Volumen (RMS)", 0.0, 1.0, 0.1, step=0.05)

    if st.session_state['tipo_plan'] == "PRO" and os.path.exists(config.ARCHIVO_DB):
        metricas_top = consultor.obtener_metricas_exito(nicho_sim)
        if metricas_top:
            st.sidebar.markdown("---")
            st.sidebar.subheader("⚖️ Comparativa PRO")
            
            dif_wpm = sim_wpm - metricas_top['wpm_ideal']
            st.sidebar.metric("Diferencia de Ritmo", f"{sim_wpm} WPM", f"{dif_wpm:.1f} vs Ideal", delta_color="normal")
            
            dif_cpm = sim_cpm - metricas_top['cpm_ideal']
            st.sidebar.metric("Diferencia de Edición", f"{sim_cpm} CPM", f"{dif_cpm:.1f} vs Ideal", delta_color="normal")
            
            if abs(dif_wpm) > 30 or abs(dif_cpm) > 5:
                st.sidebar.warning("⚠️ Tus ajustes se alejan del patrón viral de este nicho.")
            else:
                st.sidebar.success("✅ Estás en la 'Zona Viral' de este nicho.")

    st.sidebar.markdown("---")

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

    # --- SECCIÓN PRINCIPAL: LECTURA SEGURA DE LA BD ---
    if not os.path.exists(config.ARCHIVO_DB):
        st.info("La base de datos se creará en cuanto analices tu primer video desde tu terminal con main.py.")
    else:
        try:
            conn = sqlite3.connect(config.ARCHIVO_DB)
            df = pd.read_sql_query("SELECT * FROM videos", conn)
            conn.close()

            if not df.empty:
                st.subheader("📊 Panel de Control SaaS")
                df['fecha_proceso'] = pd.to_datetime(df['fecha_proceso'])
                ahora = pd.Timestamp.now()

                if st.session_state['tipo_plan'] == "PRO":
                    st.success("✅ Acceso PRO activado. Viendo tendencias frescas de las últimas 24 horas.")
                    limite_24h = ahora - pd.Timedelta(hours=24)
                    df = df[df['fecha_proceso'] >= limite_24h]
                else:
                    st.info("ℹ️ Plan Básico. Viendo patrones históricos (sin datos de las últimas 24h).")
                    limite_24h = ahora - pd.Timedelta(hours=24)
                    df = df[df['fecha_proceso'] < limite_24h]

                st.divider()

                if df.empty:
                    st.warning("No hay videos en este rango de tiempo para tu plan.")
                else:
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
                                              title="Ritmo vs Engagement")
                            st.plotly_chart(fig1, use_container_width=True)
                        with col_graf2:
                            fig2 = px.scatter(df, x="cortes_min", y="vistas", color="nicho" if 'nicho' in df.columns else "autor",
                                              hover_name="autor", hover_data=["wpm", "gancho"],
                                              title="Dinamismo de Edición vs Vistas", log_y=True)
                            st.plotly_chart(fig2, use_container_width=True)

                    with tab_ia:
                        st.header("🧠 Asesor Estratégico de Contenido")
                        
                        if 'nicho' in df.columns:
                            nichos_disponibles = df[df['nicho'] != 'Desconocido']['nicho'].dropna().unique().tolist()
                            
                            if nichos_disponibles:
                                nicho_elegido = st.selectbox("🎯 Elige el Nicho a auditar:", nichos_disponibles)
                                
                                col_btn1, col_btn2 = st.columns(2)
                                with col_btn1:
                                    if st.button("Generar Informe Top 5", type="primary", use_container_width=True):
                                        with st.spinner("Analizando métricas..."):
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
            st.error(f"Error crítico al leer los datos: {e}")