import random
import numpy as np
from utils import categorize_ethical_factors

def explain_classification(analysis_result, factors, classification, nlp):
    """
    Generate a detailed explanation for the classification
    
    Args:
        analysis_result: Dictionary with analysis results
        factors: Dictionary with contributing ethical factors
        classification: String classification label
        nlp: spaCy NLP model
    
    Returns:
        String with detailed explanation
    """
    # Get probabilities
    ethical_prob = analysis_result['ethical_prob']
    ambiguous_prob = analysis_result['ambiguous_prob']
    unethical_prob = analysis_result['unethical_prob']
    
    # Get top factors
    top_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Create explanation based on classification
    if classification == "Ethical":
        explanation = f"This scenario is classified as **ethical** with {ethical_prob:.0%} confidence. "
        explanation += "The key factors contributing to this assessment are:\n\n"
        
        for factor, score in top_factors:
            if factor == "transparency":
                explanation += f"- **Transparency** ({score:.0%}): The scenario demonstrates clear and open communication with appropriate disclosures.\n"
            elif factor == "fairness":
                explanation += f"- **Fairness** ({score:.0%}): The actions described treat all stakeholders equitably without bias or discrimination.\n"
            elif factor == "integrity":
                explanation += f"- **Integrity** ({score:.0%}): The situation shows honesty and adherence to moral and ethical principles.\n"
            elif factor == "legality":
                explanation += f"- **Legality** ({score:.0%}): The actions are in compliance with applicable laws and regulations.\n"
            elif factor == "harm":
                explanation += f"- **Harm Prevention** ({score:.0%}): Appropriate steps are taken to prevent potential harm to stakeholders.\n"
            elif factor == "consent":
                explanation += f"- **Informed Consent** ({score:.0%}): All parties involved have given proper informed consent.\n"
            elif factor == "conflict_of_interest":
                explanation += f"- **Conflict of Interest Management** ({score:.0%}): Potential conflicts of interest are appropriately managed or avoided.\n"
            elif factor == "responsibility":
                explanation += f"- **Responsibility** ({score:.0%}): The scenario demonstrates appropriate assumption of professional responsibilities.\n"
                
        explanation += f"\nThe analysis also indicates a {ambiguous_prob:.0%} probability of ethical ambiguity and a {unethical_prob:.0%} probability of unethical elements."
        
    elif classification == "Ethically Ambiguous":
        explanation = f"This scenario is classified as **ethically ambiguous** with {ambiguous_prob:.0%} confidence. "
        explanation += "The analysis reveals competing ethical considerations:\n\n"
        
        for factor, score in top_factors:
            if factor == "transparency":
                explanation += f"- **Transparency Concerns** ({score:.0%}): There may be questions about whether all relevant information is being appropriately disclosed.\n"
            elif factor == "fairness":
                explanation += f"- **Fairness Considerations** ({score:.0%}): The scenario presents potential inequities or situations where different stakeholders' interests conflict.\n"
            elif factor == "integrity":
                explanation += f"- **Integrity Questions** ({score:.0%}): Some aspects of the situation raise questions about adherence to ethical principles.\n"
            elif factor == "legality":
                explanation += f"- **Regulatory Gray Areas** ({score:.0%}): The situation may involve compliance complexities or regulatory gray areas.\n"
            elif factor == "harm":
                explanation += f"- **Potential Harm** ({score:.0%}): There are considerations about possible negative impacts to certain stakeholders.\n"
            elif factor == "consent":
                explanation += f"- **Consent Ambiguities** ({score:.0%}): Questions exist about whether all parties have given proper informed consent.\n"
            elif factor == "conflict_of_interest":
                explanation += f"- **Potential Conflicts** ({score:.0%}): The scenario contains potential conflicts of interest that require careful management.\n"
            elif factor == "responsibility":
                explanation += f"- **Competing Responsibilities** ({score:.0%}): There appear to be competing professional responsibilities or obligations.\n"
                
        explanation += f"\nThe analysis also indicates a {ethical_prob:.0%} probability of ethical elements and a {unethical_prob:.0%} probability of unethical elements."
        
    else:  # Unethical
        explanation = f"This scenario is classified as **unethical** with {unethical_prob:.0%} confidence. "
        explanation += "The key concerns identified in this scenario are:\n\n"
        
        for factor, score in top_factors:
            if factor == "transparency":
                explanation += f"- **Lack of Transparency** ({score:.0%}): The scenario involves inadequate disclosure or deliberate concealment of important information.\n"
            elif factor == "fairness":
                explanation += f"- **Unfairness** ({score:.0%}): The actions described demonstrate bias, discrimination, or inequitable treatment of stakeholders.\n"
            elif factor == "integrity":
                explanation += f"- **Integrity Violations** ({score:.0%}): The situation shows dishonesty or violations of ethical principles.\n"
            elif factor == "legality":
                explanation += f"- **Legal/Regulatory Concerns** ({score:.0%}): The actions may violate applicable laws, regulations, or organizational policies.\n"
            elif factor == "harm":
                explanation += f"- **Potential Harm** ({score:.0%}): The scenario presents significant risk of harm to stakeholders.\n"
            elif factor == "consent":
                explanation += f"- **Consent Issues** ({score:.0%}): Actions are taken without proper informed consent from affected parties.\n"
            elif factor == "conflict_of_interest":
                explanation += f"- **Conflicts of Interest** ({score:.0%}): Unmanaged conflicts of interest compromise professional judgment.\n"
            elif factor == "responsibility":
                explanation += f"- **Abdication of Responsibility** ({score:.0%}): The scenario demonstrates failure to meet professional responsibilities.\n"
                
        explanation += f"\nThe analysis also indicates a {ethical_prob:.0%} probability of ethical elements and a {ambiguous_prob:.0%} probability of ethical ambiguity."
    
    # Add banking/finance specific context
    explanation += "\n\n**Banking/Finance Context:**\n"
    if classification == "Ethical":
        explanation += "This approach aligns with banking industry best practices and likely meets regulatory requirements. Financial institutions that maintain high ethical standards typically benefit from enhanced reputation, customer trust, and reduced regulatory scrutiny."
    elif classification == "Ethically Ambiguous":
        explanation += "Financial institutions often face these types of ethical gray areas. While the scenario may not violate specific regulations, it raises questions about fiduciary duty, fair treatment of customers, and alignment with the institution's stated values. Additional context or policy guidance may be needed."
    else:  # Unethical
        explanation += "This scenario presents significant risks in the banking/finance context, including potential regulatory violations, reputational damage, loss of customer trust, and possible legal consequences. Financial institutions are held to high standards of ethical conduct due to their role as stewards of customer assets and the broader financial system."
    
    return explanation

