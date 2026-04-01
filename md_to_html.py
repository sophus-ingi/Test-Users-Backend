#!/usr/bin/env python3
"""Generate printer-friendly HTML from markdown for PDF printing."""

import markdown2
from pathlib import Path

def convert_md_to_printable_html(md_file, html_file):
    """Convert markdown to HTML optimized for printing to PDF."""
    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(
        md_content, 
        extras=['tables', 'fenced-code-blocks', 'break-on-newline']
    )
    
    # Create printer-friendly HTML with CSS for PDF
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Black-Box Test Design</title>
    <style>
        @media print {{
            body {{
                margin: 0;
                padding: 0;
            }}
            h1 {{
                page-break-after: avoid;
            }}
            h2 {{
                page-break-after: avoid;
                margin-top: 30px;
            }}
            table {{
                page-break-inside: avoid;
            }}
            p {{
                page-break-inside: avoid;
            }}
            .page-break {{
                page-break-before: always;
            }}
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.7;
            color: #333;
            background: white;
            padding: 40px;
            max-width: 900px;
            margin: 0 auto;
        }}
        
        h1 {{
            color: #0066cc;
            border-bottom: 4px solid #0066cc;
            padding: 20px 0;
            margin: 40px 0 20px 0;
            font-size: 32px;
            font-weight: 600;
        }}
        
        h2 {{
            color: #0066cc;
            border-bottom: 2px solid #ccc;
            padding: 15px 0 10px 0;
            margin: 35px 0 15px 0;
            font-size: 24px;
            font-weight: 600;
        }}
        
        h3 {{
            color: #444;
            margin: 20px 0 10px 0;
            font-size: 18px;
            font-weight: 600;
        }}
        
        h4 {{
            color: #555;
            margin: 15px 0 8px 0;
            font-size: 16px;
            font-weight: 600;
        }}
        
        p {{
            margin: 12px 0;
            text-align: justify;
        }}
        
        ul, ol {{
            margin: 12px 0 12px 30px;
            padding: 0;
        }}
        
        li {{
            margin: 6px 0;
            line-height: 1.8;
        }}
        
        code {{
            background-color: #f0f0f0;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            color: #333;
        }}
        
        pre {{
            background-color: #f5f5f5;
            border-left: 4px solid #0066cc;
            padding: 15px;
            margin: 15px 0;
            overflow-x: auto;
            border-radius: 4px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 13px;
            line-height: 1.5;
        }}
        
        pre code {{
            background: none;
            padding: 0;
            color: #333;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        th {{
            background-color: #0066cc;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #0066cc;
        }}
        
        td {{
            padding: 10px 12px;
            border: 1px solid #ddd;
            background-color: #fafafa;
        }}
        
        tr:nth-child(even) td {{
            background-color: #f5f5f5;
        }}
        
        tr:hover td {{
            background-color: #e8f4ff;
        }}
        
        hr {{
            border: 0;
            border-top: 2px solid #ddd;
            margin: 30px 0;
        }}
        
        strong {{
            font-weight: 600;
            color: #222;
        }}
        
        em {{
            font-style: italic;
            color: #555;
        }}
        
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #0066cc;
            padding-bottom: 20px;
        }}
        
        .header h1 {{
            margin: 0;
            border: none;
            padding: 0;
        }}
        
        .toc {{
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        blockquote {{
            border-left: 4px solid #0066cc;
            padding-left: 15px;
            margin-left: 0;
            color: #666;
            font-style: italic;
        }}
        
        .note {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 4px;
            padding: 12px;
            margin: 15px 0;
        }}
        
        .warning {{
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            padding: 12px;
            margin: 15px 0;
        }}
        
        .success {{
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 4px;
            padding: 12px;
            margin: 15px 0;
        }}
    </style>
</head>
<body>
    {html_content}
    
    <div style="margin-top: 60px; padding-top: 20px; border-top: 2px solid #ddd; font-size: 12px; color: #888; text-align: center;">
        <p>Generated on: April 1, 2026 | Black-Box Test Case Design | Fake Data Generator API</p>
    </div>
</body>
</html>
"""
    
    # Write HTML file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ Created printer-friendly HTML: {html_file}")
    print(f"📄 To create PDF: Open {html_file} in browser → Print → Save as PDF")

if __name__ == '__main__':
    # Convert BLACK_BOX_TEST_DESIGN.md to HTML
    convert_md_to_printable_html(
        'docs/BLACK_BOX_TEST_DESIGN.md',
        'docs/BLACK_BOX_TEST_DESIGN.html'
    )
    
    print("\n✅ Conversion complete!")
