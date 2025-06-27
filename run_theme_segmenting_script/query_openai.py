# TODO: clean imports formatting.
import random # for handling rate limiting 
import time # for handling rate limiting
import json # for handling JSON data
import argparse # to take in args
import logging # to log errors
from openai import OpenAI # to query OpenAI
from dotenv import load_dotenv # for saving OpenAI key locally
import sys  # for outputting error msgs & results to stdout
import os # to access environment variables

## DOC: ##
# This script intakes 1 article and outputs the same article, segmented by theme using OpenAI prompting. (Format: CSV of theme, text)
# if OpenAI prompting errors, script outputs 1-line CSV of "QUERYING ERROR [optional explanation]" and original text.

# To try running it:
# python3 query_openai.py "$(cat testing/sample_article.txt)" > querying_test_output.json

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
article_text = args.article_text

# Reading codebook: 
with open('codebook_examples_removed.txt') as f:
    codebook = f.readlines()
    f.close()

acc = ""
for str in codebook: # turning list of strings to string.
     acc += str
codebook = acc

# Our prompt:

our_prompt = f"""
You are given an article about a wind energy development project that has received some amount of opposition.

Your job is to segment the given article by theme(s), according to the given codebook. The codebook text is given after this prompt, & the article text is given after the codebook.

Reply ONLY with a JSON object with 6 columns: 

1. themes - All the themes that apply to the passage 

2. text - Associated text 

3. wind_energy_reference - Boolean that is TRUE when the passage DIRECTLY refers to the wind turbines or planned development in question.

4. relevance_score - see scoring methodology below.

Scoring methodology for relevance score (0.0-1.0): Calculate this score based on the density and explicitness of terms and concepts related to the themes you applied. A higher score indicates more significant discussion of that issue in the passage.
0.0 - Always default to 0 if direct_reference is FALSE.
0.0 - 0.1: No mention or extremely tangential, fleeting mention.
0.2 - 0.4: Minimal mention, perhaps a single keyword or a very brief, indirect reference. Does not fully meet the framework's detailed criteria.
0.5 - 0.7: Moderate discussion, with several keywords or direct phrases aligning with the framework, but perhaps not the primary focus of the post.
0.8 - 1.0: Strong discussion, with frequent keywords, phrases, and conceptual alignment, indicating a central theme or significant focus of the post. 

5. sentiment_score - see scoring methodology below.

Scoring methodology for sentiment score (-1.0 - 1.0): 
Does the passage discuss support or opposition towards the wind energy project? A negative score indicates opposition, while a positive score indicates support.

-1.0 to -0.7 (Strong Opposition)
Clear, intense opposition.
Language is emotionally charged, negative, or accusatory.
Use of absolute or categorical terms (e.g., "disaster," "unacceptable," "ruin the environment").
Explicit statements rejecting the project or calling for its cancellation.
Example: "This project is a complete disaster and must be stopped immediately."

-0.6 to -0.3 (Moderate Opposition)
Criticism or opposition, but less extreme.
Concerns are raised with some justification or rationale.
May acknowledge potential benefits but argue they’re outweighed by drawbacks.
Example: "While renewable energy is important, this wind farm could harm local wildlife and hurt tourism."

-0.2 to 0.0 (Mild Opposition or Neutral-Negative)
Minor objections or skeptical tone without strong wording.
Criticism may be implied or indirect.
Could reflect doubt, uncertainty, or slight disapproval.
Example: "Some people worry about how the turbines might affect bird populations."

0.0 to 0.2 (Neutral to Mild Support)
Slightly positive or neutral stance.
Mentions potential benefits but without strong endorsement.
May present both pros and cons in a balanced way.
Example: "The project has some environmental benefits, but it also needs careful implementation."

0.3 to 0.6 (Moderate Support)
Supportive but not passionately so.
Acknowledges trade-offs but ultimately views the project positively.
Tone is constructive, with some optimism or approval.
Example: "Wind energy is a step in the right direction, even if there are a few local concerns to address."

0.7 to 1.0 (Strong Support)
Clear and enthusiastic support.
Uses highly positive, affirming, or motivational language.
May advocate for expansion or express pride in the project.
Example: "This wind energy project is a fantastic initiative that shows real environmental leadership."

--

Please make sure NOT to segment the text in a way that allows any sentence to appear more than once. Please make sure your response contains ALL the text in the article - not a single word should be ommitted.

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
    ''' Outputs string representation of a JSON array upon success;
     outputs string starting with "ERROR:" upon failure. 
    (fields of each JSON: [theme], [relevant segment of text], [is windmill mentioned explicitly?]) 
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
            logging.info(f"OpenAI's output as string: \n {output} \n")
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
# (output should be a string, as our querying function outputs the "message" field from the ChatCompletion object)
output_string = query_openai()
logging.info(f"OpenAI's response, which should be a string: {output_string}")

# Format the output as JSON array, w/ consistent error formatting:
if "error:" in output_string.lower()[:100]:
     logging.error("OpenAI's output contained ERROR - program assumes it is an error message.")
     print({
          f"Received the following error string instead of JSON: {output_string}":article_text
          })
else:
    try:
        cleaned_output_string = output_string.strip().replace("\n", "").replace("json", "").replace("```", "")
        json_output = json.dumps(cleaned_output_string)
        sys.stdout.write(json_output)
        logging.info("Output is parsable by json.dumps - it should be a working JSON.")

    except:
         print(
              {f"Wholly unexpected output: {output_string}":article_text})
         logging.info("OpenAI's output was neither a recognized error message or a correct output.")
         

# TODO: clean the above as necessary - we should return a string representing a JSON array, which we jsondump into an actual json array.
# make error checking as minimal as possible - just put it in the right places.

