import pandas as pd
import pymupdf
import argparse
import json

# SPECIFICATIONS:
# IN: CSV
in_csv_path = "../data/sample.csv"
df = pd.read_csv(in_csv_path)

# PROCESSING: 
df = df[['Content_Files', 'Attachment_Files']]
# print(df)

# NOTE: head is just to limit for testing.
for row in df.head(10).itertuples():
    print(row)

def extract(pdf_path):
    # Iterate through PDF until end of article, then put entire article text into title_text_dict, then continue iterating thru PDF.
    doc = pymupdf.open(pdf_path)
    acc = ""
    peek = "print debugging var"
    for page in doc:
        text = page.get_text()
        acc += str(text) # NOTE: get_text doesn't always return get_text()
    return acc

