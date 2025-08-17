# NOTE: python is highlighting things in red, but I believe (?) syntax is correct. Better to check again.

from openai import OpenAI 
from langgraph.graph import StateGraph, START, END, add_messages
from langchain_core.messages import AnyMessage, SystemMessage, AIMessage, ToolMessage

from format import OverallState, SegmentState
from nodes import seg_by_superclaim, emit_segments, seg_by_subclaims, aggregate_jsons

workflow = StateGraph(OverallState) 

# Add nodes:
workflow.add_node('seg_by_superclaim', seg_by_superclaim)
workflow.add_node('emit_segments", emit_segments)
workflow.add_node('seg_by_subclaims', seg_by_subclaims)
workflow.add_node('score_segment', score_segment)
workflow.add_node('aggregate_jsons', aggregate_jsons)
# Add edges:
workflow.add_edge(START, 'seg_by_superclaim')
workflow.add_conditional_edges('seg_by_superclaim', emit_segments, ['seg_by_subclaims']) # syntax reference from Medium: graph.add_conditional_edges("evaluate_solution", continue_to_deep_thought, ["deepen_thought"])
workflow.add_edge('seg_by_subclaims', 'score_segment')
workflow.add_edge('score_segment', 'aggregate_jsons') # TODO: this is placeholder code! aggregate must actually aggregate.
workflow.add_edge('aggregate_jsons', END)

# Compile:
graph = workflow.compile() 
