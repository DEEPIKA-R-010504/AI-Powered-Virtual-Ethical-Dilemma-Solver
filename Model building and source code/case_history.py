import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime
import json

from database import Database
from reporter import generate_pdf_report

# Page config
st.set_page_config(
    page_title="EthicsAI Finance Advisor - Case History",
    page_icon="📚",
    layout="wide",
)

# Title and description
st.title("Ethical Dilemma Case History")
st.subheader("View, search, and analyze past ethical dilemma cases")

# Initialize database connection
@st.cache_resource
def init_database():
    return Database()

# Function to display case details
def display_case_details(case):
    # Create tabs for different sections
    tabs = st.tabs(["Summary", "Explanation", "Implications", "Recommendations", "Generate Report"])
    
    with tabs[0]:  # Summary tab
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader("Classification")
            classification = case["classification"]
            
            if classification == "Ethical":
                st.success("This scenario appears to be **Ethical**")
            elif classification == "Ethically Ambiguous":
                st.warning("This scenario is **Ethically Ambiguous**")
            else:
                st.error("This scenario appears to be **Unethical**")
            
            st.subheader("Ethics Score")
            ethics_score = case["ethics_score"]
            
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
            factors = case["factors"]
            
            if factors:
                # Prepare data for bar chart
                factor_df = pd.DataFrame({
                    'Factor': [factor.replace('_', ' ').title() for factor in factors.keys()],
                    'Score': [value for value in factors.values()]
                })
                
                # Sort by score descending
                factor_df = factor_df.sort_values('Score', ascending=False)
                
                # Create bar chart
                fig = px.bar(
                    factor_df, 
                    x='Score', 
                    y='Factor',
                    orientation='h',
                    color='Score',
                    color_continuous_scale='Blues'
                )
                
                fig.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=300
                )
                
                st.plotly_chart(fig)
    
    with tabs[1]:  # Explanation tab
        st.subheader("Dilemma Text")
        st.write(case["dilemma_text"])
        
        if case["dilemma_context"]:
            st.subheader("Context")
            st.write(case["dilemma_context"])
        
        if case["dilemma_stakeholders"]:
            st.subheader("Stakeholders")
            st.write(case["dilemma_stakeholders"])
        
        st.subheader("Explanation")
        st.write(case["explanation"])
    
    with tabs[2]:  # Implications tab
        st.subheader("Future Implications")
        for impl in case["implications"]:
            st.markdown(f"• {impl}")
    
    with tabs[3]:  # Recommendations tab
        st.subheader("Recommendations")
        for i, rec in enumerate(case["recommendations"]):
            st.markdown(f"{i+1}. {rec}")
    
    with tabs[4]:  # Generate Report tab
        st.subheader("Generate PDF Report")
        if st.button("Generate PDF Report", key=f"gen_pdf_{case['id']}"):
            with st.spinner("Generating PDF report..."):
                pdf_bytes = generate_pdf_report(
                    dilemma_text=case["dilemma_text"],
                    dilemma_context=case["dilemma_context"],
                    dilemma_stakeholders=case["dilemma_stakeholders"],
                    classification=case["classification"],
                    ethics_score=case["ethics_score"],
                    explanation=case["explanation"],
                    implications=case["implications"],
                    recommendations=case["recommendations"],
                    factors=case["factors"]
                )
                
                # Create download link
                b64 = base64.b64encode(pdf_bytes).decode()
                download_filename = f"ethics_case_{case['id']}_report.pdf"
                href = f'<a href="data:application/pdf;base64,{b64}" download="{download_filename}">Download Ethics Analysis Report</a>'
                st.markdown(href, unsafe_allow_html=True)

# Main app
db = init_database()

# Sidebar with search and filter options
with st.sidebar:
    st.header("Search & Filter")
    
    # Search box
    search_term = st.text_input("Search by keyword", placeholder="Enter keywords...")
    
    # Filter by classification
    st.subheader("Filter by Classification")
    show_ethical = st.checkbox("Ethical", value=True)
    show_ambiguous = st.checkbox("Ethically Ambiguous", value=True)
    show_unethical = st.checkbox("Unethical", value=True)
    
    # Apply filters button
    filter_button = st.button("Apply Filters")

# Main content area
try:
    # Get cases based on search and filters
    if search_term:
        cases = db.search_cases(search_term)
    else:
        cases = db.get_all_cases()
    
    # Apply classification filters
    filtered_cases = []
    for case in cases:
        if (case["classification"] == "Ethical" and show_ethical) or \
           (case["classification"] == "Ethically Ambiguous" and show_ambiguous) or \
           (case["classification"] == "Unethical" and show_unethical):
            filtered_cases.append(case)
    
    # Display case count
    st.write(f"Found {len(filtered_cases)} ethical dilemma cases")
    
    if not filtered_cases:
        st.info("No cases found. Try adjusting your search criteria or add new cases from the main page.")
    else:
        # Create case cards
        for i, case in enumerate(filtered_cases):
            with st.expander(f"Case #{case['id']}: {case['case_title']} ({case['classification']})", expanded=(i==0)):
                display_case_details(case)
except Exception as e:
    st.error(f"Error retrieving cases: {str(e)}")
finally:
    db.close()