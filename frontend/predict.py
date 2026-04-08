"""
Predict Tab - Real-time SMS Classification
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


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
