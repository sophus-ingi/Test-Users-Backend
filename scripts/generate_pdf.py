#!/usr/bin/env python
"""Generate PDF from markdown files for black-box test design."""

from weasyprint import HTML
import re

def markdown_to_html(md_file, html_file):
    """Convert markdown to HTML."""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Simple markdown to HTML conversion
    html = md_content
    
    # Headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    
    # Code blocks
    html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # Lists
    html = re.sub(r'^\- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # Paragraphs
    lines = html.split('\n')
    processed = []
    for line in lines:
        if line and not line.startswith('<'):
            processed.append(f'<p>{line}</p>')
        else:
            processed.append(line)
    html = '\n'.join(processed)
    
    # Full HTML structure
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin-top: 40px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-left: 4px solid #3498db; padding-left: 10px; }}
        h3 {{ color: #7f8c8d; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #bdc3c7; padding: 12px; text-align: left; }}
        th {{ background-color: #ecf0f1; font-weight: bold; }}
        code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }}
        pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; font-family: 'Courier New', monospace; }}
        ul, ol {{ margin: 15px 0; padding-left: 20px; }}
        li {{ margin: 8px 0; }}
        p {{ margin: 10px 0; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    return html_file

def html_to_pdf(html_file, pdf_file):
    """Convert HTML to PDF."""
    HTML(filename=html_file).write_pdf(pdf_file)
    print(f"✅ PDF generated: {pdf_file}")

if __name__ == '__main__':
    # Convert backend black-box design
    print("Converting backend black-box design to PDF...")
    html_file = markdown_to_html('docs/BLACK_BOX_TEST_DESIGN.md', 'docs/BLACK_BOX_DESIGN_TEMP.html')
    html_to_pdf(html_file, 'docs/BLACK_BOX_TEST_DESIGN.pdf')
