# these schemas serve as blueprints to ensure that our nodes' output is in the correct format.
# This prevents us from having to ask our LLM nicely for a JSON and then pray.

from pydantic import BaseModel, Field
from typing import Dict 

class SuperclaimResponse(BaseModel):
    claims: Dict[str, str] = Field(
        description="A dictionary mapping each superclaim to its corresponding article segment"
        )

class SubclaimResponse(BaseModel):
    claims: Dict[str, str] = Field(
        description="A dictionary mapping each superclaim to its corresponding article segment"
        )
