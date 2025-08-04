# for reading Google sheet housing our taxonomy:
from sheetfu import SpreadsheetApp
# for calling LLMs & abstracting LLM input / output logic:
from openai import OpenAI 
from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage, SystemMessage, AIMessage, ToolMessage
# for storing our hierarchy of claims as a tree:
from typing import TypedDict, Annotated
from treelib import Tree
# For accessing environment variables frm .env file:
import os
from dotenv import load_dotenv   

# TODO: move spreadsheet integration away from here.

## Constants: ##
load_dotenv()

# our OpenAI key:
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# our taxonomy:
sheet_url = os.getenv("TAXONOMY_GSHEET_URL")
# The indices of the rows within spreadsheet we care about:
column_indices = {
    "Number": 0,
    "SuperclaimShortName": 1, 
    "Superclaim": 2,
    "SubclaimShortName": 3,
    "Subclaim": 4,
    "SubSubShortName": 5,
    "SubSubclaim": 6
} # ^ TODO: move this to .env.

# TODO: import spreadsheet as array.
def import_spreadsheet(url: str,
                       column_indices: dict = column_indices,
                       ) -> list[list]:
    ''' Import taxonomy spreadsheet as an array, only keeping meaningful columns (i.e. those in column_indices.) '''
    return []

# TODO: turn taxonomy spreadsheet into taxonomy tree.
def array_to_tree(arr: list[list]) -> Tree:
    '''Turns our array of claim entries into a tree of L1: Superclaim, L2: Subclaim, L3 (optional): Subsubclaim'''
    # TODO: add an option to visually render tree.

# 

# Figure out:
# - spreadsheet API
# - 