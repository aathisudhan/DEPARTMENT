import fitz
import pandas as pd
import re

doc = fitz.open("UNIT 1 AIES_CLEANED.pdf")
text = "\n".join(page.get_text() for page in doc)

text = text.replace("c_opt)", "c)")
text = re.sub(r'\ba\s*[\.\)]', 'a)', text)
text = re.sub(r'\bb\s*[\.\)]', 'b)', text)
text = re.sub(r'\bc\s*[\.\)]', 'c)', text)
text = re.sub(r'\bd\s*[\.\)]', 'd)', text)

pattern = re.compile(
    r"""
    (?P<qno>\d+)\.?\s*
    (?P<question>.*?)
    a\)\s*(?P<opt_a>.+?)\s*
    b\)\s*(?P<opt_b>.+?)\s*
    c\)\s*(?P<opt_c>.+?)\s*
    d\)\s*(?P<opt_d>.+?)\s*
    Answer\s*:\s*(?P<answer>[a-dA-D])
    """,
    re.VERBOSE | re.DOTALL,
)

data = []
for m in pattern.finditer(text):
    question = m.group("question").strip()
    question = re.sub(r'\s*a\)$', '', question)
    data.append([
        m.group("qno").strip(),
        question,
        m.group("opt_a").strip(),
        m.group("opt_b").strip(),
        m.group("opt_c").strip(),
        m.group("opt_d").strip(),
        m.group("answer").strip().lower(),
    ])


df = pd.DataFrame(data, columns=["Q.No", "Question", "Option A", "Option B", "Option C", "Option D", "Answer"])
df.to_excel("mcq_extracted.xlsx", index=False)

print("Extraction complete. Saved as: mcq_extracted.xlsx")
