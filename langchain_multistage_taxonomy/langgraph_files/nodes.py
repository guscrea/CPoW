# Legal case classification workflow nodes for LangGraph
# These nodes implement the 7 tasks from summary_chunked_instructor.py

import os
import json
from dotenv import load_dotenv
from .format import LegalCaseState, ArgumentClassificationsResponse
from .prompts import (
    system_prompt, legal_conflict_prompt, plaintiff_arguments_prompt,
    plaintiff_classification_prompt, defendant_arguments_prompt,
    defendant_classification_prompt, judge_arguments_prompt,
    judge_classification_prompt
)
from langchain_openai import ChatOpenAI
from openai import OpenAI
from typing import Dict, Any
import re

load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key, max_retries=3)

# Initialize LangChain model for text generation
model = ChatOpenAI(model="o4-mini", temperature=1)

def extract_text_from_response(response_text: str) -> str:
    """Extract the main text content from the response"""
    lines = response_text.strip().split('\n')
    content_start = 0
    for i, line in enumerate(lines):
        if line.strip() and not line.startswith('Task') and not line.startswith('Please'):
            content_start = i
            break
    
    return '\n'.join(lines[content_start:]).strip()

def standardize_argument_key(key: str) -> str:
    """Standardize argument key format to argument_N"""
    key = key.lower()
    num = ''.join(c for c in key if c.isdigit())
    if num:
        return f"argument_{num}"
    return key

