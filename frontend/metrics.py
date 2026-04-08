"""
Metrics Tab - Model Performance Analysis
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, roc_auc_score


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
