###########
# JUL 28: TODO (logic)
# - define nodes
# - figure out how to compile graph for basic checks
# - define LLM call.

## TODO (fixing)
# - figure out operator methods for updating state
# - figure out send API & conditional edges, possibly needed during emission.
###########

# For calling LLMs & abstracting LLM input / output logic:
from openai import OpenAI 
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.types import Send # for emitting units of data in MapReduce framework.
from langchain_core.messages import AnyMessage, SystemMessage, AIMessage, ToolMessage
import operator

# For type hints:
from pydantic import Field
from typing import TypedDict, List, Annotated, Optional

# Our nodes:
from nodes import seg_by_superclaim, seg_by_subclaims, aggregate_jsons
# Note: our agent uses a MapReduce framework; see the below resource.
# https://medium.com/@astropomeai/implementing-map-reduce-with-langgraph-creating-flexible-branches-for-parallel-execution-b6dc44327c0e

# Aliasing!
article_segment = str
ClaimsList = List[str] # a list of claims: [superclaim, subclaim, subsubclaim] 

# Defining overall state passed in and out of graph:
class OverallState(TypedDict):
    article_str: str # the entire article, passed as input.
    article_segments: dict[article_segment, ClaimsList] 

# State of each text segment, passed seperately through intermediate nodes, to join at graph's end:
class SegmentState(TypedDict):
    segment_str: str 
    ClaimsList: List[str] 

# Define mapping logic:
def emit_segments(OverallState):
    return [Send("deepen_thought", {"solution": r}) for r in OverallState["article_segments"]]

## Time to make our graph! ##

workflow = StateGraph(OverallState) 
# Add nodes:
workflow.add_node('seg_by_superclaim', seg_by_superclaim)
workflow.add_node('seg_by_subclaims', seg_by_subclaims)
workflow.add_node('aggregate_jsons', aggregate_jsons)

# Add edges:
workflow.add_edge(START, 'seg_by_superclaim')
workflow.add_conditional_edges('seg_by_superclaim', 
emit_segments,
['seg_by_subclaims'])
workflow.add_edge('seg_by_subclaims', END)

# compile!
graph = workflow.compile()


# class sybilles_agent:
#     def __init__(self, model, tools, checkpointer, system=''):
#         self.system = system

#         # Define workflow graph
#         workflow = StateGraph(AgentState)
#         workflow.add_node('llm_call', self.call_ollama)
#         workflow.add_node('action', self.take_action)
#         workflow.add_conditional_edges(
#             'llm_call',
#             self.exists_action,
#             {True: 'action', False: END}
#         )
#         workflow.add_edge('action', 'llm_call')
#         workflow.set_entry_point('llm_call')
#         self.workflow = workflow.compile(checkpointer=checkpointer)
#         self.tools = {t.name: t for t in tools}
#         self.model = model.bind_tools(tools)

#     def exists_action(self, state:AgentState):
#         result = state['messages'][-1]
#         return len(result.tool_calls) > 0
    
    def call_ollama(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}
    
#     def take_action(self, state: AgentState):
#         tool_calls = state['messages'][-1].tool_calls
#         results = []
#         for t in tool_calls:
#             print(f'Calling: {t}')
#             if not t['name'] in self.tools:
#                 print('\n ....bad tool name....')
#                 result = 'bad tool name, retry'
#             else:
#                 result = self.tools[t['name']].invoke(t['args'])
#             results.append(ToolMessage(
#                 tool_call_id=t['id'],
#                 name=t['name'],
#                 content=str(result)
#             ))
#         print('Back to the model!')
#         return {'messages': results}