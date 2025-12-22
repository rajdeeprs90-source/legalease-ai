from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(results, output_path):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []

    elements.append(Paragraph("LegalEase AI – Risk Analysis Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    for idx, item in enumerate(results, 1):
        elements.append(Paragraph(f"<b>Clause {idx}</b>", styles["Heading3"]))
        elements.append(Paragraph(item["clause"], styles["Normal"]))
        elements.append(Spacer(1, 6))

        elements.append(Paragraph(f"<b>Risk Level:</b> {item['risk_level']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Explanation:</b> {item['plain_english']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Justification:</b> {item['risk_justification']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Safer Wording:</b> {item['safer_wording']}", styles["Normal"]))
        elements.append(Spacer(1, 12))

    doc.build(elements)
