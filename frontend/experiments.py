"""
Experiments Tab - Comprehensive Experimentation Framework
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from model import run_all_experiments, create_comparison_table, generate_report


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
            with st.spinner("Running experiments..."):
                all_results = run_all_experiments(df)
            
            st.success("✅ Experiments completed!")
            _display_experiment_results(all_results, df)
        
        except Exception as e:
            st.error(f"❌ Error running experiments: {str(e)}")
            import traceback
            st.error(traceback.format_exc())


def _display_experiment_results(all_results, df):
    """Display experiment results."""
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
            _display_main_experiment_details(all_results['main_experiments'][exp_key])
    
    # Tweaks analysis
    st.markdown('<div class="section-header">Hyperparameter Tweaks Analysis</div>', unsafe_allow_html=True)
    
    tweak_tabs = st.tabs([
        "Max Features",
        "NGram Range",
        "Alpha (Smoothing)",
        "Stopwords",
        "Stemming"
    ])
    
    _display_tweaks_analysis(all_results['tweaks'], tweak_tabs)
    
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


def _display_main_experiment_details(result):
    """Display details for a main experiment."""
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


def _display_tweaks_analysis(tweaks, tweak_tabs):
    """Display analysis for hyperparameter tweaks."""
    
    # Max Features
    with tweak_tabs[0]:
        st.markdown("**Max Features Comparison (500 vs 3000 vs 5000)**")
        max_feat_results = []
        for max_feat in [500, 3000, 5000]:
            key = f'Tweak_MaxFeatures_{max_feat}'
            result = tweaks[key]
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
            result = tweaks[key]
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
            result = tweaks[key]
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
            result = tweaks[key]
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
            result = tweaks[key]
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
            result = tweaks[key]
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
            result = tweaks[key]
            stemming_results.append({
                'Setting': 'Without Stemming' if label == 'WithoutStemming' else 'With Stemming',
                'Accuracy': f"{result['accuracy']:.4f}",
                'Precision': f"{result['precision']:.4f}",
                'Recall': f"{result['recall']:.4f}",
                'F1-Score': f"{result['f1']:.4f}"
            })
        st_df = pd.DataFrame(stemming_results)
        st.dataframe(st_df, use_container_width=True, hide_index=True)
