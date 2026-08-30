import io
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def sanitize_text(text: str) -> str:
    """Special characters aur markdown formatting ko clean karta hai"""
    text = text.replace('**', '').replace('###', '').replace('##', '').replace('#', '')
    text = text.replace('₹', 'INR ').replace('$', 'USD ').replace('€', 'EUR ')
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def create_financial_pdf(data: dict, report_text: str) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0F172A')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#64748B')
    )

    header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0284C7'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # 1. Header
    story.append(Paragraph("FINANCIAL RESEARCH &amp; EQUITY REPORT", title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')} | FinAgent AI", subtitle_style))
    story.append(Spacer(1, 10))

    # 2. Company Info Box Table
    comp_name = sanitize_text(f"{data.get('company_name', 'N/A')} ({data.get('symbol', 'N/A')})")
    metrics_line = sanitize_text(f"Price: {data.get('currency', '')} {data.get('current_price', 'N/A')}  |  1D Change: {data.get('1d_change_percent', 0.0)}%  |  P/E: {data.get('pe_ratio', 'N/A')}")
    
    card_data = [
        [Paragraph(f"<b>{comp_name}</b>", body_style)],
        [Paragraph(metrics_line, subtitle_style)]
    ]
    card_table = Table(card_data, colWidths=[520])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(card_table)
    story.append(Spacer(1, 14))

    # 3. Report Content
    cleaned = sanitize_text(report_text)
    for line in cleaned.split('\n'):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 4))
            continue
        
        # Headers recognition
        if any(line.startswith(prefix) for prefix in ['1.', '2.', '3.', '4.', 'Bull Case', 'Bear Case', 'Final Verdict', 'Key Metrics', 'News &amp; Sentiment', 'News & Sentiment']):
            story.append(Paragraph(line, header_style))
        else:
            story.append(Paragraph(line, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()