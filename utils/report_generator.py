from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def generate_pdf_report(query, result, filename="security_report.pdf"):

    file_path = os.path.join("static", filename)
    c = canvas.Canvas(file_path, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "SQL Injection Security Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Query: {query}")
    c.drawString(50, 700, f"Risk Level: {result['risk']}")
    c.drawString(50, 680, f"Score: {result['score']}")

    c.drawString(50, 650, "Findings:")

    y = 630

    for item in result.get("explanations", []):
        c.drawString(60, y, f"- {item}")
        y -= 20

    c.drawString(50, 580, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.save()

    return file_path