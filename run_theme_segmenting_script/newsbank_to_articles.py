import pymupdf
import argparse
import json

## This script extracts articles from Newsbank PDF bundles as properly-formatted plaintext. ##
## Input is PDF path, output is JSON object of plaintext articles.
## To make sure dependencies work, run this script in the venv!     command: source .venv/bin/activate

## Test command:
## python3 extract_txt_from_newsbankpdf.py "/Users/rnzha/Documents/RESL_lab/Data_newspapers_sample/bear creek/NewsBank Multiple Articles (35).pdf"

# We store articles during intermediate processing in a dictionary where key = article name and value = article content.
title_text_dict = {}

## Take in PDF path ##
parser = argparse.ArgumentParser(description="take in path to Newsbank PDF so we can extract individual articles.")
parser.add_argument("pdf_path", type=str)
args = parser.parse_args()

# Iterate through PDF until end of article, then put entire article text into title_text_dict, then continue iterating thru PDF.
doc = pymupdf.open(args.pdf_path)
acc = ""
peek = "print debugging var"
for page in doc:
    text = page.get_text()
    acc += text
    # At end of each article (i.e. when citation guide shows up), 
    # extract article name (& full citation) from citation guide & add article to dict.
    # Clear accumulator & repeat.
    if "Citation (aglc Style)\n" in text:
        title_citations = text.split("Citation (aglc Style)\n", maxsplit=1)[1]
        just_the_title = title_citations.split("'")[1] # actual title w/o citations or author - used for cleaning text

        # store accumulated text, omitting article title, citation info, & newlines 
        # (...as PDF creates a large amount of arbitrary newlines, & OpenAI is going to re-segment the text for us anyway)
        title_text_dict[title_citations] = acc.split("Contact the writer")[0]\
            .split("Copyright (c)")[0]\
            .replace("\n", " ")\
            .replace(just_the_title, "")
        acc = ""  # Reset accumulator
        title_citations = ""
    else:
        acc += text  # Accumulate text for the last page

output_json = json.dumps(title_text_dict, indent=4)
print(output_json)