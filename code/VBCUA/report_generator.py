"""
report_generator.py
--------------------
Generates a structured, downloadable PDF report using ReportLab,
including evaluation metrics, waveform image, and qualitative feedback.
"""

import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)


def generate_pdf_report(concept_name: str, transcript: str,
                         result: dict, waveform_png_bytes: bytes = None) -> bytes:
    """
    Build a PDF report in memory and return the raw PDF bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], fontSize=20, spaceAfter=10
    )
    heading_style = ParagraphStyle(
        "HeadingStyle", parent=styles["Heading2"], spaceBefore=14, spaceAfter=8
    )
    body_style = styles["BodyText"]

    story = []

    # Title
    story.append(Paragraph("Voice-Based Concept Understanding Analyser", title_style))
    story.append(Paragraph(f"Evaluation Report — {concept_name}", styles["Heading3"]))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
    story.append(Spacer(1, 12))

    # Transcript
    story.append(Paragraph("Transcribed Explanation", heading_style))
    story.append(Paragraph(transcript if transcript.strip() else "No speech detected.", body_style))
    story.append(Spacer(1, 8))

    # Waveform image
    if waveform_png_bytes:
        story.append(Paragraph("Waveform Visualization", heading_style))
        img_buffer = io.BytesIO(waveform_png_bytes)
        story.append(Image(img_buffer, width=16 * cm, height=5 * cm))
        story.append(Spacer(1, 8))

    # Metrics table
    story.append(Paragraph("Evaluation Metrics", heading_style))
    table_data = [
        ["Metric", "Value"],
        ["Semantic Similarity (%)", f"{result['semantic_similarity']}"],
        ["Fluency Score (%)", f"{result['fluency_score']}"],
        ["Final Understanding Score (%)", f"{result['final_score']}"],
        ["Classification", result['classification']],
        ["Filler Word Count", f"{result['filler_count']} / {result['total_words']} words"],
        ["Filler Word Ratio (%)", f"{result['filler_ratio']}"],
        ["Pause Ratio (%)", f"{result['pause_ratio']}"],
        ["RMS Energy", f"{result['rms_energy']}"],
    ]
    table = Table(table_data, colWidths=[8 * cm, 8 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4C72B0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    # Feedback
    story.append(Paragraph("Qualitative Feedback", heading_style))
    for point in result.get("feedback", []):
        story.append(Paragraph(f"• {point}", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
