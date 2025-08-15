from format import SuperclaimResponse, SubclaimResponse

# to fetch API keys:
import os 
from dotenv import load_dotenv 
from agent import OverallState, SegmentState
from prompts import superclaim_prompt, subclaim_prompt

# for calling LLMs & abstracting LLM input / output logic:
from langchain_openai import ChatOpenAI
from openai import OpenAI 
from pydantic import BaseModel, Field 

# initialize AI model
api_key = os.getenv("OPENAI_API_KEY") #TODO: use this.

# Node definitions:
def seg_by_superclaim(state: OverallState, article_string): 
    "Give AI entire article text to segment by theme; AI emits a stream of JSONs of {text segment, metaclaim}."

    prompt = superclaim_prompt.format(input=article_string) #TODO: codebook for metaclaims (highest level) isn't imported yet; implement a way.
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Bind schema to model
    schema = SuperclaimResponse # dictionary of superclaim, text
    model_with_tools = model.bind_tools([SuperclaimResponse])
    response = model_with_tools.invoke(superclaim_prompt)
    # get this as a dict.
    # send elements of list as JSONs

def seg_by_subclaims(state: SegmentState): # TODO: figure out output
    "Give AI a JSON of {text segment, 1 metaclaim wrapped in list}. AI evaluates list of child claims & selects appropriate subclaim - & subsubclaim, if relevant. Claims are appended in order to our list."
    # TODO: give AI a list of child subclaims connected to parent superclaim. AI chooses a subclaim, & then a sub-subclaim if relevant.
    # TODO: AI then appends these child claims to the list of claims: list[str]
    # TODO: use json mode.
    return #{key, updated_val}

def aggregate_jsons(state: SegmentState):
    "Node aggregates a stream of SegmentState & updates OverallState."
    return {OverallState["article_segments"], ...} # TODO: one line of code aggregating segmentstates thru appending or overwriting list[...]
