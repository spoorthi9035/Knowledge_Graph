from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_document(content, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, "Knowledge Graph Query Result")
    c.drawString(100, height - 120, content)
    c.save()
