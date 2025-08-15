# For type hints:
from pydantic import BaseModel, Field
from typing import TypedDict, List, Dict

article_segment = str
ClaimsList = List[str] # a list of claims structured [superclaim, subclaim, subsubclaim] 

###### template for states: ######

# overall state passed in and out of graph:
class OverallState(TypedDict):
    article_str: str # the entire article, passed as input.
    article_segments: dict[article_segment, ClaimsList] 

# State of each text segment, passed seperately through intermediate nodes, to join at graph's end:
class SegmentState(TypedDict):
    segment_str: str 
    ClaimsList: List[str] 



##### template for schemas: #####

# these schemas serve as blueprints to ensure that our nodes' output is in the correct format.
# This prevents us from having to ask our LLM nicely for a JSON and then pray.

# Reference - unused:
class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    answer: str = Field(description="The answer to the user's question")

class SuperclaimResponse(BaseModel):
    claims: Dict[str, str] = Field(
        description="Dictionary of {superclaim, corresponding article segment}"
        )

class SubclaimResponse(BaseModel):
    claims: Dict[str, str] = Field(
        description="A dictionary mapping each superclaim to its corresponding article segment"
        )