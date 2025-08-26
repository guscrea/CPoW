# LangGraph Legal Case Classification Workflow Package
# This package implements the legal decision classification workflow using LangGraph

from .agent import run_legal_case_workflow, run_batch_legal_cases
from .format import LegalCaseState, ArgumentClassificationsResponse
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

__all__ = [
    'run_legal_case_workflow',
    'run_batch_legal_cases',
    'LegalCaseState',
    'ArgumentClassificationsResponse',
    'identify_legal_conflict',
    'summarize_plaintiff_arguments',
    'classify_plaintiff_arguments',
    'summarize_defendant_arguments',
    'classify_defendant_arguments',
    'summarize_judge_arguments',
    'classify_judge_arguments',
    'aggregate_final_output'
] 