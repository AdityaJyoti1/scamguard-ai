import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


# Docs: https://docs.streamlit.io/develop/api-reference
import streamlit as st
import pandas as pd
from pipeline.scam_detector.detector import ScamDetector
from evaluate import evaluate_model

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