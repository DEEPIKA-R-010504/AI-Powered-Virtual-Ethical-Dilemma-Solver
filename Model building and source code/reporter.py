import io
import base64
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf_report(dilemma_text, dilemma_context, dilemma_stakeholders, 
                       classification, ethics_score, explanation, 
                       implications, recommendations, factors):
    """
    Generate a PDF report of the ethical dilemma analysis
    
    Args:
        dilemma_text: The original dilemma description
        dilemma_context: Additional context information
        dilemma_stakeholders: Stakeholders involved
        classification: Ethical classification result
        ethics_score: Numerical ethics score
        explanation: Detailed explanation of the classification
        implications: List of future implications
        recommendations: List of recommendations
        factors: Dictionary of contributing ethical factors
    
    Returns:
        PDF report as bytes
    """
    # Create a buffer for the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    subheading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Create custom styles
    label_style = ParagraphStyle(
        name='LabelStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        spaceAfter=5
    )
    
    value_style = ParagraphStyle(
        name='ValueStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leftIndent=20,
        spaceAfter=10
    )
    
    # Create a story to hold all elements
    story = []
    
    # Add title
    story.append(Paragraph("Ethical Dilemma Analysis Report", title_style))
    story.append(Spacer(1, 0.25*inch))
    
    # Add date
    current_date = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"Report Date: {current_date}", normal_style))
    story.append(Spacer(1, 0.25*inch))
    
    # Add dilemma details
    story.append(Paragraph("Ethical Dilemma Details", heading_style))
    
    story.append(Paragraph("Dilemma Description:", label_style))
    story.append(Paragraph(dilemma_text, value_style))
    
    if dilemma_context:
        story.append(Paragraph("Context:", label_style))
        story.append(Paragraph(dilemma_context, value_style))
    
    if dilemma_stakeholders:
        story.append(Paragraph("Stakeholders:", label_style))
        story.append(Paragraph(dilemma_stakeholders, value_style))
    
    story.append(Spacer(1, 0.25*inch))
    
    # Add classification results
    story.append(Paragraph("Analysis Results", heading_style))
    
    # Classification
    story.append(Paragraph("Classification:", label_style))
    
    # Make the classification colored based on the result
    if classification == "Ethical":
        classification_color = colors.green
    elif classification == "Ethically Ambiguous":
        classification_color = colors.orange
    else:  # Unethical
        classification_color = colors.red
    
    classification_style = ParagraphStyle(
        name='ClassificationStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=classification_color,
        leftIndent=20,
        spaceAfter=10
    )
    
    story.append(Paragraph(classification, classification_style))
    
    # Ethics Score
    story.append(Paragraph("Ethics Score:", label_style))
    
    # Create a figure for the ethics score
    fig = plt.figure(figsize=(4, 1))
    ax = fig.add_subplot(111)
    
    # Draw a horizontal progress bar
    ax.barh(0, ethics_score, height=0.5, color='#1f77b4')
    ax.barh(0, 100, height=0.5, color='#d3d3d3', alpha=0.3)
    
    # Add the score as text
    ax.text(ethics_score / 2, 0, f"{ethics_score}/100", 
            ha='center', va='center', color='white', fontweight='bold')
    
    # Remove axes
    ax.axis('off')
    
    # Save to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
    img_buffer.seek(0)
    
    # Create Image object and add to story
    score_img = Image(img_buffer, width=3*inch, height=0.75*inch)
    story.append(score_img)
    story.append(Spacer(1, 0.25*inch))
    
    # Contributing Factors
    if factors:
        story.append(Paragraph("Contributing Factors:", label_style))
        
        # Create table for factors
        factor_data = [['Factor', 'Contribution']]
        for factor, value in factors.items():
            # Format the factor name to be more readable
            factor_name = factor.replace('_', ' ').title()
            factor_data.append([factor_name, f"{int(value * 100)}%"])
        
        # Create table
        factor_table = Table(factor_data, colWidths=[2.5*inch, 1*inch])
        
        # Add style to table
        factor_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        story.append(factor_table)
        story.append(Spacer(1, 0.25*inch))
    
    # Explanation
    story.append(Paragraph("Explanation:", label_style))
    
    # Split explanation by paragraphs and add each one
    explanation_paragraphs = explanation.split('\n\n')
    for para in explanation_paragraphs:
        # Process markdown-style bold formatting
        para = para.replace('**', '<b>', 1)
        para = para.replace('**', '</b>', 1)
        
        # Process bullet points
        if para.startswith('- '):
            para = '• ' + para[2:]
            
        story.append(Paragraph(para, value_style))
    
    story.append(Spacer(1, 0.25*inch))
    
    # Future Implications
    story.append(Paragraph("Future Implications", heading_style))
    
    for impl in implications:
        story.append(Paragraph(f"• {impl}", value_style))
    
    story.append(Spacer(1, 0.25*inch))
    
    # Recommendations
    story.append(Paragraph("Recommendations", heading_style))
    
    for i, rec in enumerate(recommendations):
        story.append(Paragraph(f"{i+1}. {rec}", value_style))
    
    # Build the PDF
    doc.build(story)
    
    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data