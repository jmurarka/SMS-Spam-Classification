"""
Common UI Components - Sidebar and Hero Banner
"""
import streamlit as st


def render_sidebar(df, models_list):
    """Render the sidebar."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 16px 0 24px 0;">
            <div style="font-size:3rem;">🛡️</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:1.1rem; font-weight:700;
                        background:linear-gradient(135deg,#00f5a0,#00d9f5);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                        background-clip:text;">SpamGuard</div>
            <div style="font-size:0.72rem; color:#cbd5e1; margin-top:4px;">SMS Classifier · ML Project</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**📦 Dataset**")
        st.markdown('<span class="info-pill">UCI SMS Spam Collection</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="info-pill">{len(df):,} messages</span>', unsafe_allow_html=True)
        st.markdown("")

        st.markdown("**🤖 Models**")
        for m in models_list:
            st.markdown(f"<div style='font-size:0.8rem; color:#e2e8f0; padding:2px 0;'>▸ {m}</div>", unsafe_allow_html=True)


def render_hero():
    """Render the hero banner."""
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">SMS Spam Detector</div>
        <div class="hero-sub">Multi-model NLP classifier · TF-IDF Pipeline · EDA + Metrics · Real-time Prediction</div>
    </div>
    """, unsafe_allow_html=True)
