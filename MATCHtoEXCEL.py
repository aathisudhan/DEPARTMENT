import fitz  # PyMuPDF
import pandas as pd
import re

# === Load PDF ===
doc = fitz.open("CLEANED_OUTPUT.pdf")
text = "\n".join(page.get_text() for page in doc)

# === Split into Questions ===
questions_raw = re.split(r"\nQ\s*\n?", text)
data = []

for q_raw in questions_raw:
    if not q_raw.strip():
        continue

    lines = q_raw.strip().splitlines()
    numbered = []
    lettered = []
    options_block = ""
    answer = ""
    has_question = any(re.match(r"^\d\.", line.strip()) for line in lines)
    
    if not has_question:
        continue  # Skip empty 'Q' section (like first one)

    # Extract parts
    state = "numbered"
    for line in lines:
        if line.strip().startswith("Options:"):
            state = "options"
            options_block += line + "\n"
            continue
        elif line.strip().startswith("Answer:"):
            answer = re.search(r"Answer:\s*\(?([a-d])\)?", line.strip())
            answer = answer.group(1) if answer else ""
            break
        if state == "options":
            options_block += line + "\n"
        elif re.match(r"^\d\.", line.strip()):
            numbered.append(line.strip())
        elif re.match(r"^[a-e]\.", line.strip()):
            lettered.append(line.strip())

    # Clean matching terms
    a_list = [item.partition(".")[2].strip() for item in numbered]
    b_list = [item.partition(".")[2].strip() for item in lettered]
    a_list += [""] * (5 - len(a_list))
    b_list += [""] * (5 - len(b_list))

    # Extract AnswerA1–A4 from Options block (remove a, b, etc.)
    option_contents = re.findall(r"\(?[a-d]\)?\)?\s*(.*?)(?=\([a-d]\)|$)", options_block, re.DOTALL)
    option_contents = [opt.strip().replace("\n", " ") for opt in option_contents]
    option_contents += [""] * (4 - len(option_contents))  # pad to 4

    answer_map = {
        f"AnswerA{i+1}": option_contents[i] for i in range(4)
    }

    # Construct row
    row = {
        "Type": "MATCH_FOLLOWING",
        "Question": f"Match the following:",
        "A1": a_list[0],
        "A2": a_list[1],
        "A3": a_list[2],
        "A4": a_list[3],
        "A5": a_list[4],
        "B1": b_list[0],
        "B2": b_list[1],
        "B3": b_list[2],
        "B4": b_list[3],
        "B5": b_list[4],
        "CorrectOption": answer
    }
    row.update(answer_map)
    data.append(row)

# === Save to Excel ===
df = pd.DataFrame(data)
df.to_excel("formatted_matching_questions.xlsx", index=False)
print("Completed")
