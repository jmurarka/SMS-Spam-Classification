"""
Frontend UI Components and Styling
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics import roc_curve, roc_auc_score
from backend import get_message_stats, create_wordcloud, get_top_words


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
        --muted: #64748b;
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
        color: var(--muted) !important;
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
            <div style="font-size:0.72rem; color:#64748b; margin-top:4px;">SMS Classifier · ML Project</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**📦 Dataset**")
        st.markdown('<span class="info-pill">UCI SMS Spam Collection</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="info-pill">{len(df):,} messages</span>', unsafe_allow_html=True)
        st.markdown("")

        st.markdown("**🤖 Models**")
        for m in models_list:
            st.markdown(f"<div style='font-size:0.8rem; color:#94a3b8; padding:2px 0;'>▸ {m}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**📋 Project Rules**")
        st.markdown("""
        <div style="font-size:0.75rem; color:#64748b; line-height:1.7;">
        ✅ sklearn pipeline<br>
        ✅ No GitHub clones<br>
        ✅ UCI dataset<br>
        ✅ Built from scratch
        </div>
        """, unsafe_allow_html=True)


def render_hero():
    """Render the hero banner."""
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">SMS Spam Detector</div>
        <div class="hero-sub">Multi-model NLP classifier · TF-IDF Pipeline · EDA + Metrics · Real-time Prediction</div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 - EDA
# ═══════════════════════════════════════════════════════════════════════════════

def render_tab_eda(df):
    """Render EDA tab."""
    st.markdown('<div class="section-header">Dataset Overview</div>', unsafe_allow_html=True)

    spam_count = df['label'].value_counts()['spam']
    ham_count = df['label'].value_counts()['ham']
    total = len(df)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl, color in [
        (c1, total, "Total Messages", "#00d9f5"),
        (c2, ham_count, "Ham (Legit)", "#00f5a0"),
        (c3, spam_count, "Spam", "#ff4d6d"),
        (c4, f"{spam_count/total*100:.1f}%", "Spam Rate", "#ffd166"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:{color}">{val}</div>
            <div class="metric-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1: Distribution + Word count dist
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="section-header">Class Distribution</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=['Ham', 'Spam'],
            values=[ham_count, spam_count],
            hole=0.55,
            marker_colors=['#00f5a0', '#ff4d6d'],
            textfont_size=13,
            textfont_color='#0a0e1a'
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0', legend_font_size=13,
            margin=dict(t=20,b=20,l=20,r=20), height=260
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Character Length Distribution</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        for label, color, name in [('ham','#00f5a0','Ham'), ('spam','#ff4d6d','Spam')]:
            subset = df[df['label'] == label]['num_chars']
            fig2.add_trace(go.Histogram(
                x=subset, name=name, opacity=0.75,
                marker_color=color, nbinsx=50
            ))
        fig2.update_layout(
            barmode='overlay', paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,24,39,0.6)', font_color='#e2e8f0',
            xaxis=dict(title='Character Count', gridcolor='#1e293b'),
            yaxis=dict(title='Frequency', gridcolor='#1e293b'),
            legend=dict(bgcolor='rgba(0,0,0,0)'),
            margin=dict(t=20,b=40,l=40,r=20), height=260
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Feature comparison
    st.markdown('<div class="section-header">Feature Analysis by Class</div>', unsafe_allow_html=True)
    features = ['num_chars', 'num_words', 'num_digits', 'capitals_ratio']
    feat_labels = ['Characters', 'Words', 'Digits', 'Capitals Ratio']

    fig3 = make_subplots(rows=1, cols=4, subplot_titles=feat_labels)
    for i, (feat, lbl) in enumerate(zip(features, feat_labels), 1):
        for label, color, name in [('ham','#00f5a0','Ham'),('spam','#ff4d6d','Spam')]:
            fig3.add_trace(go.Box(
                y=df[df['label']==label][feat],
                name=name, marker_color=color,
                showlegend=(i==1), boxmean=True
            ), row=1, col=i)
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,24,39,0.6)',
        font_color='#e2e8f0', height=320,
        margin=dict(t=40,b=20), legend=dict(bgcolor='rgba(0,0,0,0)')
    )
    fig3.update_xaxes(showgrid=False)
    fig3.update_yaxes(gridcolor='#1e293b')
    st.plotly_chart(fig3, use_container_width=True)

    # Word Clouds
    st.markdown('<div class="section-header">Word Clouds</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ham Messages**")
        fig_wc = create_wordcloud(df[df['label']=='ham']['cleaned'].tolist(), 'Greens')
        st.pyplot(fig_wc)

    with col2:
        st.markdown("**Spam Messages**")
        fig_wc2 = create_wordcloud(df[df['label']=='spam']['cleaned'].tolist(), 'Reds')
        st.pyplot(fig_wc2)

    # Top words bar chart
    st.markdown('<div class="section-header">Top 15 Words: Ham vs Spam</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        ham_words = get_top_words(df[df['label']=='ham']['cleaned'])
        words, counts = zip(*ham_words)
        fig_bar = go.Figure(go.Bar(
            x=list(counts)[::-1], y=list(words)[::-1],
            orientation='h', marker_color='#00f5a0',
            marker_line_width=0
        ))
        fig_bar.update_layout(
            title="Top Ham Words", paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,24,39,0.6)', font_color='#e2e8f0',
            xaxis=dict(gridcolor='#1e293b'), yaxis=dict(gridcolor='#1e293b'),
            height=400, margin=dict(t=40,b=20,l=120,r=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        spam_words = get_top_words(df[df['label']=='spam']['cleaned'])
        words2, counts2 = zip(*spam_words)
        fig_bar2 = go.Figure(go.Bar(
            x=list(counts2)[::-1], y=list(words2)[::-1],
            orientation='h', marker_color='#ff4d6d',
            marker_line_width=0
        ))
        fig_bar2.update_layout(
            title="Top Spam Words", paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,24,39,0.6)', font_color='#e2e8f0',
            xaxis=dict(gridcolor='#1e293b'), yaxis=dict(gridcolor='#1e293b'),
            height=400, margin=dict(t=40,b=20,l=120,r=20)
        )
        st.plotly_chart(fig_bar2, use_container_width=True)

    # Raw samples
    st.markdown('<div class="section-header">Sample Messages</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Ham Samples**")
        st.dataframe(
            df[df['label']=='ham'][['message','num_chars','num_words']].head(5),
            use_container_width=True, hide_index=True
        )
    with col2:
        st.markdown("**Spam Samples**")
        st.dataframe(
            df[df['label']=='spam'][['message','num_chars','num_words']].head(5),
            use_container_width=True, hide_index=True
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 - PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def render_tab_pipeline(df):
    """Render Pipeline tab."""
    st.markdown('<div class="section-header">Preprocessing Pipeline Architecture</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#111827; border:1px solid #1e293b; border-radius:16px; padding:28px; font-family:'JetBrains Mono',monospace; font-size:0.82rem; line-height:2;">
    <span style="color:#64748b"># Step 1 — Text Cleaning</span><br>
    <span style="color:#00d9f5">lowercase</span> → <span style="color:#00d9f5">strip URLs</span> → <span style="color:#00d9f5">normalize digits</span> → <span style="color:#00d9f5">remove punctuation</span><br><br>
    <span style="color:#64748b"># Step 2 — Tokenization & Normalization</span><br>
    <span style="color:#00f5a0">split tokens</span> → <span style="color:#00f5a0">remove stopwords</span> → <span style="color:#00f5a0">Porter Stemming</span><br><br>
    <span style="color:#64748b"># Step 3 — Feature Extraction (sklearn Pipeline)</span><br>
    <span style="color:#ffd166">TfidfVectorizer</span>(<span style="color:#e2e8f0">max_features=8000, ngram_range=(1,2), sublinear_tf=True, min_df=2</span>)<br><br>
    <span style="color:#64748b"># Step 4 — Classifier</span><br>
    <span style="color:#ff4d6d">Model.fit(X_train, y_train)</span> → <span style="color:#ff4d6d">predict(X_test)</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Feature Engineering</div>', unsafe_allow_html=True)

    features_info = {
        "num_chars":       ("Character count of message",           "Spam tends to be longer"),
        "num_words":       ("Word count",                           "More words → more likely spam"),
        "num_digits":      ("Count of digit characters",            "Phone numbers / promo codes"),
        "num_upper":       ("Uppercase letter count",               "CAPS used for urgency in spam"),
        "capitals_ratio":  ("Ratio of uppercase to total chars",    "Normalized uppercase density"),
        "has_url":         ("Binary: contains URL",                 "Phishing links"),
        "has_phone":       ("Binary: contains long digit sequence", "Contact numbers in spam"),
        "has_currency":    ("Binary: £, $, free, win, prize",       "Promotional language"),
        "exclamations":    ("Count of ! characters",                "Excitement / urgency signals"),
        "num_sentences":   ("Estimated sentence count",             "Structural complexity"),
    }
    feat_df = pd.DataFrame(
        [(k, v[0], v[1]) for k,v in features_info.items()],
        columns=['Feature', 'Description', 'Spam Signal']
    )
    st.dataframe(feat_df, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-header">TF-IDF Parameters</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    params = [
        ("max_features", "8,000", "Vocabulary size limit"),
        ("ngram_range", "(1, 2)", "Unigrams + bigrams"),
        ("sublinear_tf", "True", "Log TF scaling"),
        ("min_df", "2", "Min document frequency"),
        ("strip_accents", "'unicode'", "Unicode normalization"),
        ("analyzer", "'word'", "Word-level tokenization"),
    ]
    for i, (param, val, desc) in enumerate(params):
        [col1, col2, col3][i % 3].markdown(f"""
        <div style="background:#111827; border:1px solid #1e293b; border-radius:12px; padding:16px; margin-bottom:12px;">
            <div style="color:#00d9f5; font-family:'JetBrains Mono',monospace; font-size:0.85rem; font-weight:600;">{param}</div>
            <div style="color:#00f5a0; font-family:'JetBrains Mono',monospace; font-size:1.1rem; font-weight:700; margin:4px 0;">{val}</div>
            <div style="color:#64748b; font-size:0.75rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Class Distribution After Split</div>', unsafe_allow_html=True)
    train_size = int(len(df) * 0.8)
    test_size = len(df) - train_size
    col1, col2, col3 = st.columns(3)
    for col, lbl, val, color in [
        (col1, "Train Set", f"{train_size:,}", "#00f5a0"),
        (col2, "Test Set", f"{test_size:,}", "#00d9f5"),
        (col3, "Split Ratio", "80 / 20", "#ffd166"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:{color}">{val}</div>
            <div class="metric-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 - PREDICT
# ═══════════════════════════════════════════════════════════════════════════════

def render_tab_predict(trained_models):
    """Render Prediction tab."""
    st.markdown('<div class="section-header">Real-time SMS Classification</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_area(
            "Enter an SMS message",
            placeholder="Type or paste an SMS message here...",
            height=120,
            label_visibility="collapsed"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        model_choice = st.selectbox("Model", list(trained_models.keys()), label_visibility="visible")

        st.markdown("<br>", unsafe_allow_html=True)

        examples = {
            "Spam — Prize": "Congratulations! You've won a FREE £500 prize. Call 07912345678 NOW to claim!",
            "Spam — Offer": "URGENT! Limited time offer. 50% OFF everything. Text WIN to 85000 today only!!!",
            "Ham — Friend": "Hey! Are you coming to dinner tonight? Let me know by 7pm.",
            "Ham — Work": "The project meeting has been moved to Thursday afternoon.",
        }
        selected_ex = st.selectbox("Try an example", ["— select —"] + list(examples.keys()))
        if selected_ex != "— select —":
            user_input = examples[selected_ex]

    if st.button("🔍  Classify Message"):
        if user_input.strip():
            from backend import predict_message
            
            model = trained_models[model_choice]
            result = predict_message(user_input, model)

            st.markdown("<br>", unsafe_allow_html=True)

            if result['prediction'] == 1:
                st.markdown(f"""
                <div class="pred-spam">
                    <div class="pred-label" style="color:#ff4d6d;">🚨 SPAM</div>
                    <div class="pred-conf">Spam confidence: {result['spam_prob']*100:.1f}%</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="pred-ham">
                    <div class="pred-label" style="color:#00f5a0;">✅ HAM</div>
                    <div class="pred-conf">Ham confidence: {result['ham_prob']*100:.1f}%</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Confidence gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['spam_prob'] * 100,
                title=dict(text="Spam Probability (%)", font=dict(color='#e2e8f0', size=14)),
                gauge=dict(
                    axis=dict(range=[0, 100], tickcolor='#64748b', tickfont=dict(color='#64748b')),
                    bar=dict(color='#ff4d6d' if result['prediction'] == 1 else '#00f5a0'),
                    bgcolor='#1a2236',
                    steps=[
                        dict(range=[0,40], color='rgba(0,245,160,0.1)'),
                        dict(range=[40,70], color='rgba(255,209,102,0.1)'),
                        dict(range=[70,100], color='rgba(255,77,109,0.1)'),
                    ],
                    threshold=dict(line=dict(color='#ffd166', width=2), value=50)
                ),
                number=dict(font=dict(color='#e2e8f0', size=32), suffix='%')
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', font_color='#e2e8f0',
                height=220, margin=dict(t=20, b=20, l=30, r=30)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Message stats
            st.markdown('<div class="section-header">Message Statistics</div>', unsafe_allow_html=True)
            mc1, mc2, mc3, mc4 = st.columns(4)
            stats = [
                (len(user_input), "Characters", "#00d9f5"),
                (len(user_input.split()), "Words", "#00f5a0"),
                (sum(c.isupper() for c in user_input), "Uppercase", "#ffd166"),
                (user_input.count('!'), "Exclamations", "#ff4d6d"),
            ]
            for col, (val, lbl, color) in zip([mc1,mc2,mc3,mc4], stats):
                col.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color:{color};font-size:1.8rem">{val}</div>
                    <div class="metric-label">{lbl}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.warning("Please enter a message to classify.")

    # Batch prediction
    st.markdown('<div class="section-header">Batch Prediction</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload a CSV with a 'message' column", type=['csv'])
    if uploaded:
        from backend import batch_predict
        batch_df = pd.read_csv(uploaded)
        model = trained_models[model_choice]
        result_df, error = batch_predict(batch_df, model)
        if error:
            st.error(error)
        else:
            st.dataframe(result_df[['message','label'] + (['spam_prob'] if 'spam_prob' in result_df.columns else [])],
                        use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 - METRICS
# ═══════════════════════════════════════════════════════════════════════════════

def render_tab_metrics(results):
    """Render Metrics tab."""
    st.markdown('<div class="section-header">Model Performance Comparison</div>', unsafe_allow_html=True)

    # Summary table
    summary_data = []
    for name, res in results.items():
        summary_data.append({
            'Model': name,
            'Accuracy': f"{res['accuracy']*100:.2f}%",
            'Precision': f"{res['precision']*100:.2f}%",
            'Recall': f"{res['recall']*100:.2f}%",
            'F1 Score': f"{res['f1']*100:.2f}%",
        })
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    # Bar chart comparison
    st.markdown('<div class="section-header">Metric Comparison</div>', unsafe_allow_html=True)
    metric_names = ['accuracy','precision','recall','f1']
    metric_labels = ['Accuracy','Precision','Recall','F1']
    colors = ['#00f5a0','#00d9f5','#ffd166','#ff4d6d']

    fig_comp = go.Figure()
    for metric, label, color in zip(metric_names, metric_labels, colors):
        fig_comp.add_trace(go.Bar(
            name=label,
            x=list(results.keys()),
            y=[results[m][metric] for m in results],
            marker_color=color, marker_line_width=0,
            text=[f"{results[m][metric]*100:.1f}%" for m in results],
            textposition='outside', textfont=dict(color='#e2e8f0', size=10)
        ))
    fig_comp.update_layout(
        barmode='group', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(17,24,39,0.6)', font_color='#e2e8f0',
        xaxis=dict(gridcolor='#1e293b'), yaxis=dict(gridcolor='#1e293b', range=[0,1.15]),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(t=20,b=20), height=380
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # Detailed model view
    st.markdown('<div class="section-header">Detailed Analysis Per Model</div>', unsafe_allow_html=True)
    selected_model = st.selectbox("Select model to inspect", list(results.keys()), key="metrics_model")
    res = results[selected_model]

    col1, col2 = st.columns(2)

    # Confusion Matrix
    with col1:
        st.markdown("**Confusion Matrix**")
        cm = res['cm']
        labels = ['Ham', 'Spam']
        fig_cm = go.Figure(go.Heatmap(
            z=cm, x=labels, y=labels,
            colorscale=[[0,'#111827'],[0.5,'#1a3a2a'],[1,'#00f5a0']],
            text=cm, texttemplate='<b>%{text}</b>',
            textfont=dict(size=20, color='#e2e8f0'),
            showscale=False
        ))
        fig_cm.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,24,39,0.6)',
            font_color='#e2e8f0', height=300,
            xaxis=dict(title='Predicted', side='bottom'),
            yaxis=dict(title='Actual'),
            margin=dict(t=20,b=60,l=60,r=20)
        )
        st.plotly_chart(fig_cm, use_container_width=True)

    # ROC Curve
    with col2:
        st.markdown("**ROC / PR Curve**")
        if res['y_prob'] is not None:
            fpr, tpr, _ = roc_curve(res['y_test'], res['y_prob'])
            auc_val = roc_auc_score(res['y_test'], res['y_prob'])
            fig_roc = go.Figure()
            fig_roc.add_trace(go.Scatter(
                x=[0,1], y=[0,1], mode='lines',
                line=dict(color='#64748b', dash='dash'), showlegend=False
            ))
            fig_roc.add_trace(go.Scatter(
                x=fpr, y=tpr, mode='lines', name=f'AUC = {auc_val:.4f}',
                line=dict(color='#00f5a0', width=2),
                fill='tozeroy', fillcolor='rgba(0,245,160,0.07)'
            ))
            fig_roc.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,24,39,0.6)',
                font_color='#e2e8f0', height=300,
                xaxis=dict(title='False Positive Rate', gridcolor='#1e293b'),
                yaxis=dict(title='True Positive Rate', gridcolor='#1e293b'),
                legend=dict(bgcolor='rgba(0,0,0,0)'),
                margin=dict(t=20,b=60,l=60,r=20)
            )
            st.plotly_chart(fig_roc, use_container_width=True)
        else:
            st.info("Probability scores not available for this model. All Naive Bayes variants support ROC curves.")

    # Classification report
    st.markdown("**Classification Report**")
    st.code(res['report'], language='text')

    # Per-model metrics cards
    mc1, mc2, mc3, mc4 = st.columns(4)
    for col, key, lbl, color in [
        (mc1,'accuracy','Accuracy','#00f5a0'),
        (mc2,'precision','Precision','#00d9f5'),
        (mc3,'recall','Recall','#ffd166'),
        (mc4,'f1','F1 Score','#ff4d6d'),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:{color}">{res[key]*100:.2f}%</div>
            <div class="metric-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 - EXPERIMENTS
# ═══════════════════════════════════════════════════════════════════════════════

def render_tab_experiments(df):
    """Render Comprehensive Experiments tab."""
    st.markdown('<div class="section-header">Comprehensive Experiments Framework</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This section runs systematic experiments comparing different:
    - **Models**: Multinomial NB, Bernoulli NB, Complement NB
    - **Vectorizers**: CountVectorizer, TF-IDF
    - **Preprocessing**: With/without stopwords, with/without stemming
    - **Hyperparameters**: max_features, ngram_range, alpha smoothing
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">Main Experiments</div>', unsafe_allow_html=True)
        st.markdown("""
        **Experiment 1 — Multinomial NB + CountVectorizer + Basic**
        - Model: Multinomial Naive Bayes
        - Vectorizer: CountVectorizer (max_features=3000)
        - Preprocessing: No stopword removal, no stemming
        
        **Experiment 2 — Bernoulli NB + Binary BoW + Stopword Removal**
        - Model: Bernoulli Naive Bayes
        - Vectorizer: Binary CountVectorizer
        - Preprocessing: With stopword removal
        
        **Experiment 3 — Complement NB + TF-IDF + Stemming**
        - Model: Complement Naive Bayes
        - Vectorizer: TF-IDF Vectorizer
        - Preprocessing: With stemming
        """)
    
    with col2:
        st.markdown('<div class="section-header">Hyperparameter Tweaks</div>', unsafe_allow_html=True)
        st.markdown("""
        **Vectorizer Tweaks:**
        - max_features: 500, 3000, 5000
        - ngram_range: unigrams (1,1) vs bigrams (1,2)
        
        **Model Tweaks:**
        - alpha (smoothing): 0.1, 0.5, 1.0
        
        **Preprocessing Tweaks:**
        - Stopword removal: with vs without
        - Stemming: with vs without
        """)
    
    st.markdown("")
    
    # Run experiments button
    if st.button("🚀 Run All Experiments", use_container_width=True):
        st.info("⏱️ Running experiments... This may take several minutes.")
        
        try:
            from model import run_all_experiments, create_comparison_table, generate_report
            
            with st.spinner("Running experiments..."):
                # Run all experiments
                all_results = run_all_experiments(df)
            
            st.success("✅ Experiments completed!")
            
            # ===== RESULTS DISPLAY =====
            st.markdown('<div class="section-header">Experiment Results</div>', unsafe_allow_html=True)
            
            # Comparison table
            st.markdown("**Comparison Table**")
            comparison_df = create_comparison_table(all_results)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            
            # Download comparison as CSV
            csv_data = comparison_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv_data,
                file_name="experiment_results.csv",
                mime="text/csv"
            )
            
            st.markdown("")
            
            # Main experiments details
            st.markdown('<div class="section-header">Main Experiments - Detailed Results</div>', unsafe_allow_html=True)
            
            exp_tabs = st.tabs([
                "Experiment 1",
                "Experiment 2", 
                "Experiment 3"
            ])
            
            exp_keys = [
                'Exp1_MultinomialNB_CountVect_Basic',
                'Exp2_BernoulliNB_BinaryBoW_Stopword',
                'Exp3_ComplementNB_TFIDF_Stemming'
            ]
            
            for tab, exp_key in zip(exp_tabs, exp_keys):
                with tab:
                    result = all_results['main_experiments'][exp_key]
                    
                    # Metrics
                    mc1, mc2, mc3, mc4 = st.columns(4)
                    for col, key, lbl, color in [
                        (mc1,'accuracy','Accuracy','#00f5a0'),
                        (mc2,'precision','Precision','#00d9f5'),
                        (mc3,'recall','Recall','#ffd166'),
                        (mc4,'f1','F1 Score','#ff4d6d'),
                    ]:
                        col.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value" style="color:{color}">{result[key]*100:.2f}%</div>
                            <div class="metric-label">{lbl}</div>
                        </div>""", unsafe_allow_html=True)
                    
                    st.markdown("")
                    
                    # Confusion Matrix
                    st.markdown("**Confusion Matrix**")
                    cm = result['confusion_matrix']
                    labels = ['Ham', 'Spam']
                    fig_cm = go.Figure(go.Heatmap(
                        z=cm, x=labels, y=labels,
                        colorscale=[[0,'#111827'],[0.5,'#1a3a2a'],[1,'#00f5a0']],
                        text=cm, texttemplate='<b>%{text}</b>',
                        textfont=dict(size=20, color='#e2e8f0'),
                        showscale=False
                    ))
                    fig_cm.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,24,39,0.6)',
                        font_color='#e2e8f0', height=300,
                        xaxis=dict(title='Predicted', side='bottom'),
                        yaxis=dict(title='Actual'),
                        margin=dict(t=20,b=60,l=60,r=20)
                    )
                    st.plotly_chart(fig_cm, use_container_width=True)
            
            # Tweaks analysis
            st.markdown('<div class="section-header">Hyperparameter Tweaks Analysis</div>', unsafe_allow_html=True)
            
            tweak_tabs = st.tabs([
                "Max Features",
                "NGram Range",
                "Alpha (Smoothing)",
                "Stopwords",
                "Stemming"
            ])
            
            # Max Features
            with tweak_tabs[0]:
                st.markdown("**Max Features Comparison (500 vs 3000 vs 5000)**")
                max_feat_results = []
                for max_feat in [500, 3000, 5000]:
                    key = f'Tweak_MaxFeatures_{max_feat}'
                    result = all_results['tweaks'][key]
                    max_feat_results.append({
                        'max_features': max_feat,
                        'Accuracy': f"{result['accuracy']:.4f}",
                        'Precision': f"{result['precision']:.4f}",
                        'Recall': f"{result['recall']:.4f}",
                        'F1-Score': f"{result['f1']:.4f}"
                    })
                max_df = pd.DataFrame(max_feat_results)
                st.dataframe(max_df, use_container_width=True, hide_index=True)
                
                # Chart
                fig = go.Figure()
                for max_feat in [500, 3000, 5000]:
                    key = f'Tweak_MaxFeatures_{max_feat}'
                    result = all_results['tweaks'][key]
                    fig.add_trace(go.Bar(
                        name=f'max_features={max_feat}',
                        x=['Accuracy', 'Precision', 'Recall', 'F1'],
                        y=[result['accuracy'], result['precision'], result['recall'], result['f1']]
                    ))
                fig.update_layout(
                    barmode='group', paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(17,24,39,0.6)', font_color='#e2e8f0',
                    legend=dict(bgcolor='rgba(0,0,0,0)'), height=350
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # NGram
            with tweak_tabs[1]:
                st.markdown("**NGram Range Comparison (Unigrams vs Bigrams)**")
                ngram_results = []
                for ngram in [(1, 1), (1, 2)]:
                    key = f'Tweak_Ngram_{ngram[0]}_{ngram[1]}'
                    result = all_results['tweaks'][key]
                    ngram_results.append({
                        'ngram_range': f'{ngram}',
                        'type': 'Unigrams' if ngram == (1, 1) else 'Unigrams + Bigrams',
                        'Accuracy': f"{result['accuracy']:.4f}",
                        'Precision': f"{result['precision']:.4f}",
                        'Recall': f"{result['recall']:.4f}",
                        'F1-Score': f"{result['f1']:.4f}"
                    })
                ngram_df = pd.DataFrame(ngram_results)
                st.dataframe(ngram_df, use_container_width=True, hide_index=True)
            
            # Alpha
            with tweak_tabs[2]:
                st.markdown("**Alpha (Smoothing) Comparison (0.1 vs 0.5 vs 1.0)**")
                alpha_results = []
                for alpha in [0.1, 0.5, 1.0]:
                    key = f'Tweak_Alpha_{str(alpha).replace(".", "_")}'
                    result = all_results['tweaks'][key]
                    alpha_results.append({
                        'alpha': alpha,
                        'Accuracy': f"{result['accuracy']:.4f}",
                        'Precision': f"{result['precision']:.4f}",
                        'Recall': f"{result['recall']:.4f}",
                        'F1-Score': f"{result['f1']:.4f}"
                    })
                alpha_df = pd.DataFrame(alpha_results)
                st.dataframe(alpha_df, use_container_width=True, hide_index=True)
                
                # Chart
                fig = go.Figure()
                for alpha in [0.1, 0.5, 1.0]:
                    key = f'Tweak_Alpha_{str(alpha).replace(".", "_")}'
                    result = all_results['tweaks'][key]
                    fig.add_trace(go.Scatter(
                        mode='lines+markers',
                        name=f'alpha={alpha}',
                        x=['Accuracy', 'Precision', 'Recall', 'F1'],
                        y=[result['accuracy'], result['precision'], result['recall'], result['f1']]
                    ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(17,24,39,0.6)', font_color='#e2e8f0',
                    legend=dict(bgcolor='rgba(0,0,0,0)'), height=350
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Stopwords
            with tweak_tabs[3]:
                st.markdown("**Stopword Removal Impact**")
                stopword_results = []
                for label in ['WithoutStopwords', 'WithStopwords']:
                    key = f'Tweak_Stopwords_{label}'
                    result = all_results['tweaks'][key]
                    stopword_results.append({
                        'Setting': 'Without Stopwords' if label == 'WithoutStopwords' else 'With Stopwords',
                        'Accuracy': f"{result['accuracy']:.4f}",
                        'Precision': f"{result['precision']:.4f}",
                        'Recall': f"{result['recall']:.4f}",
                        'F1-Score': f"{result['f1']:.4f}"
                    })
                sw_df = pd.DataFrame(stopword_results)
                st.dataframe(sw_df, use_container_width=True, hide_index=True)
            
            # Stemming
            with tweak_tabs[4]:
                st.markdown("**Stemming Impact**")
                stemming_results = []
                for label in ['WithoutStemming', 'WithStemming']:
                    key = f'Tweak_Stemming_{label}'
                    result = all_results['tweaks'][key]
                    stemming_results.append({
                        'Setting': 'Without Stemming' if label == 'WithoutStemming' else 'With Stemming',
                        'Accuracy': f"{result['accuracy']:.4f}",
                        'Precision': f"{result['precision']:.4f}",
                        'Recall': f"{result['recall']:.4f}",
                        'F1-Score': f"{result['f1']:.4f}"
                    })
                st_df = pd.DataFrame(stemming_results)
                st.dataframe(st_df, use_container_width=True, hide_index=True)
            
            # Full report
            st.markdown('<div class="section-header">Complete Report</div>', unsafe_allow_html=True)
            
            report = generate_report(all_results, df)
            st.download_button(
                label="📄 Download Full Report",
                data=report,
                file_name="EXPERIMENT_REPORT.txt",
                mime="text/plain"
            )
            
            with st.expander("📋 View Report in Browser"):
                st.text(report)
        
        except Exception as e:
            st.error(f"❌ Error running experiments: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
