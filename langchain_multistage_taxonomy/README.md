<h1> Intro: </h1>

Our LangChain pipeline takes a single article, (a) segments it according to theme based on a provided codebook (all input is modular!), and then (b) emits each segment to be processed seperately (c) by a node that assigns it subclaims, then another (d) that assigns a relevancy score, and a sentiment score. These segments are then (e) aggregated into 1 data structure. 

(a) - seg_by_superclaim
(b) - emit_segments
(c) - seg_by_subclaims
(d) - score_segment
(e) - aggregate_jsons


LEFT TO DO (aug 15):
- add sentiment scoring
- fix invoke in main.py
- clean up and formalize annotations & docstrings in nodes.py
- make a visualizer of graph, as Sybille showed.
- correct logic of passing in intiial article string
- alongside Kevin, define nodes (some require LLM calls)

article (passed in alongside currently-empty state) goes into segment_by_superclaim node; state is updated to be dict of claim, evidence.
