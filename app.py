import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import base64
import time
import json
from datetime import datetime



from models import load_models
from utils import preprocess_text, get_banking_keywords, get_finance_keywords, get_ethical_keywords
from analyzer import analyze_dilemma, classify_dilemma, get_ethics_score, get_contributing_factors
from explainer import explain_classification, generate_future_implications
from reporter import generate_pdf_report
from database import Database

# Page config
st.set_page_config(
    page_title="AI-POWERED VIRTUAL ETHICAL DILEMMA SOLVER",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load models
@st.cache_resource
def init_models():
    return load_models()

classifier_model, vectorizer, nlp = init_models()

# Title and description
st.title("AI-POWERED VIRTUAL ETHICAL DILEMMA SOLVER")
st.subheader("AI-powered ethical dilemma solver for banking and finance professionals")

st.markdown("""
This tool helps banking and finance professionals analyze ethical dilemmas,
classify them according to ethical principles, and receive recommendations
on how to proceed in accordance with industry best practices and regulations.
""")

# Initialize session state
if 'dilemma_submitted' not in st.session_state:
    st.session_state.dilemma_submitted = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'dilemma_text' not in st.session_state:
    st.session_state.dilemma_text = ""
if 'dilemma_context' not in st.session_state:
    st.session_state.dilemma_context = ""
if 'dilemma_stakeholders' not in st.session_state:
    st.session_state.dilemma_stakeholders = ""
if 'dilemma_classification' not in st.session_state:
    st.session_state.dilemma_classification = None
if 'ethics_score' not in st.session_state:
    st.session_state.ethics_score = 0
if 'explanation' not in st.session_state:
    st.session_state.explanation = ""
if 'implications' not in st.session_state:
    st.session_state.implications = []
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
if 'factors' not in st.session_state:
    st.session_state.factors = {}

# Sidebar
with st.sidebar:
    st.header("About AI-POWERED VIRTUAL ETHICAL DILEMMA SOLVER")
    st.markdown("""
    Our tool uses machine learning and natural language processing to:
    
    - Analyze ethical dilemmas in finance
    - Classify situations based on ethical principles
    - Explain the reasoning behind classifications
    - Provide recommendations aligned with industry regulations
    - Analyze potential future implications
    """)
    
    st.markdown("---")
    st.subheader("Industry Focus Areas")
    
    industry_tabs = st.tabs(["Banking", "Finance", "Ethics"])
    
    with industry_tabs[0]:
        banking_keywords = get_banking_keywords()
        st.write("Banking context keywords:")
        st.write(", ".join(banking_keywords[:10]) + "...")
    
    with industry_tabs[1]:
        finance_keywords = get_finance_keywords()
        st.write("Finance context keywords:")
        st.write(", ".join(finance_keywords[:10]) + "...")
    
    with industry_tabs[2]:
        ethical_keywords = get_ethical_keywords()
        st.write("Ethical principle keywords:")
        st.write(", ".join(ethical_keywords[:10]) + "...")

# Main interface
if not st.session_state.dilemma_submitted:
    st.header("Describe Your Ethical Dilemma")
    
    with st.form("dilemma_input_form"):
        dilemma_text = st.text_area(
            "Describe the ethical dilemma in detail:", 
            height=150,
            placeholder="Example: A client has asked me to approve a loan with documentation that seems suspicious..."
        )
        
        dilemma_context = st.text_area(
            "Provide context (optional):", 
            height=100,
            placeholder="Example: This occurred in the context of a retail banking operation..."
        )
        
        dilemma_stakeholders = st.text_area(
            "List stakeholders involved (optional):", 
            height=75,
            placeholder="Example: Client, bank shareholders, regulatory bodies, other customers..."
        )
        
        submit_button = st.form_submit_button("Analyze Dilemma")
        
        if submit_button:
            if not dilemma_text:
                st.error("Please describe the ethical dilemma before submitting.")
            else:
                st.session_state.dilemma_text = dilemma_text
                st.session_state.dilemma_context = dilemma_context
                st.session_state.dilemma_stakeholders = dilemma_stakeholders
                st.session_state.dilemma_submitted = True
                st.rerun()

else:
    st.header("Ethical Dilemma Analysis")
    
    with st.expander("Dilemma Details", expanded=True):
        st.subheader("Described Dilemma")
        st.write(st.session_state.dilemma_text)
        
        if st.session_state.dilemma_context:
            st.subheader("Context")
            st.write(st.session_state.dilemma_context)
        
        if st.session_state.dilemma_stakeholders:
            st.subheader("Stakeholders")
            st.write(st.session_state.dilemma_stakeholders)
    
    if not st.session_state.analysis_complete:
        with st.spinner("Analyzing the ethical dilemma..."):
            # Prepare the full text for analysis
            full_text = st.session_state.dilemma_text
            if st.session_state.dilemma_context:
                full_text += " " + st.session_state.dilemma_context
            if st.session_state.dilemma_stakeholders:
                full_text += " Stakeholders: " + st.session_state.dilemma_stakeholders
            
            # Preprocess the text
            processed_text = preprocess_text(full_text, nlp)
            
            # Get analysis results
            analysis_result = analyze_dilemma(processed_text, classifier_model, vectorizer)
            classification = classify_dilemma(analysis_result)
            ethics_score = get_ethics_score(analysis_result)
            factors = get_contributing_factors(processed_text, nlp)
            
            # Generate explanations and recommendations
            explanation = explain_classification(analysis_result, factors, classification, nlp)
            implications = generate_future_implications(processed_text, classification, factors, nlp)
            
            # Store results in session state
            st.session_state.dilemma_classification = classification
            st.session_state.ethics_score = ethics_score
            st.session_state.explanation = explanation
            st.session_state.implications = implications
            st.session_state.factors = factors
            
            # Generate recommendations based on classification and factors
            recommendations = []
            if classification == "Ethical":
                recommendations.append("Document the decision-making process for future reference")
                recommendations.append("Consider creating a case study for training purposes")
                recommendations.append("Evaluate if any policy improvements could be made based on this case")
            elif classification == "Ethically Ambiguous":
                recommendations.append("Consult with compliance and ethics departments")
                recommendations.append("Consider escalating to senior management")
                recommendations.append("Document all considerations and decision rationale")
                recommendations.append("Review relevant regulations and internal policies")
            else:  # Unethical
                recommendations.append("Report the situation to appropriate authorities if required by regulations")
                recommendations.append("Consult with legal and compliance departments immediately")
                recommendations.append("Document all details and maintain records")
                recommendations.append("Consider implementing additional controls to prevent similar situations")
            
            st.session_state.recommendations = recommendations
            st.session_state.analysis_complete = True
            time.sleep(1)  # Give a moment for the spinner to show
            
    # Display analysis results
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Classification")
        classification = st.session_state.dilemma_classification
        
        if classification == "Ethical":
            st.success("This scenario appears to be **Ethical**")
        elif classification == "Ethically Ambiguous":
            st.warning("This scenario is **Ethically Ambiguous**")
        else:
            st.error("This scenario appears to be **Unethical**")
        
        st.subheader("Ethics Score")
        ethics_score = st.session_state.ethics_score
        
        # Create a gauge chart with Plotly
        fig = px.pie(values=[ethics_score, 100-ethics_score], 
                    names=["Ethics Score", ""], 
                    hole=0.7,
                    color_discrete_sequence=["#1f77b4", "#e0e0e0"])
        
        fig.update_layout(
            annotations=[dict(text=f"{ethics_score}/100", x=0.5, y=0.5, font_size=20, showarrow=False)],
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            height=200
        )
        
        st.plotly_chart(fig)
    
    with col2:
        st.subheader("Contributing Factors")
        factors = st.session_state.factors
        
        if factors:
            # Prepare data for horizontal bar chart
            factor_names = list(factors.keys())
            factor_values = list(factors.values())
            
            fig, ax = plt.subplots(figsize=(5, 4))
            bars = ax.barh(factor_names, factor_values)
            
            # Add color gradient based on value
            for i, bar in enumerate(bars):
                bar.set_color(plt.cm.Blues(factor_values[i]/max(factor_values)))
            
            ax.set_xlabel('Contribution Score')
            ax.set_title('Ethical Factor Contribution')
            plt.tight_layout()
            
            st.pyplot(fig)
    
    st.subheader("Explanation")
    st.write(st.session_state.explanation)
    
    st.subheader("Future Implications")
    for impl in st.session_state.implications:
        st.markdown(f"• {impl}")
    
    st.subheader("Recommendations")
    for i, rec in enumerate(st.session_state.recommendations):
        st.markdown(f"{i+1}. {rec}")
    
    # Report generation
    st.subheader("Generate Report")
    if st.button("Generate PDF Report"):
        with st.spinner("Generating PDF report..."):
            pdf_bytes = generate_pdf_report(
                dilemma_text=st.session_state.dilemma_text,
                dilemma_context=st.session_state.dilemma_context,
                dilemma_stakeholders=st.session_state.dilemma_stakeholders,
                classification=st.session_state.dilemma_classification,
                ethics_score=st.session_state.ethics_score,
                explanation=st.session_state.explanation,
                implications=st.session_state.implications,
                recommendations=st.session_state.recommendations,
                factors=st.session_state.factors
            )
            
            # Create download link
            b64 = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="ethics_analysis_report.pdf">Download Ethics Analysis Report</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    # Save to database section
    st.subheader("Save Analysis to Database")
    case_title = st.text_input("Case Title (for reference)", placeholder="Enter a title for this ethical case")
    if st.button("Save to Database"):
        if case_title:
            try:
                # Initialize database connection
                db = Database()
                
                # Prepare case data
                case_data = {
                    "case_title": case_title,
                    "dilemma_text": st.session_state.dilemma_text,
                    "dilemma_context": st.session_state.dilemma_context,
                    "dilemma_stakeholders": st.session_state.dilemma_stakeholders,
                    "classification": st.session_state.dilemma_classification,
                    "ethics_score": st.session_state.ethics_score,
                    "explanation": st.session_state.explanation,
                    "implications": st.session_state.implications,
                    "recommendations": st.session_state.recommendations,
                    "factors": st.session_state.factors
                }
                
                # Save to database
                case_id = db.save_case(case_data)
                db.close()
                
                st.success(f"Case '{case_title}' saved successfully with ID: {case_id}")
            except Exception as e:
                st.error(f"Error saving to database: {str(e)}")
        else:
            st.warning("Please enter a title for the case before saving")
    
    # Reset button
    if st.button("Analyze Another Dilemma"):
        for key in st.session_state.keys():
            if key != "model_loaded":
                del st.session_state[key]
        st.session_state.dilemma_submitted = False
        st.session_state.analysis_complete = False
        st.rerun()