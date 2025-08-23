from format import SuperclaimResponse, SubclaimResponse

# to fetch API keys:
import os 
from dotenv import load_dotenv 
from agent import OverallState, SegmentState
from inputs.prompts import superclaim_prompt, subclaim_prompt
from inputs.sample_tree import dummy_taxonomy_tree

# for abstracting LLM input / output logic:
from langgraph.types import Send # for emitting units of data in MapReduce framework.
from langchain_openai import ChatOpenAI
from openai import OpenAI 
from pydantic import BaseModel, Field 

# initialize AI model
api_key = os.getenv("OPENAI_API_KEY") #TODO: use this.

# Node definitions:
def seg_by_superclaim(state: OverallState) -> OverallState: 
    "Give AI entire article text to segment by theme; AI updates state[article_segments] to comprise a list of segments, each with ONE parent claim attached."
    # import prompt & model:
    prompt = superclaim_prompt
    model = ChatOpenAI(model="gpt-4o", temperature=0)    

    # Ensure that return type is of SuperclaimResponse (a dict of superclaim & text)
    model_structured = model.with_structured_output(SuperclaimResponse)
    response = model_structured.invoke(prompt)
    if not isinstance(response, SuperclaimResponse):
        raise TypeError("Expected SuperclaimResponse")
        # TODO: add detailed error logging here.
    for superclaim, text in response:
        seg: SegmentState = {
        "segment": text,
        "claims": [superclaim],
        "relevance": None,
        "sentiment": None 
        }
        state["article_segments"].append(seg)
    return state

# Mapping logic:
def emit_segments(OverallState):
    """ each dict entry in OverallState["article_segments"] (i.e. segment & claim) is sent to seg_by_subclaims."""
    return [Send("seg_by_subclaims", {article_segment, claims_list}) 
            for article_segment, claims_list in OverallState["article_segments"]]

def seg_by_subclaims(state: SegmentState):
    "For a SegmentState containing (1) article text and (2) a parent claim, works through tree of child claims, assigning a claim at each level to our segment until (1) the end of the tree is reached, or (2) no relevant claim is found. Claims are appended to state[claims_list]."
    # TODO: complete!
    tree = dummy_taxonomy_tree 
    # hey Kevin! This is a dummy tree. docs: https://treelib.readthedocs.io/en/latest/
    # there is support to turn the tree structure into json or dict, if needed - will leave implementation up to you!
    # https://docs.google.com/spreadsheets/d/126K2wNkvVqveZiTTDPY67LvlHjvBojurj036fL2QJ2Q/edit?gid=0#gid=0 this is the document I referenced for the wind opposition claims. 

    # in taxonomy_to_tree.py, run the script to visualize the tree. Prompts are in the inputs file in prompts.py
    return state

def score_segment(state: SegmentState):
    """ Use LLM to score a single segment according to modular logic; enter scores into corresponding fields in SegmentState"""
    # TODO: define scoring logic; may require (1) custom prompt, define and import from prompt.py, (2) output validation - use SuperClaimResponse as reference
    return state

def aggregate_jsons(state: SegmentState):
    "Node aggregates a stream of SegmentState & updates OverallState."
    # TODO: update state[claims_list] to include new segments as they're emitted; these should replace old segments that don't yet have metadata. check mapreduce medium article linked in readme.
    return state