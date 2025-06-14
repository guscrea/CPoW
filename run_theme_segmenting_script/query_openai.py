# TODO: clean imports formatting.
import random # for handling rate limiting 
import time # for handling rate limiting
import csv # for writing into CSV
import json # for handling JSON data
import argparse # to take in args
import logging # to log errors
from openai import OpenAI # to query OpenAI
from dotenv import load_dotenv # for saving OpenAI key locally
import sys  # for outputting error msgs & results to stdout
import os # to access environment variables

## NOTES: ##
# script intakes 1 article and outputs the same article, segmented by theme using OpenAI prompting. (Format: CSV of theme, text)
# if OpenAI prompting errors, script outputs 1-line CSV of "QUERYING ERROR [optional explanation]" and original text.

# Set up logging to track the program's execution
# This will help us understand what's happening and debug any issues
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

### QUERYING PARAMETERS: ###
# Parsing arguments (article text - title ignored for now): #
parser = argparse.ArgumentParser(description = "The given article is segmented by theme according to our codebook.")
parser.add_argument("article_text", type=str)
args = parser.parse_args()
article_text = args[0]

# Reading codebook: 
with open('themes_examples_removed.txt') as f:
    codebook = f.readlines()
    f.close()

acc = ""
for str in codebook: # turning list of strings to string.
     acc += str
codebook = acc

# Our prompt:
our_prompt = f"""Segment the given article by theme, according to the given codebook. The codebook text is given after this prompt, & the article text is given after the codebook.

Reply ONLY with a JSON object with theme as first column & associated text as second column. The order of text should not be changed, and no text should be ommitted.

If an error occurs that prevents these instructions from being followed, please respond NOT with a JSON object, but with a string starting with "ERROR:" and consisting of a 1-sentence error message. 

------ CODEBOOK: -----
{codebook}
------ END OF CODEBOOK ----


----- ARTICLE: -----
{article_text}
----- END OF ARTICLE -----
"""

# Sanity check:
logging.info(f"Preview of codebook provided: {codebook[:100]}")
logging.info(f"Preview of article provided: {article_text[:100]}")
                
# creating our client w/ a locally saved key:
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Function to query OpenAI & handle errors:
def query_openai(prompt=our_prompt, retry_delay=2, max_retries=5):
    ''' Outputs string representation of list-of-JSONs upon success;
     outputs string starting with "ERROR:" upon failure. 
    (fields of each JSON: [theme], [relevant segment of text]) 
    '''

    for attempt in range(max_retries):
        try:
            # Make the API call to OpenAI
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0  # Use 0 temperature for more consistent results
            )
            # Retrieve output as string:
            output = response.choices[0].message.content
            logging.info(f"OpenAI's putput as string: \n {output} \n")
            return output
        except Exception as e:
            if "Rate limit" in str(e):
                    # Handle rate limiting by implementing exponential backoff
                    wait_time = retry_delay + random.uniform(0, 1)
                    logging.warning(f"Rate limit reached. Retrying in {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                    retry_delay *= 2  # Double the delay for next potential retry
            else:
                # Handles other errors by logging them in theme column w/ full article text
                logging.warning(f"Error message from OpenAI: {str(e)}")
                return {f"Error: {str(e)}": article_text} 


### Finally: Call OpenAI with our prompt ###
# (This should be a string, as our querying function outputs the "message" field from the ChatCompletion object)
output_string = query_openai()
logging.info(f"OpenAI's response, which should be a string: {output_string}")

# Format the output as JSON, w/ consistent error formatting:
if "error:" in output_string.lower()[:100]:
     print({
          f"Received the following error string instead of JSON: {output_string}":article_text
          })
else:
    try:
        cleaned_output_string = output_string.strip().replace("\n", "").replace("json", "")
        print(
             json.dumps(cleaned_output_string))
    except:
         print(
     print({
          f"Unexpected output: {output_string}":article_text
          })              
         )

# TODO: clean the above as necessary - we should return a string representing a JSON, which we jsondump into an actual json.
# make error checking as minimal as possible - just put it in the right places.

