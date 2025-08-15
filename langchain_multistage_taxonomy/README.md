<h1> Intro: </h1>

Our LangChain pipeline takes a single article, (a) segments it according to theme based on a provided codebook (all input is modular!), and then (b) emits each segment to be processed seperately (c) by a node that assigns it subclaims, a relevancy score, and a sentiment score. These segments are then (d) aggregated into 1 data structure. 

(a) - seg_by_superclaim
(b) - emit_segments
(c) - seg_by_subclaims
(d) - aggregate_jsons

Note: our agent uses a MapReduce framework; see the below resource.
https://medium.com/@astropomeai/implementing-map-reduce-with-langgraph-creating-flexible-branches-for-parallel-execution-b6dc44327c0e

<h2> Graph logic </h2>
class OverallState(TypedDict):
    article_str: str # the entire article, passed as input.
    article_segments: list[dict[article_segment, ClaimsList, additional fields such as sentiment scoring]]

seg_by_superclaim(OverallState: TypedDict) -> OverallState
    input: OverallState["article_str"] consists of the entire article in string format; OverallState["article_segments"] is empty.
    output: article_str is unchanged; article_segments now holds

emit_segments


seg_by_subclaims aggregate_jsons

<h2> _ </h2>
           
START --> seg_by_superclaim --> emit_segments ==> seg_by_subclaims ==> aggregate_jsons --> END




LEFT TO DO (aug 15):
- add sentiment scoring
- fix invoke in main.py
- clean up and formalize annotations & docstrings in nodes.py
- make a visualizer of graph, as Sybille showed.
- correct logic of passing in intiial article string
- alongside Kevin, define nodes (some require LLM calls)

article (passed in alongside currently-empty state) goes into segment_by_superclaim node; state is updated to be dict of claim, evidence.
