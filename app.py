"""
SMS Spam Detector - Main Application
Connects ML model, backend logic, and frontend UI
"""
import streamlit as st
from model import load_data, preprocess_data, train_models
from frontend import (
    set_page_config, apply_custom_css, render_sidebar, render_hero,
    render_tab_eda, render_tab_pipeline, render_tab_predict, render_tab_metrics,
    render_tab_experiments
)

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
set_page_config()
apply_custom_css()

# ─── LOAD AND TRAIN ─────────────────────────────────────────────────────────
with st.spinner("⚙️  Loading dataset and training models..."):
    raw_df = load_data()
    df = preprocess_data(raw_df)
    trained_models, results, X_test_global, y_test_global = train_models(df)

st.success(f"✅  Dataset loaded · {len(df):,} messages · {df['label'].value_counts()['spam']:,} spam · Models trained")

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
render_sidebar(df, list(trained_models.keys()))

# ─── MAIN CONTENT ────────────────────────────────────────────────────────────
render_hero()

# ─── TABS ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍  EDA", "⚙️  Pipeline", "🎯  Predict", "📊  Metrics", "🧪  Experiments"])

with tab1:
    render_tab_eda(df)

with tab2:
    render_tab_pipeline(df)

with tab3:
    render_tab_predict(trained_models)

with tab4:
    render_tab_metrics(results)

with tab5:
    render_tab_experiments(df)
