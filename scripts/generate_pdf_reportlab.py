#!/usr/bin/env python
"""Generate PDF from markdown using reportlab."""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import re

def generate_pdf(md_file, pdf_file):
    """Generate PDF from markdown file."""
    
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                           topMargin=0.75*inch,
                           bottomMargin=0.75*inch,
                           leftMargin=0.75*inch,
                           rightMargin=0.75*inch)
    
    # Define styles
    styles = getSampleStyleSheet()
    story = []
    
    # Add title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Parse markdown and build story
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Main heading
        if line.startswith('# ') and not line.startswith('## '):
            title = line[2:].strip()
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 0.2*inch))
        
        # Heading 2
        elif line.startswith('## '):
            text = line[3:].strip()
            heading_style = ParagraphStyle(
                'CustomHeading2',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#34495e'),
                spaceAfter=12,
                fontName='Helvetica-Bold'
            )
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph(text, heading_style))
        
        # Heading 3
        elif line.startswith('### '):
            text = line[4:].strip()
            heading_style = ParagraphStyle(
                'CustomHeading3',
                parent=styles['Heading3'],
                fontSize=12,
                textColor=colors.HexColor('#7f8c8d'),
                spaceAfter=10,
                fontName='Helvetica-Bold'
            )
            story.append(Spacer(1, 0.05*inch))
            story.append(Paragraph(text, heading_style))
        
        # Regular paragraphs
        elif line and not line.startswith('-') and not line.startswith('|') and not line.startswith('`'):
            body_style = styles['BodyText']
            body_style.fontSize = 11
            story.append(Paragraph(line, body_style))
        
        # Page break
        elif line.strip() == '---':
            story.append(PageBreak())
        
        # Lists
        elif line.startswith('-'):
            text = line[2:].strip()
            list_style = ParagraphStyle(
                'ListItem',
                parent=styles['Normal'],
                leftIndent=20,
                fontSize=11
            )
            story.append(Paragraph('• ' + text, list_style))
        
        # Add spacing
        elif not line:
            story.append(Spacer(1, 0.1*inch))
        
        i += 1
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF generated: {pdf_file}")

if __name__ == '__main__':
    print("Converting backend black-box design to PDF...")
    generate_pdf('docs/BLACK_BOX_TEST_DESIGN.md', 'docs/BLACK_BOX_TEST_DESIGN.pdf')
    print("✅ Successfully created: docs/BLACK_BOX_TEST_DESIGN.pdf")
