import fitz
from tkinter import Tk, filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import re

headers_to_remove = [
    "Department of Artificial Intelligence and Data Science",
    "Course Code / Name: 23AD1302 / ARTIFICIAL INTELLIGENCE AND EXPERT SYSTEMS",
    "23AD1302 – UNIT I – MCQ – SET",
    "Year / Semester: II / III",
    "Max Time: 30 Mins",
    "Regulation: 2023",
    "Max Marks: 30"
]

def clean_text(text):

    cleaned_lines = []
    for line in text.split('\n'):
        stripped = line.strip()

        if not stripped:
            continue
        if any(header in stripped for header in headers_to_remove):
            continue
        if re.fullmatch(r'CO\d+', stripped):
            continue

        cleaned_lines.append(stripped)

    return '\n'.join(cleaned_lines)

def select_pdf_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select your PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    return file_path

def save_text_as_pdf(pages_text, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    font_size = 9
    line_height = font_size + 3
    margin_top = 40
    margin_bottom = 40
    usable_height = height - margin_top - margin_bottom
    max_lines_per_page = int(usable_height // line_height)

    for page_text in pages_text:
        lines = page_text.split('\n')
        text_obj = c.beginText(40, height - margin_top)
        text_obj.setFont("Helvetica", font_size)
        line_count = 0

        for line in lines:
            if line_count >= max_lines_per_page:
                c.drawText(text_obj)
                c.showPage()
                text_obj = c.beginText(40, height - margin_top)
                text_obj.setFont("Helvetica", font_size)
                line_count = 0

            text_obj.textLine(line)
            line_count += 1

        c.drawText(text_obj)
        c.showPage()

    c.save()

pdf_path = select_pdf_file()
if not pdf_path:
    print("\n❌ No file selected.")
    exit()

try:
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"\nLoaded: {pdf_path}")
    print(f"\nTotal Pages in PDF: {total_pages}")

    num_pages = int(input(f"Enter number of pages to process (max {total_pages}): "))
    if num_pages > total_pages:
        print("\n❌ Entered page count exceeds total pages.")
        exit()

    cleaned_pages = []

    for i in range(num_pages):
        page = doc[i]
        text = page.get_text()
        cleaned = clean_text(text)
        cleaned_pages.append(cleaned)

    output_pdf = pdf_path.replace(".pdf", "_CLEANED.pdf")
    save_text_as_pdf(cleaned_pages, output_pdf)
    print(f"\nCleaned PDF saved as: {output_pdf}")

except Exception as e:
    print("\n❌ Error:", e)
