import pandas as pd
import pymupdf
import argparse
import json
import requests
import tempfile
import os

## TODO: 
# figure out way to manage multiple PDFs per entry. Either put in same cell (loss of info) or add max 10 columns (unwieldy). HACK SOLUTION: same cell with very distinc headers per PDF.

# then: make results presentable.

def extract(pdf_path):
    doc = pymupdf.open(pdf_path)
    acc = ""
    for page in doc:
        text = page.get_text()
        acc += str(text) # NOTE: get_text doesn't always return get_text()
    return acc

# IN: CSV
in_csv_path = "../data/sample.csv"
df = pd.read_csv(in_csv_path)

# PROCESSING: 
df = df[['Content_Files', 'Attachment_Files']]
print("DF before extract: \n")
print(df.head(3))


# NOTE: head is just to limit for testing.
for row in df.itertuples():
    print("iteration started")
    for col_name in ["Content_Files", "Attachment_Files"]:
        pdf_paths = getattr(row, col_name, None)
        if pdf_paths is not None:
            pdf_paths = str(pdf_paths).split(',')
            pdf_path = pdf_paths[0]  # TODO: change to  unpacking multiple

            pdf_acc = ""
            for idx, pdf_path in enumerate(pdf_paths):
                pdf_acc += f"\n \n DOCUMENT #{idx}; LINK:{pdf_path} \n"
                try:
                    # Download to a temporary file
                    response = requests.get(pdf_path, timeout=10)
                    response.raise_for_status() # Errors if download failed
                    # Write pdf content to temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(response.content) # Write PDF content to temp file
                        local_pdf = tmp_file.name # Get the temp file path
                    
                    # Extract text from the downloaded PDF
                    pdf_acc += extract(local_pdf)

                except Exception as e:
                    print(f"Error processing {pdf_path}: {e}")
                    pdf_acc += "No text found."

            df.at[row.Index, f'{col_name}_extracted'] = pdf_acc 

print(df)

df.to_csv('out.csv', index=False)