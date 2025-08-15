Logic:
article (passed in alongside currently-empty state) goes into segment_by_superclaim node; state is updated to be dict of claim, evidence.

Note: our agent uses a MapReduce framework; see the below resource.
https://medium.com/@astropomeai/implementing-map-reduce-with-langgraph-creating-flexible-branches-for-parallel-execution-b6dc44327c0e


LEFT TO DO (aug 15):
- fix invoke in main.py
- clean up and formalize annotationg & docstrings in nodes.py
- make a visualizer of graph, as Sybille showed.
- correct logic of passing in intiial article string
- alongside Kevin, define nodes (some require LLM calls)