# For type hints and data structures for legal decision classification workflow
from pydantic import BaseModel, Field, field_validator
from typing import TypedDict, List, Dict, Optional, Union, Any
import os
from dotenv import load_dotenv

load_dotenv()

# Base types for legal case processing
DecisionText = str
DecisionID = str
LegalConflictSummary = str
ArgumentsSummary = str

# State structure for the overall legal case processing workflow
class LegalCaseState(TypedDict):
    decision_text: DecisionText  # The entire judicial opinion text
    decision_id: DecisionID      # Unique identifier for the case
    legal_conflict_summary: Optional[LegalConflictSummary]  # Task 1 output
    plaintiff_arguments_summary: Optional[ArgumentsSummary]  # Task 2 output
    plaintiff_classifications: Optional[Dict[str, Any]]      # Task 3 output
    defendant_arguments_summary: Optional[ArgumentsSummary]  # Task 4 output
    defendant_classifications: Optional[Dict[str, Any]]      # Task 5 output
    judge_arguments_summary: Optional[ArgumentsSummary]     # Task 6 output
    judge_classifications: Optional[Dict[str, Any]]         # Task 7 output
    final_output: Optional[Dict[str, Any]]                  # Final aggregated output

# Pydantic models for structured output validation
class ReasoningClassification(BaseModel):
    is_present: bool = Field(..., description="Whether this reasoning type is present in the argument")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    supporting_text: Optional[str] = Field(None, description="Text from the argument that supports this reasoning type")
    
    @field_validator('supporting_text')
    @classmethod
    def validate_supporting_text(cls, v, info):
        """If reasoning is present, supporting text should not be null"""
        if info.data.get('is_present', False) and v is None:
            raise ValueError("Supporting text cannot be null when reasoning is present")
        return v

class ArgumentClassification(BaseModel):
    economic_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Economic reasoning",
        serialization_alias="economic_reasoning"
    )
    ecological_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Ecological reasoning",
        serialization_alias="ecological_reasoning"
    )
    health_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Health reasoning",
        serialization_alias="health_reasoning"
    )
    justice_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Justice reasoning",
        serialization_alias="justice_reasoning"
    )
    legal_procedural_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Legal-procedural reasoning",
        serialization_alias="legal_procedural_reasoning"
    )
    federalism_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Federalism reasoning",
        serialization_alias="federalism_reasoning"
    )
    deferential_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Deferential reasoning",
        serialization_alias="deferential_reasoning"
    )
    conservative_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Conservative reasoning",
        serialization_alias="conservative_reasoning"
    )
    safety_security_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Safety and security reasoning",
        serialization_alias="safety_security_reasoning"
    )
    insufficient_eis_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Insufficient environmental impact statement reasoning",
        serialization_alias="insufficient_eis_reasoning"
    )
    standing_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Standing reasoning",
        serialization_alias="standing_reasoning"
    )
    undue_burden_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Undue burden reasoning",
        serialization_alias="undue_burden_reasoning"
    )
    recreation_reasoning: List[Union[bool, float, Optional[str]]] = Field(
        ..., 
        alias="Recreation reasoning",
        serialization_alias="recreation_reasoning"
    )

    model_config = {
        "populate_by_name": True,
        "json_schema_serialization_defaults_required": True,
        "extra": "forbid",
        "use_enum_values": True
    }
    
    @field_validator('*')
    @classmethod
    def validate_reasoning_lists(cls, v):
        """Validate that reasoning lists have proper structure"""
        if not isinstance(v, list):
            raise ValueError("Reasoning data must be a list")
        if len(v) < 2:
            raise ValueError("Reasoning data must have at least 2 elements")
        if not isinstance(v[0], bool):
            raise ValueError("First element must be a boolean")
        if not isinstance(v[1], (int, float)):
            raise ValueError("Second element must be a number")
        if not (0.0 <= v[1] <= 1.0):
            raise ValueError("Confidence score must be between 0.0 and 1.0")
        if v[0] and len(v) >= 3 and v[2] is None:
            raise ValueError("Supporting text cannot be null when reasoning is present")
        return v

class ArgumentClassificationsResponse(BaseModel):
    """Response model for argument classifications with dynamic argument fields"""
    model_config = {
        "extra": "allow",
        "populate_by_name": True,
        "use_enum_values": True,
        "json_encoders": {
            List[Union[bool, float, Optional[str]]]: lambda v: v  # Preserve list format
        }
    }
    
    def __init__(self, **data):
        # Standardize argument keys to use underscores
        standardized_data = {}
        for key, value in data.items():
            # Convert argument1, argument2 etc to argument_1, argument_2
            if key.startswith('argument') and not key.startswith('argument_'):
                new_key = f"argument_{key[8:]}"
            else:
                new_key = key
                
            # Standardize the field names within each argument
            if isinstance(value, dict):
                standardized_value = {}
                for field_key, field_value in value.items():
                    if not field_key.endswith('_reasoning'):
                        field_key = f"{field_key}_reasoning"
                    standardized_value[field_key] = field_value
                standardized_data[new_key] = standardized_value
            else:
                standardized_data[new_key] = value
                
        super().__init__(**standardized_data)
    
    def model_dump(self, *args, **kwargs):
        """Ensure consistent field naming in output"""
        data = super().model_dump(*args, **kwargs)
        
        # Standardize all field names in the output
        result = {}
        for key, value in data.items():
            # Standardize argument keys
            if key.startswith('argument') and not key.startswith('argument_'):
                key = f"argument_{key[8:]}"
                
            # Standardize reasoning fields within arguments
            if isinstance(value, dict):
                value = {
                    (f"{k}_reasoning" if not k.endswith('_reasoning') else k): v
                    for k, v in value.items()
                }
            result[key] = value
            
        return result
    
    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        """Custom validation to handle dynamic argument fields"""
        if isinstance(obj, dict):
            # Standardize field names in each argument classification
            validated_data = {}
            for key, value in obj.items():
                # Standardize argument key format
                if key.startswith('argument') and not key.startswith('argument_'):
                    key = f"argument_{key[8:]}"
                
                # Standardize and validate argument contents
                if key.startswith('argument_'):
                    if isinstance(value, dict):
                        # Standardize field names within the argument
                        standardized_value = {}
                        for field_key, field_value in value.items():
                            if not field_key.endswith('_reasoning'):
                                field_key = f"{field_key}_reasoning"
                            standardized_value[field_key] = field_value
                        try:
                                                         validated_data[key] = ArgumentClassification.model_validate(standardized_value)
                        except Exception as e:
                            print(f"Warning: Invalid argument classification for {key}: {e}")
                            validated_data[key] = None
                    else:
                        validated_data[key] = value
                else:
                    validated_data[key] = value
                    
            return super().model_validate(validated_data, *args, **kwargs)
        return super().model_validate(obj, *args, **kwargs)
