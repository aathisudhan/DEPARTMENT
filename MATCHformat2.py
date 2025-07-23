import fitz  # PyMuPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def clean_and_format_text(raw_text):
    if "Q" in raw_text:
        raw_text = raw_text[raw_text.index("Q"):]  # Start from first 'Q'

    lines = raw_text.splitlines()
    cleaned_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Remove "CO1" and strip
        line = line.replace("CO1", "").strip()

        # Remove the line before any "Answer:"
        if "Answer:" in line and len(cleaned_lines) > 0:
            cleaned_lines.pop()

        if line:
            cleaned_lines.append(line)
        i += 1

    return "\n".join(cleaned_lines)

def write_cleaned_pdf(output_path, cleaned_text, font_size=10):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    x, y = 50, height - 50
    line_spacing = font_size + 2

    c.setFont("Helvetica", font_size)

    for line in cleaned_text.split("\n"):
        if y < 70:
            c.showPage()
            c.setFont("Helvetica", font_size)
            y = height - 50
        c.drawString(x, y, line)
        y -= line_spacing

    c.save()

# === MAIN ===
input_pdf_path = "MATCH_CLEANED.pdf"
output_pdf_path = "CLEANED_OUTPUT.pdf"

raw_text = extract_text_from_pdf(input_pdf_path)
cleaned_text = clean_and_format_text(raw_text)
write_cleaned_pdf(output_pdf_path, cleaned_text, font_size=10)

print(f"✅ Cleaned PDF saved as: {output_pdf_path}")
