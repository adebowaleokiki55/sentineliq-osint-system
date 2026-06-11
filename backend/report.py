from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, filename="report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("OSINT Investigation Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Score: {data['score']}", styles["Normal"]))
    content.append(Paragraph(f"Verdict: {data['label']}", styles["Normal"]))

    content.append(Spacer(1, 12))

    content.append(Paragraph("Evidence:", styles["Heading2"]))

    for ev in data.get("evidence", []):
        content.append(Paragraph(ev["title"], styles["Normal"]))
        content.append(Paragraph(ev["url"], styles["Normal"]))
        content.append(Spacer(1, 8))

    doc.build(content)

    return filename