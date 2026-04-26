import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


# Docs: https://docs.streamlit.io/develop/api-reference
import streamlit as st
import pandas as pd
from pipeline.scam_detector.detector import ScamDetector
from evaluate import calculate_metrics

st.set_page_config(page_title="Scam Detection App", layout="wide")
st.title("Scam Detection")

#Inititalize the backend scam detector
detector = ScamDetector()

#TAB LAYOUT
tab1, tab2 = st.tabs(["Single Message Detection", "Dataset Evaluation"])

with tab1:
    st.header("Single Message Scam Detection")
    
    user_input = st.text_area("Enter a message to analyze for scams:", height=150,
                              placeholder="Type or paste a message here...")
    
    if st.button("Analyze Message",type= "primary"):
        if user_input.strip()== "":
            st.warning("Please enter a message to analyze.")
        else:
            with st.spinner("Analyzing..."):
                result = detector.detect(user_input)
                    
            st.success("Analysis Complete!")
            col1, col2 = st.columns([2, 1])

            with col1:
                label = result.get("label", "Uncertain")
                if label == "Scam":
                    st.error(f"**PREDICTION: {label}**")
                elif label == "Not Scam":
                    st.success(f"**PREDICTION: {label}**")
                else:
                    st.warning(f"**PREDICTION: {label}**")
                
                intent = result.get("intent", "Unknown")
                st.info(f"**Intent Detected:** {intent}")
            
            with col2:
                # Display risk factors as a bullet list
                risk_factors = result.get("risk_factors", [])
                if risk_factors:
                    st.subheader("Risk Factors")
                    for factor in risk_factors:
                        st.text(f"• {factor}")
            

            reasoning = result.get("reasoning", "No reasoning provided")
            with st.expander("AI Reasoning Process", expanded=False):
                st.write(reasoning)


# ============================================================================
# TAB 2: DATASET EVALUATION
# ============================================================================

with tab2:
    st.header("Evaluate Model on Dataset")

    st.write("Upload a CSV file with columns `message_text` and `label` to evaluate the model's performance.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")


    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            text_col = None

            if 'text' in df.columns:
                text_col = 'text'
            elif 'message_text' in df.columns:
                text_col = 'message_text'
            if text_col is None or 'label' not in df.columns:
                st.error("CSV file must contain 'text' or 'message_text' column and 'label' column.")
            else:
                st.success(f"Successfully loaded dataset with {len(df)} rows.")

                with st.expander("Sample Data", expanded=False):
                    st.dataframe(df.head())
            
            col1,col2 = st.columns(2)
            with col1:
                limit = st.number_input("Limit number of messages to evaluate:", min_value=1, max_value=len(df), value=min(100, len(df)), step=1)
            with col2:
                if st.button("Evaluate Dataset", type="primary"):
                    with st.spinner("Processing Messages in Batches..."):
                        try:
                            messages = df[text_col].tolist()[:limit]
                            actual_labels = df['label'].tolist()[:limit]
                            predicted_results = detector.detect_batch(messages)
                            predicted_labels = [result['label'] for result in predicted_results]

                            results = calculate_metrics(actual_labels, predicted_labels)

                            st.success("Evaluation Complete!")

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Overall Accuracy", f"{results['accuracy']}%")
                            with col2:
                                st.metric("Total Predictions", results['total'])
                            with col3:
                                st.metric("Correct Predictions", results['correct'])
                        except Exception as e:
                            st.error(f"Error Processing the Dataset: {e}")



        except:
            st.error("Error reading the CSV file. Please ensure it is properly formatted.")
                    