def update_argument_classification(classification_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update an argument classification with LLM output"""
    if not isinstance(classification_data, dict):
        print(f"❌ Skipping non-dict classification data: {classification_data}")
        return None
        
    argument_data = {}
    
    # Field name mapping to ensure consistent naming
    field_mappings = {
        "cost reasoning": "cost_reasoning",
        "economic reasoning": "economic_reasoning",
        "ecological reasoning": "ecological_reasoning", 
        "major federal action reasoning": "major_federal_action_reasoning",
        "missing congressional approval reasoning": "missing_congressional_approval_reasoning",
        "omission reasoning": "omission_reasoning",
        "valid environmental analysis reasoning": "valid_environmental_analysis_reasoning",
        "feasible alternative reasoning": "feasible_alternative_reasoning",
        "good faith analysis reasoning": "good_faith_analysis_reasoning",
        "consultation reasoning": "consultation_reasoning",
        "health reasoning": "health_reasoning",
        "undue burden reasoning": "undue_burden_reasoning",
        "equality reasoning": "equality_reasoning",
        "justice reasoning": "justice_reasoning",
        "legal-procedural reasoning": "legal_procedural_reasoning",
        "legal procedural reasoning": "legal_procedural_reasoning",
        "federalism reasoning": "federalism_reasoning",
        "deferential reasoning": "deferential_reasoning",
        "conservative reasoning": "conservative_reasoning",
        "military reasoning": "military_reasoning",
        "safety and security reasoning": "safety_security_reasoning",
        "insufficient environmental impact statement reasoning": "insufficient_eis_reasoning",
        "standing reasoning": "standing_reasoning",
        "recreation reasoning": "recreation_reasoning",
        "retroactive reasoning": "retroactive_reasoning",
        "legal technicality reasoning": "legal_technicality_reasoning"
    }
    
    for key, value in classification_data.items():
        normalized_key = key.lower().strip()
        
        if normalized_key in field_mappings:
            std_key = field_mappings[normalized_key]
        else:
            std_key = normalized_key.replace(" ", "_").replace("-", "_")
            std_key = std_key.replace("_reasoning_reasoning", "_reasoning")
            if not std_key.endswith("_reasoning"):
                std_key = f"{std_key}_reasoning"
            
        if isinstance(value, list) and len(value) >= 2:
            if value[0] or value[1] > 0:
                argument_data[std_key] = value
                print(f"✅ Added valid reasoning: {std_key} = {value}")
            else:
                print(f"ℹ️ Skipping zero-confidence reasoning: {std_key} = {value}")
        else:
            print(f"❌ Invalid reasoning value format: {std_key} = {value}")
    
    return argument_data if argument_data else None

def clean_json_keys(data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean up JSON keys that may have newlines, whitespace, or other formatting issues"""
    if not isinstance(data, dict):
        return data
    
    cleaned_data = {}
    for key, value in data.items():
        # Clean the key by removing newlines, extra whitespace, and quotes
        clean_key = key.strip().strip('\n').strip()
        # Remove leading/trailing quotes if present
        if clean_key.startswith('"') and clean_key.endswith('"'):
            clean_key = clean_key[1:-1]
        if clean_key.startswith("'") and clean_key.endswith("'"):
            clean_key = clean_key[1:-1]
        # Clean any remaining whitespace
        clean_key = clean_key.strip()
        
        # Recursively clean nested dictionaries
        if isinstance(value, dict):
            value = clean_json_keys(value)
        elif isinstance(value, list):
            value = [clean_json_keys(item) if isinstance(item, dict) else item for item in value]
        
        cleaned_data[clean_key] = value
    
    return cleaned_data

def parse_classification_response(response_text: str) -> Dict[str, Any]:
    """Parse the classification response from the LLM"""
    try:
        # Parse the JSON and clean up any malformed keys
        raw_data = json.loads(response_text)
        return clean_json_keys(raw_data)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Response text: {response_text[:200]}...")
        # Try to extract JSON from the response as fallback
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                raw_data = json.loads(json_str)
                return clean_json_keys(raw_data)
            else:
                print(f"❌ No JSON found in response: {response_text[:200]}...")
                return {}
        except Exception as fallback_e:
            print(f"❌ Fallback JSON parsing also failed: {fallback_e}")
            return {}
    except Exception as e:
        print(f"❌ Error parsing response: {e}")
        return {}

# Node 1: Legal conflict identification
def identify_legal_conflict(state: LegalCaseState) -> LegalCaseState:
    """Task 1: Identify the basic legal conflict in the case"""
    print(f"=== Processing Legal Conflict for {state['decision_id']} ===")
    
    # Format the prompt with decision text and ID
    formatted_system = system_prompt.format(
        decision_text=state['decision_text'],
        decision_id=state['decision_id']
    )
    
    prompt = legal_conflict_prompt.format(system_prompt=formatted_system)
    
    try:
        response = model.invoke(prompt)
        summary = extract_text_from_response(response.content)
        state['legal_conflict_summary'] = summary
        print(f"✅ Legal conflict identified: {len(summary)} characters")
    except Exception as e:
        print(f"❌ Legal conflict identification failed: {str(e)}")
        state['legal_conflict_summary'] = "Error processing legal conflict"
    
    return state

# Node 2: Plaintiff arguments summary
def summarize_plaintiff_arguments(state: LegalCaseState) -> LegalCaseState:
    """Task 2: Summarize plaintiff arguments"""
    print(f"=== Processing Plaintiff Arguments for {state['decision_id']} ===")
    
    formatted_system = system_prompt.format(
        decision_text=state['decision_text'],
        decision_id=state['decision_id']
    )
    
    prompt = plaintiff_arguments_prompt.format(system_prompt=formatted_system)
    
    try:
        response = model.invoke(prompt)
        summary = extract_text_from_response(response.content)
        state['plaintiff_arguments_summary'] = summary
        print(f"✅ Plaintiff arguments summarized: {len(summary)} characters")
    except Exception as e:
        print(f"❌ Plaintiff arguments summary failed: {str(e)}")
        state['plaintiff_arguments_summary'] = "Error processing plaintiff arguments"
    
    return state

# Node 3: Plaintiff argument classification
def classify_plaintiff_arguments(state: LegalCaseState) -> LegalCaseState:
    """Task 3: Classify plaintiff arguments by reasoning type"""
    print(f"=== Processing Plaintiff Classification for {state['decision_id']} ===")
    
    if not state.get('plaintiff_arguments_summary'):
        print("❌ No plaintiff arguments summary available")
        return state
    
    formatted_system = system_prompt.format(
        decision_text=state['decision_text'],
        decision_id=state['decision_id']
    )
    
    prompt = plaintiff_classification_prompt.format(
        system_prompt=formatted_system,
        plaintiff_arguments=state['plaintiff_arguments_summary']
    )
    
    # Estimate token count (rough approximation: 1 token ≈ 4 characters)
    estimated_tokens = len(prompt) // 4
    print(f"🔍 Estimated prompt tokens: {estimated_tokens}")
    
    try:
        # Use standard OpenAI API call with JSON response format
        response = client.chat.completions.create(
            model="o4-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        response_text = response.choices[0].message.content
        print(f"🔍 Raw LLM response (first 500 chars): {repr(response_text[:500])}")
        print(f"🔍 Raw LLM response length: {len(response_text)}")
        print(f"🔍 Raw LLM response (last 200 chars): {repr(response_text[-200:])}")
        
        # Check if response starts with proper JSON
        if not response_text.strip().startswith('{'):
            print(f"❌ Response doesn't start with '{{': {repr(response_text[:100])}")
            # Try to find JSON in the response
            json_start = response_text.find('{')
            if json_start != -1:
                print(f"🔍 Found JSON starting at position {json_start}")
                response_text = response_text[json_start:]
            else:
                print(f"❌ No JSON found in response")
                state['plaintiff_classifications'] = {}
                return state
        
        try:
            raw_data = parse_classification_response(response_text)
            print(f"Raw plaintiff classification data keys: {list(raw_data.keys())}")
            print(f"Raw plaintiff classification data: {raw_data}")
        except Exception as parse_error:
            print(f"❌ Error parsing classification response: {parse_error}")
            print(f"🔍 Response that failed: {repr(response_text[:200])}")
            state['plaintiff_classifications'] = {}
            return state
        
        plaintiff_classifications = {}
        for arg_key, arg_value in raw_data.items():
            if "argument" in arg_key.lower():
                std_key = standardize_argument_key(arg_key)
                print(f"\nProcessing plaintiff {std_key}:")
                processed_arg = update_argument_classification(arg_value)
                if processed_arg:
                    plaintiff_classifications[std_key] = processed_arg
                    print(f"✅ Added {std_key} to plaintiff classifications")
        
        state['plaintiff_classifications'] = plaintiff_classifications
        print(f"✅ Plaintiff classification processed successfully")
        
    except Exception as e:
        print(f"❌ Plaintiff classification processing failed: {str(e)}")
        state['plaintiff_classifications'] = {}
    
    return state

# Node 4: Defendant arguments summary
def summarize_defendant_arguments(state: LegalCaseState) -> LegalCaseState:
    """Task 4: Summarize defendant arguments"""
    print(f"=== Processing Defendant Arguments for {state['decision_id']} ===")
    
    formatted_system = system_prompt.format(
        decision_text=state['decision_text'],
        decision_id=state['decision_id']
    )
    
    prompt = defendant_arguments_prompt.format(system_prompt=formatted_system)
    
    try:
        response = model.invoke(prompt)
        summary = extract_text_from_response(response.content)
        state['defendant_arguments_summary'] = summary
        print(f"✅ Defendant arguments summarized: {len(summary)} characters")
    except Exception as e:
        print(f"❌ Defendant arguments summary failed: {str(e)}")
        state['defendant_arguments_summary'] = "Error processing defendant arguments"
    
    return state

# Node 5: Defendant argument classification
def classify_defendant_arguments(state: LegalCaseState) -> LegalCaseState:
    """Task 5: Classify defendant arguments by reasoning type"""
    print(f"=== Processing Defendant Classification for {state['decision_id']} ===")
    
    if not state.get('defendant_arguments_summary'):
        print("❌ No defendant arguments summary available")
        return state
    
    formatted_system = system_prompt.format(
        decision_text=state['decision_text'],
        decision_id=state['decision_id']
    )
    
    prompt = defendant_classification_prompt.format(
        system_prompt=formatted_system,
        defendant_arguments=state['defendant_arguments_summary']
    )
    
    try:
        # Use standard OpenAI API call with JSON response format
        response = client.chat.completions.create(
            model="o4-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        response_text = response.choices[0].message.content
        print(f"🔍 Raw LLM response (first 500 chars): {repr(response_text[:500])}")
        print(f"🔍 Raw LLM response length: {len(response_text)}")
        raw_data = parse_classification_response(response_text)
        print(f"Raw defendant classification data keys: {list(raw_data.keys())}")
        print(f"Raw defendant classification data: {raw_data}")
        
        defendant_classifications = {}
        for arg_key, arg_value in raw_data.items():
            if "argument" in arg_key.lower():
                std_key = standardize_argument_key(arg_key)
                print(f"\nProcessing defendant {std_key}:")
                processed_arg = update_argument_classification(arg_value)
                if processed_arg:
                    defendant_classifications[std_key] = processed_arg
                    print(f"✅ Added {std_key} to defendant classifications")
        
        state['defendant_classifications'] = defendant_classifications
        print(f"✅ Defendant classification processed successfully")
        
    except Exception as e:
        print(f"❌ Defendant classification processing failed: {str(e)}")
        state['defendant_classifications'] = {}
    
    return state

# Node 6: Judge arguments summary
def summarize_judge_arguments(state: LegalCaseState) -> LegalCaseState:
    """Task 6: Summarize judge arguments"""
    print(f"=== Processing Judge Arguments for {state['decision_id']} ===")
    
    formatted_system = system_prompt.format(
        decision_text=state['decision_text'],
        decision_id=state['decision_id']
    )
    
    prompt = judge_arguments_prompt.format(system_prompt=formatted_system)
    
    try:
        response = model.invoke(prompt)
        summary = extract_text_from_response(response.content)
        state['judge_arguments_summary'] = summary
        print(f"✅ Judge arguments summarized: {len(summary)} characters")
    except Exception as e:
        print(f"❌ Judge arguments summary failed: {str(e)}")
        state['judge_arguments_summary'] = "Error processing judge arguments"
    
    return state

# Node 7: Judge argument classification
def classify_judge_arguments(state: LegalCaseState) -> LegalCaseState:
    """Task 7: Classify judge arguments by reasoning type"""
    print(f"=== Processing Judge Classification for {state['decision_id']} ===")
    
    if not state.get('judge_arguments_summary'):
        print("❌ No judge arguments summary available")
        return state
    
    formatted_system = system_prompt.format(
        decision_text=state['decision_text'],
        decision_id=state['decision_id']
    )
    
    prompt = judge_classification_prompt.format(
        system_prompt=formatted_system,
        judge_arguments=state['judge_arguments_summary']
    )
    
    try:
        # Use standard OpenAI API call with JSON response format
        response = client.chat.completions.create(
            model="o4-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        response_text = response.choices[0].message.content
        print(f"🔍 Raw LLM response (first 500 chars): {repr(response_text[:500])}")
        print(f"🔍 Raw LLM response length: {len(response_text)}")
        raw_data = parse_classification_response(response_text)
        print(f"Raw judge classification data keys: {list(raw_data.keys())}")
        print(f"Raw judge classification data: {raw_data}")
        
        judge_classifications = {}
        for arg_key, arg_value in raw_data.items():
            if "argument" in arg_key.lower():
                std_key = standardize_argument_key(arg_key)
                print(f"\nProcessing judge {std_key}:")
                processed_arg = update_argument_classification(arg_value)
                if processed_arg:
                    judge_classifications[std_key] = processed_arg
                    print(f"✅ Added {std_key} to judge classifications")
        
        state['judge_classifications'] = judge_classifications
        print(f"✅ Judge classification processed successfully")
        
    except Exception as e:
        print(f"❌ Judge classification processing failed: {str(e)}")
        state['judge_classifications'] = {}
    
    return state

# Node 8: Final aggregation and output formatting
def aggregate_final_output(state: LegalCaseState) -> LegalCaseState:
    """Final node: Aggregate all results into final output format"""
    print(f"=== Aggregating Final Output for {state['decision_id']} ===")
    
    final_output = {
        "ID": state['decision_id'],
        "Summary of legal conflict": state.get('legal_conflict_summary', ''),
        "Summary of plaintiff arguments": state.get('plaintiff_arguments_summary', ''),
        "Summary of defendant arguments": state.get('defendant_arguments_summary', ''),
        "Summary of judge arguments": state.get('judge_arguments_summary', ''),
        "Plaintiff individual argument classifications": state.get('plaintiff_classifications', {}),
        "Defendant individual argument classifications": state.get('defendant_classifications', {}),
        "Judge individual argument classifications": state.get('judge_classifications', {})
    }
    
    state['final_output'] = final_output
    print(f"✅ Final output aggregated successfully")
    
    return state