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

failure_output_rel_path = "output/failure_output.txt"

## NOTE: ##

# This script takes in the following arguments, provided by file_manager.py
# (1) path to codebook
# (2) article title (& citation info)
# (3) article text 

# it outputs a LIST of JSON objects, each corresponding to a code.
# each object contains the following fields: 
# - "paragraph_id" ()
# - "code"
# - "quoted_evidence"
# - "opposition_or_support"

# file_manager then takes this list and converts it into CSV rows with the following columns:
# "project_name", "article_title", "code", "quoted_evidence", "opposition_or_support"

# To call this script manually from terminal, make sure you're in run_querying_script directory, then enter:
# python openai_querying_2.py "resources/codebook.txt" "Noise pollution caused by wind farm" "Residents are worried about noise pollution caused by the wind energy project."

# For debugging: makes entire script return a sample correct output:
testing_in_out = False
sample_results = [
    {
        # data point 1:
        "paragraph_id": "1st 5 words of paragraph...last 5 words of paragraph.",
        "code": "Environmental Impact",
        "quoted_evidence": "Some residents are concerned about the impact on local wildlife", 
        "opposition_or_support": "opposition"
    },
        # data point 2:
    {
        "paragraph_id": "1st 5 words of other paragraph...last 5 words.",
        "code": "Sustainable Energy", 
        "quoted_evidence": "others see it as a step towards sustainable energy", 
        "opposition_or_support": "support"
    }
            ]

if testing_in_out:
    print("\n \n testing input/output between our two scripts: this script is currently hard-coded to pass a valid input into file_manager.py \n \n", file=sys.stderr)
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
print("Current working directory:", os.getcwd(), file=sys.stderr)
print("Attempting to resolve path to codebook:", os.path.abspath(args.codebook_path), file=sys.stderr)

if not os.path.exists(args.codebook_path):
    raise FileNotFoundError(f"Codebook file not found: {args.codebook_path}")

# Load the provided arguments into variables!
with open(args.codebook_path, 'r', encoding="utf-8") as f:
    codebook_text = f.read() # Read the codebook text
article_title = args.article_title
article_text = args.article_text

## Sample correct args, used for debugging:
testing_correct_args = False
if testing_correct_args:
    print("\n \n Testing mode: we're inputting preset valid arguments to check that OpenAI querying works. \n \n", file=sys.stderr)
    codebook_text = "Assign codes as you see fit."
    article_title = "Wind Energy Project in the Midwest"
    article_text = "The wind energy project has been met with mixed reactions. Some residents are concerned about the impact on local wildlife, while others see it as a step towards sustainable energy."

print(f"Args entered into OpenAI (check that codebook text, article title, & article text is correct!): \n {codebook_text}, {article_title}, {article_text} \n", file=sys.stderr)
# TODO: set up openAI client & query.
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") 
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
            output = response.choices[0].message.content
            print(f"success! Output saved as {type(output)} (should be string). Output: \n", file=sys.stderr)
            print(output, file=sys.stderr)
            return output
            
        
        except not isinstance(response.choices[0].message.content, list):
            # Handle cases where OpenAI's response isn't valid list
            logging.error("Invalid list response from OpenAI.")
            with open(failure_output_rel_path, "w") as file:
                print(response, file=sys.stderr)
            return [{"code": "Error: response not in list form", "paragraph_id": "", "quoted_evidence": "", "opposition_or_support": ""}]

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
                with open(failure_output_rel_path, "w") as file:
                    print(response, file=sys.stderr)
                return [{"code": "Error: OpenAI API", "paragraph_id": "", "quoted_evidence": "", "opposition_or_support": ""}]
            else:
                # Handle any unexpected errors
                logging.error(f"Unexpected error: {e}")
                with open(failure_output_rel_path, "w") as file:
                    print(response, file=sys.stderr)
            return [{"code": "Unexpected error", "paragraph_id": "", "quoted_evidence": "", "opposition_or_support": ""}]
    # If we've exhausted all retries, return an error response
    return [{"code": "Error: Max retries exceeded", "paragraph_id": "", "quoted_evidence": "", "opposition_or_support": ""}]


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

Please reply with a list of JSON objects that includes the following keys exactly:
- "paragraph_id"
- "code"
- "quoted_evidence"
- "opposition_or_support" (this should be "opposition", "support", or "neutral")

Reply only with a Python-style list of JSON objects. 
Do not include backslashes, newline characters (\n), 
or wrap the output in a string. 
Do not include the json keyword.
I want the raw list, not its string representation.

example output: {sample_results}
"""

# Call OpenAI API with the constructed prompt

# Pipeline runs correctly when we return a hardcoded list of JSONs. 
# Thus, We MUST return a list of JSONs in our real output.
# Check that this is the case!

ChatCompletion_object = query_openai(prompt)
output_as_string = ChatCompletion_object #.choices[0].message.content
output_as_string = output_as_string.strip().replace("\n", "").replace("json", "")

print(f"OpenAI returned the following: {output_as_string}", file=sys.stderr) 


try:
    import ast
    parsed_data = ast.literal_eval(output_as_string)
    
    # openai sometimes returns list of dicts instead of list of json (ie keys & entries in each object are in single quotes); check that it is one of the two.
    assert isinstance(parsed_data, list), "Expected list or dict from OpenAI"
    assert isinstance(parsed_data[0], dict), "Expected list or dict from OpenAI"
    # parse possible dict:
    json_output = json.dumps(parsed_data)
    sys.stdout.write(json_output)
    logging.info("Successfully parsed and output JSON")


    # # Convert string to Python object (list of dicts, likely)
    # output_as_json = json.loads(output_as_string)

    # # Output clean JSON to stdout for downstream usage
    # sys.stdout.write(json.dumps(output_as_json))
    # logging.info(f"Processing for {article_title} completed.")
except json.JSONDecodeError as e:
    logging.error(f"JSON decode error: {e}")
    sys.stderr.write("FAILED TO PARSE JSON\n")
    sys.stdout.write("[]")  # or raise an error / return empty result


# ChatCompletion(id='chatcmpl-BY1xQcwHTmr0kb1iJeV9Dtl6X9jBp', choices=[Choice(finish_reason='stop', index=0, logprobs=None, 
#                                                                             message=ChatCompletionMessage(content='```python\n[\n    {\n        "code": "concern about impact on wildlife",\n        "paragraph_id": "The wind energy project...impact on local wildlife, while",\n        "quoted_evidence": "Some residents are concerned about the impact on local wildlife",\n        "opposition_or_support": "opposition"\n    },\n    {\n        "code": "step towards sustainable energy",\n        "paragraph_id": "impact on local wildlife, while...step towards sustainable energy.",\n        "quoted_evidence": "others see it as a step towards sustainable energy",\n        "opposition_or_support": "support"\n    }\n]\n```', refusal=None, role='assistant', annotations=[
#                ], audio=None, function_call=None, tool_calls=None))], created=1747450376, model='gpt-4o-2024-08-06', object='chat.completion', service_tier='default', system_fingerprint='fp_90122d973c', usage=CompletionUsage(completion_tokens=128, prompt_tokens=231, total_tokens=359, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))



