#!/usr/bin/env python3
"""Convert markdown to PDF for delivery."""

import markdown2
from weasyprint import HTML, CSS
from pathlib import Path
import tempfile

def convert_md_to_pdf(md_file, pdf_file):
    """Convert markdown to PDF using weasyprint."""
    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks'])
    
    # Wrap with HTML/CSS for better formatting
    full_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
                color: #333;
            }}
            h1 {{
                color: #0066cc;
                border-bottom: 3px solid #0066cc;
                padding-bottom: 10px;
                page-break-after: avoid;
            }}
            h2 {{
                color: #0066cc;
                margin-top: 30px;
                page-break-after: avoid;
            }}
            h3 {{
                color: #444;
                page-break-after: avoid;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 15px;
                border-left: 4px solid #0066cc;
                overflow-x: auto;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f4f4f4;
                font-weight: bold;
            }}
            ul, ol {{
                margin: 10px 0;
            }}
            li {{
                margin: 5px 0;
            }}
            .page-break {{
                page-break-before: always;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert to PDF
    HTML(string=full_html).write_pdf(pdf_file)
    print(f"✅ Converted: {md_file} → {pdf_file}")

if __name__ == '__main__':
    # Convert BLACK_BOX_TEST_DESIGN.md to PDF
    convert_md_to_pdf(
        'docs/BLACK_BOX_TEST_DESIGN.md',
        'docs/BLACK_BOX_TEST_DESIGN.pdf'
    )
    
    print("\n📄 PDF files created successfully!")
