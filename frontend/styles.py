"""
Styling and Page Configuration
"""
import streamlit as st


def set_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="SMS Spam Detector",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_custom_css():
    """Apply custom CSS styling."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Sora:wght@300;400;600;700;800&display=swap');

    :root {
        --bg: #0a0e1a;
        --surface: #111827;
        --surface2: #1a2236;
        --accent: #00f5a0;
        --accent2: #00d9f5;
        --danger: #ff4d6d;
        --warn: #ffd166;
        --text: #e2e8f0;
        --muted: #a0aec0;
        --border: #1e293b;
    }

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }

    .stApp { background-color: var(--bg) !important; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1321 0%, #111827 100%) !important;
        border-right: 1px solid var(--border);
    }

    .stTabs [data-baseweb="tab-list"] {
        background: var(--surface) !important;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
        color: #0a0e1a !important;
    }

    .metric-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        transition: transform 0.2s, border-color 0.2s;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent), var(--accent2));
    }
    .metric-card:hover { transform: translateY(-4px); border-color: var(--accent); }
    .metric-value { font-size: 2.2rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
    .metric-label { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); margin-top: 4px; }

    .hero-banner {
        background: linear-gradient(135deg, #0d1321 0%, #111827 50%, #0d1f2d 100%);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 32px 40px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::after {
        content: '🛡️';
        position: absolute;
        right: 40px; top: 50%;
        transform: translateY(-50%);
        font-size: 5rem;
        opacity: 0.15;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--accent), var(--accent2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 8px 0;
        font-family: 'Sora', sans-serif;
    }
    .hero-sub { color: var(--muted); font-size: 1rem; font-weight: 400; }

    .pred-spam {
        background: linear-gradient(135deg, rgba(255,77,109,0.15), rgba(255,77,109,0.05));
        border: 2px solid var(--danger);
        border-radius: 16px;
        padding: 28px;
        text-align: center;
    }
    .pred-ham {
        background: linear-gradient(135deg, rgba(0,245,160,0.15), rgba(0,245,160,0.05));
        border: 2px solid var(--accent);
        border-radius: 16px;
        padding: 28px;
        text-align: center;
    }
    .pred-label { font-size: 2.5rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
    .pred-conf { font-size: 1rem; color: var(--muted); margin-top: 6px; }

    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--accent2);
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin: 24px 0 16px 0;
        font-family: 'JetBrains Mono', monospace;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-header::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    .info-pill {
        display: inline-block;
        background: rgba(0,217,245,0.1);
        border: 1px solid rgba(0,217,245,0.3);
        color: var(--accent2);
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }

    .stTextArea textarea {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(0,245,160,0.15) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
        color: #0a0e1a !important;
        font-weight: 700 !important;
        font-family: 'Sora', sans-serif !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 28px !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em;
        transition: opacity 0.2s, transform 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.9 !important; transform: translateY(-2px) !important; }

    .stSelectbox > div > div {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
    }

    .stDataFrame { border-radius: 12px; overflow: hidden; }
    .js-plotly-plot .plotly { border-radius: 12px; }
    .stAlert { border-radius: 12px !important; }

    [data-testid="stSidebar"] .stRadio label { color: var(--text) !important; }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    }

    #MainMenu, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)
