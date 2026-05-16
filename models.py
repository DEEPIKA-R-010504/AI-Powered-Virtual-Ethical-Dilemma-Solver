import streamlit as st
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from training_data import get_training_data

# Simple text preprocessing
def simple_preprocess(text):
    """Simple text preprocessor without spaCy dependency"""
    # Lowercase
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def create_transformer_classifier():
    """Create a classifier for ethical dilemmas"""
    return LogisticRegression(
        C=1.0,
        class_weight='balanced',
        max_iter=1000,
        random_state=42,
        n_jobs=-1
    )

@st.cache_resource
def load_models():
    """Load or train transformer models for ethical dilemma analysis"""
    # Load sentence transformer
    model_name = "all-MiniLM-L6-v2"  # Lightweight but effective model
    sentence_transformer = SentenceTransformer(model_name)
    
    # Get training data
    X, y = get_training_data()
    
    # Split into train/test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Get embeddings for training data
    X_train_embeddings = sentence_transformer.encode(X_train)
    
    # Train classifier on embeddings
    classifier = create_transformer_classifier()
    classifier.fit(X_train_embeddings, y_train)
    
    return classifier, sentence_transformer, simple_preprocess