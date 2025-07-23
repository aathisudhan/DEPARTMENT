import fitz  # PyMuPDF
import re

# === STEP 1: Load the PDF ===
input_file = "UNIT 1 AIES.pdf"  # Replace with your actual file name
doc = fitz.open(input_file)

# === STEP 2: Extract all text and split by lines ===
full_text = "\n".join(page.get_text() for page in doc)
doc.close()
lines = full_text.splitlines()

# === STEP 3: Extract only complete blocks (Column A to Answer:) ===
blocks = []
collecting = False
current_block = []

for line in lines:
    # If we hit a new "Column A" while collecting and no Answer was found — discard
    if "Column A" in line:
        if collecting and not any("Answer:" in l for l in current_block):
            # Discard the incomplete block
            current_block = []
        collecting = True
        current_block = [line]
        continue

    if collecting:
        current_block.append(line)

        # If we reach an Answer line → finalize this block
        if re.search(r'Answer:\s*\([a-dA-D]\)', line):
            blocks.append("\n".join(current_block))
            collecting = False
            current_block = []

# === STEP 4: Write only complete blocks to a new PDF ===
output_file = "Match_Only_Extracted.pdf"
new_doc = fitz.open()

if blocks:
    for block in blocks:
        page = new_doc.new_page()
        page.insert_text((72, 72), block.strip(), fontsize=11)

    new_doc.save(output_file)
    new_doc.close()
    print(f"\n✅ Extracted {len(blocks)} complete match blocks into: {output_file}")
else:
    print("⚠️ No complete match-the-following blocks found.")
