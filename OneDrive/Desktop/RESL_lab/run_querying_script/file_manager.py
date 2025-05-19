import subprocess # for shell scripting
import os # for shell scripting
import pymupdf
import csv
from dataclasses import dataclass
import json
from pathlib import Path
import datetime

@dataclass
class article_data:
    project_name: str
    article_text: str


########## IMPORTANT: ####################

print("IMPORTANT: \n This script is meant to be run while we're in the run_querying_script directory!")

## Set filepaths with run_querying_script as home directory:
# (modify this if directory is rearranged!)

# Note: I've hardcoded some paths to help w/ debugging, but they can be made relative easily.

script_directory = "c:/Users/rnzha/OneDrive/Desktop/RESL_lab/run_querying_script"
codebook_rel_path = "resources/codebook.txt"
news_data_rel_path = "../Data_newspapers_sample" 
output_csv_rel_path = """C:/Users/rnzha/OneDrive/Desktop/RESL_lab/run_querying_script/output/output.csv"""
failure_output_rel_path = """C:/Users/rnzha/OneDrive/Desktop/RESL_lab/run_querying_script/output/failure_output.txt"""

###############################################

# extract folder names as list; each folder is named for its corresponding plant.
result = subprocess.run(['ls', news_data_rel_path], capture_output = True, text=True)
folders_list = result.stdout.strip().split('\n')

print(f" \n ALL PLANTS FOUND: {folders_list} \n ")
# TODO: print error & return if folder empty

# Extract articles from each folder:
for plant_folder in folders_list:
    os.chdir('../Data_newspapers_sample')
    print(f"currently iterating through folder for: {plant_folder}")
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

    print(f"all {len(title_text_dict.keys())} articles found for plant {plant_folder}: \n {list(title_text_dict.keys())} \n")
    print("Now iterating through these articles, passing each into OpenAI.")
    ### Time to enter each article into our OpenAI querier script! ##
    implemented = True # set as false to test article "unzipping" part of script
    if implemented:
        for key in title_text_dict:
            article_name = key
            value = title_text_dict[key]
            project_name = value.project_name
            article_text = value.article_text
            os.chdir(script_directory) # FOR DEBUGGING ONLY - checks that sub.run doens't error bc of wrong directory
            # Querying OpenAI with our custom script:
            output_as_CompletedProcess = subprocess.run(
                ['python', 'openai_querying_2.py', codebook_rel_path, article_name, article_text],
                cwd = '../run_querying_script', # this should error if we're in the wrong directory
                capture_output=True,
                text=True,
                check=True
                )
            print(f"""output from OpenAI for article "{article_name} for {project_name}...": \n""", output_as_CompletedProcess.stdout, "\n \n")

    # We should return a list of JSON objects, one for each article.
    # The fields of each object are: code, paragraph_id, quoted_evidence, opposition_or_support

            output_as_JSONs = json.loads(output_as_CompletedProcess.stdout.strip())

            # 1 - Check if output is a list
            print("Checking format of the output of the above article...")
            if isinstance(output_as_JSONs, list):
                # 2 - Check if first item is a JSON object (actually, a `dict`)
                if isinstance(output_as_JSONs[0], dict):
                    print("Output is a list of JSONs!")
                else:
                    error_msg = "❌ Output is not list of JSONs!"
            else:
                error_msg = "❌ Output is not a list!"

            # If we had an error, handle it
            if 'error_msg' in locals():
                with open(failure_output_rel_path, "w") as file:
                    print(output_as_JSONs, file=file)
                raise Exception(f"""{error_msg}
                    \nRaw output saved in failure_output.txt.
                    \n{output_as_JSONs}""")


            # We iterate through each object and add it as a CSV entry in our output file:
            with open(output_csv_rel_path, 'a', newline='') as fd:
                writer = csv.writer(fd)
                # write header if CSV is empty:
                if os.stat(output_csv_rel_path).st_size == 0:
                    print("csv file empty: writing in row names")
                    writer.writerow(["wind project name", 
                                    "article title", 
                                    "paragraph ID",
                                    "code", 
                                    "quoted evidence",
                                    "opposition or support"])
                
                for entry in output_as_JSONs:
                    print(f"entry parsed right now: {entry}")
                    try:
                        writer.writerow([
                            project_name, 
                            article_name, 
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
                        
            print(f"output.csv successfully written into for article {article_name}!")



## FINALLY... rename output.csv so we have a unique timestamped output file; then clear output.csv ##

t = datetime.datetime.now()
timestamp = f"{t.year}-{t.month}-{t.day}_{t.hour}-{t.minute}"

print(f"Attempting to port output into new file with timestamp {timestamp}")
try:
    os.rename(f"{script_directory}/output/output.csv", f"{script_directory}/output/output_{timestamp}.csv")
    f = open(f"{script_directory}/output/output.csv", "x")
    print("success!")
except:
    print("Porting failed; output still saved in output.csv")

