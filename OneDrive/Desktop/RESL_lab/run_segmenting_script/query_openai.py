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

## DOCUMENTATION: ##
# script intakes 1 article and outputs the same article, segmented by theme using OpenAI prompting. (Format: CSV of theme, text)
# if OpenAI prompting errors, script outputs 1-line CSV of "QUERYING ERROR [optional explanation]" and original text.

#### parsing argument (article text - title ignored for now): ####
parser = argparse.ArgumentParser(description = "Classify given article according to given codebook.")
parser.add_argument("article_text", type=str)
args = parser.parse_args()
article_text = args[0]

#### Parameters for querying OpenAI: ####
# our prompt:
codebook = "path_here"
our_prompt = f"""Segment the given article by theme, according to the given codebook. The codebook text is given after this prompt, & the article text is given after the codebook.

Reply ONLY with a JSON object with theme as first column & associated text as second column. The order of text should not be changed, and no text should be ommitted. Mark metadata such as article title & copyright information as "METADATA".

If any error occurs that prevents these instructions from being followed, please respond with "ERROR: " + a 1-sentence explanation of the error.

codebook:
{codebook}

ARTICLE:
{article_text}
"""

# creating our client w/ a locally saved key:
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Function to query OpenAI & handle errors:
def query_openai(prompt=our_prompt, retry_delay=2, max_retries=5):

    for attempt in range(max_retries):
        try:
            # Make the API call to OpenAI
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0  # Use 0 temperature for more consistent results
            )
            output = response.choices[0].message.content
            print(f"Output: \n", file=sys.stderr)
            print(output, file=sys.stderr)
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
            # TODO: Check that JSON format is correct.


### Finally: Call OpenAI with our prompt ###
ChatCompletion_object = query_openai()
cleaned_output = ChatCompletion_object
# TODO: clean the above as necessary - we should return a string representing a JSON, which we jsondump into an actual json.
# make error checking as minimal as possible - just put it in the right places.

