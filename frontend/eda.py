"""
EDA Tab - Exploratory Data Analysis
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from backend import create_wordcloud, get_top_words


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
