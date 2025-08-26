# LangGraph workflow for legal case classification
# This implements the 7-task workflow from summary_chunked_instructor.py

from langgraph.graph import StateGraph, START, END
from .format import LegalCaseState
from .nodes import (
    identify_legal_conflict,
    summarize_plaintiff_arguments,
    classify_plaintiff_arguments,
    summarize_defendant_arguments,
    classify_defendant_arguments,
    summarize_judge_arguments,
    classify_judge_arguments,
    aggregate_final_output
)

# Create the workflow graph
workflow = StateGraph(LegalCaseState)

# Add all nodes to the workflow
workflow.add_node("identify_legal_conflict", identify_legal_conflict)
workflow.add_node("summarize_plaintiff_arguments", summarize_plaintiff_arguments)
workflow.add_node("classify_plaintiff_arguments", classify_plaintiff_arguments)
workflow.add_node("summarize_defendant_arguments", summarize_defendant_arguments)
workflow.add_node("classify_defendant_arguments", classify_defendant_arguments)
workflow.add_node("summarize_judge_arguments", summarize_judge_arguments)
workflow.add_node("classify_judge_arguments", classify_judge_arguments)
workflow.add_node("aggregate_final_output", aggregate_final_output)

# Define the workflow sequence
# Start with legal conflict identification
workflow.add_edge(START, "identify_legal_conflict")

# Then process plaintiff arguments (summary + classification)
workflow.add_edge("identify_legal_conflict", "summarize_plaintiff_arguments")
workflow.add_edge("summarize_plaintiff_arguments", "classify_plaintiff_arguments")

# Then process defendant arguments (summary + classification)
workflow.add_edge("classify_plaintiff_arguments", "summarize_defendant_arguments")
workflow.add_edge("summarize_defendant_arguments", "classify_defendant_arguments")

# Then process judge arguments (summary + classification)
workflow.add_edge("classify_defendant_arguments", "summarize_judge_arguments")
workflow.add_edge("summarize_judge_arguments", "classify_judge_arguments")

# Finally aggregate all results
workflow.add_edge("classify_judge_arguments", "aggregate_final_output")
workflow.add_edge("aggregate_final_output", END)

# Compile the workflow
graph = workflow.compile()

# Function to run the workflow for a single case
def run_legal_case_workflow(decision_text: str, decision_id: str) -> LegalCaseState:
    """
    Run the complete legal case classification workflow
    
    Args:
        decision_text: The full text of the judicial opinion
        decision_id: Unique identifier for the case
        
    Returns:
        LegalCaseState: Complete processed case with all classifications
    """
    # Initialize the state
    initial_state = {
        "decision_text": decision_text,
        "decision_id": decision_id,
        "legal_conflict_summary": None,
        "plaintiff_arguments_summary": None,
        "plaintiff_classifications": None,
        "defendant_arguments_summary": None,
        "defendant_classifications": None,
        "judge_arguments_summary": None,
        "judge_classifications": None,
        "final_output": None
    }
    
    # Run the workflow
    print(f"\n🚀 Starting legal case workflow for {decision_id}")
    print(f"📝 Decision text length: {len(decision_text)} characters")
    
    try:
        result = graph.invoke(initial_state)
        print(f"✅ Workflow completed successfully for {decision_id}")
        return result
    except KeyError as ke:
        print(f"❌ Workflow failed for {decision_id} due to KeyError: {str(ke)}")
        print(f"🔍 This suggests the LLM returned malformed JSON. Creating fallback result.")
        # Create a fallback result with partial data
        fallback_state = initial_state.copy()
        fallback_state['plaintiff_classifications'] = {}
        fallback_state['defendant_classifications'] = {}
        fallback_state['judge_classifications'] = {}
        fallback_state['final_output'] = {
            "Summary of legal conflict": fallback_state.get('legal_conflict_summary', 'Error: Classification failed'),
            "Summary of plaintiff arguments": fallback_state.get('plaintiff_arguments_summary', 'Error: Classification failed'),
            "Summary of defendant arguments": fallback_state.get('defendant_arguments_summary', 'Error: Classification failed'),
            "Summary of judge arguments": fallback_state.get('judge_arguments_summary', 'Error: Classification failed')
        }
        return fallback_state
    except Exception as e:
        print(f"❌ Workflow failed for {decision_id}: {str(e)}")
        print(f"🔍 Error type: {type(e).__name__}")
        print(f"🔍 Error details: {repr(e)}")
        # Return partial state if available
        return initial_state

# Function to run multiple cases
def run_batch_legal_cases(cases_data: list) -> list:
    """
    Run the workflow for multiple cases
    
    Args:
        cases_data: List of dicts with 'decision_text' and 'decision_id' keys
        
    Returns:
        list: List of processed LegalCaseState objects
    """
    results = []
    
    for i, case in enumerate(cases_data, 1):
        print(f"\n{'='*60}")
        print(f"Processing case {i}/{len(cases_data)}: {case['decision_id']}")
        print(f"{'='*60}")
        
        try:
            result = run_legal_case_workflow(
                case['decision_text'], 
                case['decision_id']
            )
            results.append(result)
        except Exception as e:
            print(f"❌ Failed to process case {case['decision_id']}: {str(e)}")
            # Add error case to results
            error_state = {
                "decision_text": case['decision_text'],
                "decision_id": case['decision_id'],
                "legal_conflict_summary": f"Error: {str(e)}",
                "plaintiff_arguments_summary": None,
                "plaintiff_classifications": None,
                "defendant_arguments_summary": None,
                "defendant_classifications": None,
                "judge_arguments_summary": None,
                "judge_classifications": None,
                "final_output": None
            }
            results.append(error_state)
    
    return results