def generate_future_implications(text, classification, factors, nlp):
    """
    Generate potential future implications based on the ethical analysis
    
    Args:
        text: Preprocessed dilemma text
        classification: String classification label
        factors: Dictionary with contributing ethical factors
        nlp: spaCy NLP model
    
    Returns:
        List of implications
    """
    implications = []
    
    # Get top factors
    top_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)[:3]
    top_factor_names = [factor for factor, _ in top_factors]
    
    # Generate implications based on classification and top factors
    if classification == "Ethical":
        implications.append("Maintaining this ethical approach should strengthen stakeholder trust and enhance reputation.")
        
        if "transparency" in top_factor_names:
            implications.append("The demonstrated transparency could be documented as a best practice for similar situations.")
        
        if "fairness" in top_factor_names:
            implications.append("The equitable approach sets a positive precedent for fair treatment of all clients/stakeholders.")
        
        if "integrity" in top_factor_names:
            implications.append("Continued ethical behavior will strengthen organizational culture and employee morale.")
            
        if "legality" in top_factor_names:
            implications.append("Regulatory compliance reduces the risk of penalties and enhances relationships with regulators.")
            
        implications.append("This ethical handling may present an opportunity for positive recognition within the organization.")
            
    elif classification == "Ethically Ambiguous":
        implications.append("Without clear resolution, this ambiguity could lead to inconsistent handling of similar situations.")
        
        if "transparency" in top_factor_names:
            implications.append("Addressing transparency concerns would reduce risk of stakeholder misunderstandings or complaints.")
        
        if "fairness" in top_factor_names:
            implications.append("The perceived fairness issues could impact client/employee trust if not addressed constructively.")
        
        if "integrity" in top_factor_names:
            implications.append("Ethical ambiguity might send mixed signals about organizational values and expected conduct.")
            
        if "conflict_of_interest" in top_factor_names:
            implications.append("Unresolved conflicts of interest may lead to increased scrutiny from compliance or regulators.")
            
        implications.append("Creating clear guidelines for handling similar situations would benefit organizational consistency.")
        
    else:  # Unethical
        implications.append("This approach carries significant risk of regulatory penalties, legal action, or reputational damage.")
        
        if "transparency" in top_factor_names:
            implications.append("Lack of transparency could erode stakeholder trust and prompt regulatory investigation.")
        
        if "fairness" in top_factor_names:
            implications.append("Unfair practices may lead to client complaints, legal challenges, or regulatory attention.")
        
        if "integrity" in top_factor_names:
            implications.append("Integrity violations can damage organizational culture and lead to further ethical breaches.")
            
        if "legality" in top_factor_names:
            implications.append("Potential legal or regulatory violations could result in fines, sanctions, or litigation.")
            
        implications.append("Immediate corrective action should be considered to mitigate potential negative consequences.")
    
    # Add one banking/finance specific implication
    if classification == "Ethical":
        implications.append("From a banking/finance perspective, this ethical approach may strengthen client relationships and potentially increase assets under management through enhanced trust.")
    elif classification == "Ethically Ambiguous":
        implications.append("In the financial sector, this ambiguity could create precedents that affect how the institution balances fiduciary duty with profit motives in future scenarios.")
    else:  # Unethical
        implications.append("Financial institutions face heightened scrutiny; this situation could trigger whistleblower actions, regulatory investigations, or class action lawsuits if not addressed.")
    
    return implications