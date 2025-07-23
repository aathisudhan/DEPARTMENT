import fitz  # PyMuPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def extract_clean_blocks(text):
    lines = text.splitlines()
    questions = []
    current = []
    for line in lines:
        if line.strip().startswith("1."):
            if current:
                questions.append("\n".join(current))
                current = []
        current.append(line)
    if current:
        questions.append("\n".join(current))
    return questions

def reformat_question_block(raw_text, q_number):
    import re
    lines = [line.strip() for line in raw_text.strip().split("\n") if line.strip()]
    full_text = " ".join(lines)

    a_side = re.findall(r'(\d\..*?)(?=\s+\w\.)', full_text)
    b_side = re.findall(r'([a-e]\..*?)(?=\s+\d\.|\s+Options:|\s+Answer:)', full_text)
    options = re.findall(r'([a-d]\))\s*(.*?)(?=\s+[a-d]\)|\s+Answer:|$)', full_text)
    answer_match = re.search(r'Answer:\s*\(?([a-d])\)?', full_text)

    formatted = f"Q\n"
    for i, item in enumerate(a_side, start=1):
        formatted += f"{item.strip()}\n"
        if i-1 < len(b_side):
            formatted += f"{b_side[i-1].strip()}\n"
    formatted += "Options:\n"
    for opt in options:
        formatted += f"{opt[0]} {opt[1]}\n"
    if answer_match:
        formatted += f"Answer: ({answer_match.group(1)})\n"
    return formatted.strip()

def write_to_pdf(output_path, question_blocks):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    x, y = 50, height - 50

    c.setFont("Helvetica", 9)  # Set smaller font

    for block in question_blocks:
        for line in block.split("\n"):
            if y < 70:
                c.showPage()
                c.setFont("Helvetica", 9)  # Reset font on new page
                y = height - 50
            c.drawString(x, y, line)
            y -= 12  # Line spacing
        y -= 20  # Extra space after each question
    c.save()

# === MAIN LOGIC ===
pdf_path = "Match_Only_Extracted.pdf"  # Input PDF
output_path = "MATCH_CLEANED.pdf"      # Output PDF

doc = fitz.open(pdf_path)
raw_text = "\n".join(page.get_text() for page in doc)

question_chunks = extract_clean_blocks(raw_text)

reformatted_blocks = [
    reformat_question_block(block, idx + 1) for idx, block in enumerate(question_chunks)
]

write_to_pdf(output_path, reformatted_blocks)

print(f"✅ Cleaned PDF saved to: {output_path}")
