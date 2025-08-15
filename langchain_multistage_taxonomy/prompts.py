#TODO: load superclaims_codebook correctly.
superclaims_codebook = "placeholder"

superclaim_prompt = """Segment {input} by superclaim & emit segments in JSON of claim, text. Use the following codebook of superclaims: {superclaims_codebook}"""

subclaim_prompt = """classify {input}"""
