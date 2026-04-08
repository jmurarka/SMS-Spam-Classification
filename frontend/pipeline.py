"""
Pipeline Tab - Preprocessing Pipeline and Feature Engineering
"""
import streamlit as st
import pandas as pd


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
