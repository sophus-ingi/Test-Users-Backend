#!/usr/bin/env python
"""Generate PDF from frontend black-box design."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

md_file = r'C:\Users\Aku-1\frontendtest\Test-Users-Frontend\docs\BLACK_BOX_TEST_DESIGN.md'
pdf_file = 'docs/FRONTEND_BLACK_BOX_TEST_DESIGN.pdf'

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

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#2c3e50'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

# Parse markdown
lines = content.split('\n')
for line in lines:
    line_stripped = line.strip()
    
    # Main heading
    if line_stripped.startswith('# ') and not line_stripped.startswith('## '):
        title = line_stripped[2:].strip()
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Sub headings
    elif line_stripped.startswith('## '):
        heading_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(line_stripped[3:].strip(), heading_style))
    
    elif line_stripped.startswith('### '):
        heading_style = ParagraphStyle(
            'CustomHeading3',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )
        story.append(Spacer(1, 0.05*inch))
        story.append(Paragraph(line_stripped[4:].strip(), heading_style))
    
    # Regular paragraphs
    elif line_stripped and not line_stripped.startswith('-') and not line_stripped.startswith('|'):
        body_style = styles['BodyText']
        body_style.fontSize = 11
        story.append(Paragraph(line_stripped, body_style))
    
    # Lists
    elif line_stripped.startswith('-'):
        list_style = ParagraphStyle('ListItem', parent=styles['Normal'], leftIndent=20, fontSize=11)
        story.append(Paragraph('• ' + line_stripped[2:].strip(), list_style))
    
    # Spacing
    elif not line_stripped:
        story.append(Spacer(1, 0.1*inch))

doc.build(story)
print(f"✅ Frontend black-box design PDF created: {pdf_file}")
