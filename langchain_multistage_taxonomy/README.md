<h1> Intro: </h1>

Our LangChain pipeline takes a single article, (a) segments it according to theme based on a provided codebook (all input is modular!), and then (b) emits each segment to be processed seperately (c) by a node that assigns it subclaims, then another (d) that assigns a relevancy score, and a sentiment score. These segments are then (e) aggregated into 1 data structure. 

(a) - seg_by_superclaim <br>
(b) - emit_segments <br>
(c) - seg_by_subclaims <br>
(d) - score_segment <br>
(e) - aggregate_jsons <br>


LEFT TO DO (aug 15):
- set main.py so that an actual article can be run through graph
- integrate our graph w/ langchain's graph visualization & dynamic invoking tool(s)
- alongside Kevin, define nodes (some require LLM calls; some, such as assign_score, may be more project-specific and require a fork)

article (passed in alongside currently-empty state) goes into segment_by_superclaim node; state is updated to be dict of claim, evidence.

(aug 22):
- in import_wind_taxonomy.py, update script so it can generate tree from hierarchy of any depth (needed only if we go beyond depth of 2)