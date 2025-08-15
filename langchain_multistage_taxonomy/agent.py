from openai import OpenAI 
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.types import Send # for emitting units of data in MapReduce framework.
from langchain_core.messages import AnyMessage, SystemMessage, AIMessage, ToolMessage

from format import OverallState, SegmentState
from nodes import seg_by_superclaim, seg_by_subclaims, aggregate_jsons

# Mapping logic:
def emit_segments(OverallState):
    """ each dict entry in OverallState["article_segments"] (i.e. segment & claim) is sent to seg_by_subclaims."""
    return [Send("seg_by_subclaims", {article_segment, claims_list}) 
            for article_segment, claims_list in OverallState["article_segments"]]


## Time to make our graph! ##
workflow = StateGraph(OverallState) 

# Add nodes:
workflow.add_node('seg_by_superclaim', seg_by_superclaim)
workflow.add_node('seg_by_subclaims', seg_by_subclaims)
workflow.add_node('aggregate_jsons', aggregate_jsons)
# Add edges:
workflow.add_edge(START, 'seg_by_superclaim')
workflow.add_conditional_edges('seg_by_superclaim', emit_segments, ['seg_by_subclaims']) # syntax reference from Medium: graph.add_conditional_edges("evaluate_solution", continue_to_deep_thought, ["deepen_thought"])

workflow.add_edge('seg_by_subclaims', END)

# Compile:
graph = workflow.compile() 