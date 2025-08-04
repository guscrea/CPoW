#TODO: source inputs.

superclaim_prompt = """Segment {input} by superclaim & emit segments in JSON of claim, text."""

subclaim_prompt = """classify {input}"""

class SuperclaimResponse(BaseModel):
    superclaim: str
    text: str