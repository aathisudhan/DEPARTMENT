import pandas as pd

df = pd.read_excel("mcq_extracted.xlsx")

answer_map = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

new_df = pd.DataFrame({
    "Type": "MCQ",
    "Question": df["Question"],
    "ImageURL": "",
    "Option1": df["Option A"],
    "Option1Img": "",
    "Option2": df["Option B"],
    "Option2Img": "",
    "Option3": df["Option C"],
    "Option3Img": "",
    "Option4": df["Option D"],
    "Option4Img": "",
    "CorrectOption": df["Answer"].str.lower().map(answer_map)
})

new_df.to_excel("converted_mcq_format.xlsx", index=False)

print("Conversion complete. File saved as 'converted_mcq_format.xlsx'")
