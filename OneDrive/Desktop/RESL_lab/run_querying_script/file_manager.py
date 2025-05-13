import subprocess # for shell scripting
import os # for shell scripting
import pymupdf
import csv
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class article_data:
    project_name: str
    article_text: str


########## IMPORTANT: ####################

print("IMPORTANT: \n This script is meant to be run while we're in the run_querying_script directory!")

## Set filepaths with run_querying_script as home directory:
# (modify this if directory is rearranged!)
codebook_rel_path = "resources/codebook.txt"
news_data_rel_path = "../Data_newspaper_sample" 
output_csv_rel_path = "output/output.csv"
failure_output_rel_path = "output/failure_output.txt"
###############################################

# extract folder names as list; each folder is named for its corresponding plant.
result = subprocess.run(['ls'], capture_output = True, text=True)
folders_list = result.stdout.strip().split('\n')
# TODO: print error & return if folder empty

# Extract articles from each folder:
os.chdir('../Data_newspapers_sample')
for plant_folder in folders_list:
    project_name = plant_folder 
    full_path = os.path.abspath(plant_folder)
    pdfs_list = os.listdir(full_path)

    if len(pdfs_list) == 0:
        print(f"{plant_folder} folder contains no articles!")
        # TODO: ENTER ERROR ROW INTO FINAL CSV

    if len(pdfs_list) > 1:
        print(f"{plant_folder} contains more than 1 PDF bundle of articles; our script assumes this doesn't happen.")
   
    if len(pdfs_list) == 1 and "NewsBank" in pdfs_list[0]:
        # directory format appears correct! Time to extract raw text from article bundle.
        article_bundle_pdf = pdfs_list[0]

        # We store articles in a dict. Key = article citation, value = complete text.
        title_text_dict = {}
        
        # temp accumulator stores text so we can enter it into dict after article ends:
        acc = ""

        # Open up our pdf & begin iterating!
        doc = pymupdf.open(f"{full_path}/{article_bundle_pdf}") 
        for page in doc:
            text = page.get_text()
            acc += text
            # At end of each article (i.e. when citation guide shows up), 
            # extract article name from citation guide & add article to list.
            # Next article becomes a new list entry.
            if "Citation (aglc Style)\n" in text:
                split = text.split("Citation (aglc Style)\n", maxsplit=1)
                article_title = split[1].split("\n")[0]
                title_text_dict[article_title] = article_data(project_name, acc)  # Store accumulated text
                acc = ""  # Reset accumulator
            else:
                acc += text  # Accumulate text for the last page

print(f"all {len(title_text_dict.keys())} articles found this time: \n {list(title_text_dict.keys())} \n")
            

### Time to enter each article into our OpenAI querier script! ##
implemented = True
if implemented:
    for key in title_text_dict:
        article_name = key
        value = title_text_dict[key]
        project_name = value.project_name
        article_text = value.article_text

        # Querying OpenAI with our custom script:
        output_as_CompletedProcess = subprocess.run(
            ['python', 'openai_querying_2.py', codebook_rel_path, article_name, article_text],
            capture_output=True,
            text=True,
            check=True
            )
        print("output from OpenAI: \n", output_as_CompletedProcess.stdout[:100], "...")

    # try to parse stdout as JSON    
    try:
        # Parse the clean JSON output
        output_as_JSONs = json.loads(output_as_CompletedProcess.stdout)
    except json.JSONDecodeError as e:
        with open(failure_output_rel_path, "w") as file:
            print(output_as_CompletedProcess.stdout, file=file)
        raise(f"❌ Failed to parse JSON: {e}\nRaw output:\n{output_as_CompletedProcess.stdout[:500]}... (saved in failure_output.txt)")
        
    print(type(output_as_JSONs))

# We should return a list of JSON objects, one for each article.
# The fields of each object are: code, paragraph_id, quoted_evidence, opposition_or_support

# We iterate through each object and add it as a CSV entry in our output file:
with open(output_csv_rel_path, 'a', newline='') as fd:
    writer = csv.writer(fd)
    for entry in output_as_JSONs:
        try:
            writer.writerow([
                project_name, 
                article_title, 
                entry["paragraph_id"],
                entry["code"], 
                entry["quoted_evidence"], 
                entry["opposition_or_support"]
            ])
            # If key missing, output error.
        except KeyError as e:
            missing_key = str(e).strip("'")  # Gets the name of the missing key
            print(f"ERROR: Missing key '{missing_key}' in entry: {entry}")
            writer.writerow([
                project_name,
                article_title,
                f"MISSING_KEY: {missing_key}",
                "ERROR",
                "ERROR",
                "ERROR"
            ])
            
print("output.csv successfully written into!")

# TODO: add new field called "paragraph_id"