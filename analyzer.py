import numpy as np
import pandas as pd
import re
from collections import Counter
from utils import categorize_ethical_factors

def analyze_dilemma(text, model, transformer):
    """
    Analyze the ethical dilemma text using transformer embeddings
    
    Args:
        text: Preprocessed dilemma text
        model: Trained classification model
        transformer: Sentence transformer model for embeddings
    
    Returns:
        Dictionary with analysis results
    """
    # Get text embeddings
    embedding = transformer.encode([text])[0].reshape(1, -1)
    
    # Get model prediction probabilities
    probs = model.predict_proba(embedding)[0]
    
    # Get prediction
    prediction = np.argmax(probs)
    
    # Create analysis result dictionary
    result = {
        'text': text,
        'prediction': prediction,
        'unethical_prob': probs[0] if len(probs) > 0 else 0,
        'ambiguous_prob': probs[1] if len(probs) > 1 else 0,
        'ethical_prob': probs[2] if len(probs) > 2 else 0,
    }
    
    return result

def classify_dilemma(analysis_result):
    """
    Convert numeric prediction to text classification
    
    Args:
        analysis_result: Dictionary with analysis results
    
    Returns:
        String classification: "Ethical", "Ethically Ambiguous", or "Unethical"
    """
    prediction = analysis_result['prediction']
    
    if prediction == 2:
        return "Ethical"
    elif prediction == 1:
        return "Ethically Ambiguous"
    else:
        return "Unethical"

def get_ethics_score(analysis_result):
    """
    Calculate an ethics score from 0-100 based on prediction probabilities
    
    Args:
        analysis_result: Dictionary with analysis results
    
    Returns:
        Integer score from 0-100
    """
    # Calculate weighted score:
    # 0 * unethical_prob + 50 * ambiguous_prob + 100 * ethical_prob
    score = (0 * analysis_result['unethical_prob'] + 
             50 * analysis_result['ambiguous_prob'] + 
             100 * analysis_result['ethical_prob'])
    
    # Round to nearest integer
    return int(round(score))

def get_contributing_factors(text, preprocessor):
    """
    Identify ethical factors contributing to the classification
    Using simple text analysis without spaCy
    
    Args:
        text: Preprocessed dilemma text
        preprocessor: Text preprocessing function
    
    Returns:
        Dictionary with factor categories and their scores
    """
    # Get factor categories and related terms
    factor_categories = categorize_ethical_factors()
    
    # Preprocess and tokenize text
    processed_text = preprocessor(text.lower())
    tokens = processed_text.split()
    
    # Count occurrences of each category's terms
    factor_scores = {}
    for category, terms in factor_categories.items():
        score = 0
        for term in terms:
            # Count occurrences of the term in tokens
            term_count = sum(1 for token in tokens if term in token)
            score += term_count
        
        # Only include factors with non-zero scores
        if score > 0:
            factor_scores[category] = score
    
    # Normalize scores if we have any factors
    if factor_scores:
        max_score = max(factor_scores.values())
        factor_scores = {k: round(v / max_score, 2) for k, v in factor_scores.items()}
    
    # If no factors were found, add some defaults
    if not factor_scores:
        factor_scores = {
            "transparency": 0.5,
            "fairness": 0.5,
            "integrity": 0.5
        }
    
    return factor_scores