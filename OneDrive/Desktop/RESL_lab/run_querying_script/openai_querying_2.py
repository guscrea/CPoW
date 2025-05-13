# Standard library imports for basic functionality
# import csv          # For reading and writing CSV files
import json         # For handling JSON data
import time         # For adding delays between API calls
import os           # For operating system related operations
import random       # For generating random numbers
import logging      # For logging program execution and errors
import argparse     # For parsing command line arguments
import sys        # For outputting results to stdout
from openai import OpenAI        # OpenAI API client
from dotenv import load_dotenv   # For loading environment variables from .env file

## NOTE: ##

# This script takes in the following arguments, provided by file_manager.py
# (1) path to codebook
# (2) article title (& citation info)
# (3) article text 

# it outputs a LIST of JSON objects, each corresponding to a code.
# each object contains the following fields: 
# - "code"
# - "quoted_evidence"
# - "opposition_or_support"

# file_manager then takes this list and converts it into CSV rows with the following columns:
# "project_name", "article_title", "code", "quoted_evidence", "opposition_or_support"

# To call this script manually from terminal, make sure you're in run_querying_script directory, then enter:
# python openai_querying_2.py "resources/codebook.txt" "sample_name" "sample_text"

# For debugging: makes entire script return a sample correct output:
testing_in_out = False
sample_results = [
    {"code": "Environmental Impact",
     "quoted_evidence": "Some residents are concerned about the impact on local wildlife", 
     "opposition_or_support": "opposition"}, 
     {"code": "Sustainable Energy", "quoted_evidence": 
      "others see it as a step towards sustainable energy", "opposition_or_support": "support"}
      ]

if testing_in_out:
    sys.stdout.write(json.dumps(sample_results))
    sys.exit()

# Set up logging to track the program's execution
# This will help us understand what's happening and debug any issues
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Take in args from file manager!
parser = argparse.ArgumentParser(description = "Classify given article according to given codebook.")
parser.add_argument("codebook_path", type=str, help="Path to codebook.txt") 
parser.add_argument("article_title", type=str, help="article title") 
parser.add_argument("article_text", type=str, help="article text") 
args = parser.parse_args()

# Verify that the codebook file exists before proceeding
print("Current working directory:", os.getcwd())
print("Attempting to resolve path to codebook:", os.path.abspath(args.codebook_path))

if not os.path.exists(args.codebook_path):
    raise FileNotFoundError(f"Codebook file not found: {args.codebook_path}")

# Load the provided arguments into variables!
with open(args.codebook_path, 'r') as f:
    codebook_text = f.read() # Read the codebook text
article_title = args.article_title
article_text = args.article_text

## Sample correct args, used for debugging:
testing_correct_args = True
if testing_correct_args:
    codebook_text = "Assign codes as you see fit."
    article_title = "Wind Energy Project in the Midwest"
    article_text = "The wind energy project has been met with mixed reactions. Some residents are concerned about the impact on local wildlife, while others see it as a step towards sustainable energy."

print(f"Args received: {codebook_text}, {article_title}, {article_text}")
# TODO: set up openAI client & query.
api_key = "personal api key redacted for safety!" # TODO: replace with a secure method of loading the key
client = OpenAI(api_key=api_key)

def query_openai(prompt, max_retries=5):
    """
    Send a query to OpenAI's API and handle any potential errors or rate limiting.
    
    Args:
        prompt (str): The text prompt to send to OpenAI
        max_retries (int): Maximum number of retry attempts for failed requests
        
    Returns:
        dict: Parsed JSON response from OpenAI, or error information
    """

## NOTE: simplified testing version of this script is in removed_script.py

## EXTENDED QUERYING SCRIPT: ###
    retry_delay = 2  # Initial delay between retries in seconds

    for attempt in range(max_retries):
        try:
            # Make the API call to OpenAI
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0  # Use 0 temperature for more consistent results
            )
            return json.loads(response.choices[0].message.content)

        except json.JSONDecodeError:
            # Handle cases where OpenAI's response isn't valid JSON
            logging.error("Invalid JSON response from OpenAI.")
            return {"code": "Error: invalid JSON", "paragraph_id": "", "quoted_evidence": "", "opposition_or_support": ""}

        except Exception as e:
            if "Rate limit" in str(e):
                # Handle rate limiting by implementing exponential backoff
                wait_time = retry_delay + random.uniform(0, 1)
                logging.warning(f"Rate limit reached. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                retry_delay *= 2  # Double the delay for next potential retry
            elif "openai" in str(e).lower():
                # Handle any other OpenAI-specific errors
                logging.error(f"OpenAI API error: {e}")
                return {"code": "Error: OpenAI API", "paragraph_id": "", "quoted_evidence": "", "opposition_or_support": ""}
            else:
                # Handle any unexpected errors
                logging.error(f"Unexpected error: {e}")
            return {"code": "Unexpected error", "paragraph_id": "", "quoted_evidence": "", "opposition_or_support": ""}
    # If we've exhausted all retries, return an error response
    return {"code": "Error: Max retries exceeded", "paragraph_id": "", "quoted_evidence": "", "opposition_or_support": ""}

# ############# Calling OpenAI API #############
# Construct prompt:
prompt = f"""
You are provided with a codebook and an article that discusses a certain wind energy project.
The article may contain statements of support or opposition to the wind energy project.
Moving through the article paragraph-by-paragraph, use the codebook to classify each paragraph according to the relevant codes.
For each code:
- provide one example of a quote in the same paragraph that represents that code.
- provide the first 5 words and last 5 words of the paragraph as a unique identifier: format = "First five words here...last five words here."

CODEBOOK TEXT: {codebook_text}
ARTICLE TEXT: {article_text}

Please reply with a Python list of JSON objects that includes the following keys exactly:
- "code"
- "paragraph_id"
- "quoted_evidence"
- "opposition_or_support" (this should be "opposition", "support", or "neutral")

Reply with a plain Python list of JSON objects with NO Markdown formatting.
"""

# Call OpenAI API with the constructed prompt
results = query_openai(prompt)

print(str(results)[:500], "...") 

sys.stdout.write(json.dumps(results))

logging.info(f"Processing for {article_title} completed successfully.")


