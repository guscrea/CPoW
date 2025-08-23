#TODO: import superclaims & subclaims, along with definition

superclaims_codebook = "placeholder"

superclaim_prompt = """
You are given an article about a wind energy development project that may have received contention.
\n
Your job is to segment the given article by theme(s), according to the given codebook. The codebook text is given after this prompt, & the article text is given after the codebook.
\n
CODEBOOK (CLAIMS WITH DEFINITIONS): \n
{superclaims_list}
\n
ARTICLE: \n
{article}
"""

subclaim_prompt = """
You are given a passage and a general category that describes the claim it's making.
From the following list of sub-claims, pick the sub-claim that most accurately matches the passage's claim.
\n
SEGMENT: \n
{segment}
SUBCLAIMS LIST: \n
{subclaims_list}
\n
"""
