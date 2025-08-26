# LangGraph Legal Case Classification Workflow

This directory contains a refactored version of the legal decision classification workflow using LangGraph, replacing the previous `summary_chunked_instructor.py` approach.

## Overview

The workflow processes legal decisions through 7 sequential tasks:

1. **Legal Conflict Identification** - Identify the basic legal conflict
2. **Plaintiff Arguments Summary** - Summarize plaintiff arguments
3. **Plaintiff Argument Classification** - Classify plaintiff arguments by reasoning type
4. **Defendant Arguments Summary** - Summarize defendant arguments
5. **Defendant Argument Classification** - Classify defendant arguments by reasoning type
6. **Judge Arguments Summary** - Summarize judge arguments
7. **Judge Argument Classification** - Classify judge arguments by reasoning type

## Architecture

- **`format.py`** - Data structures and Pydantic models for the workflow
- **`prompts.py`** - All prompts for the 7 tasks
- **`nodes.py`** - Individual workflow nodes implementing each task
- **`agent.py`** - LangGraph workflow definition and execution functions
- **`run_langgraph_workflow.py`** - Main script to run the workflow

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

3. Ensure your CSV data file is available (update path in `run_langgraph_workflow.py` if needed)

## Usage

### Basic Usage

Run the workflow on a single case:

```python
from agent import run_legal_case_workflow

result = run_legal_case_workflow(
    decision_text="Your legal decision text here...",
    decision_id="case_001"
)
```

### Batch Processing

Process multiple cases:

```python
from agent import run_batch_legal_cases

cases = [
    {"decision_text": "Text 1...", "decision_id": "case_001"},
    {"decision_text": "Text 2...", "decision_id": "case_002"}
]

results = run_batch_legal_cases(cases)
```

### Command Line

Run the complete workflow:

```bash
python run_langgraph_workflow.py
```

## Output Structure

Each processed case produces:

- **Legal conflict summary** - Brief description of the legal dispute
- **Arguments summaries** - Summaries for plaintiff, defendant, and judge arguments
- **Argument classifications** - Structured classification of reasoning types for each argument
- **Final output** - Aggregated results in the same format as the original workflow

## Key Differences from Original Workflow

1. **Sequential Processing** - Tasks run in a defined order rather than separate API calls
2. **State Management** - LangGraph manages the state between tasks
3. **Error Handling** - Better error handling and recovery
4. **Modularity** - Each task is a separate node that can be modified independently
5. **Scalability** - Easier to add new tasks or modify the workflow

## Customization

### Adding New Tasks

1. Add the task function to `nodes.py`
2. Add the corresponding prompt to `prompts.py`
3. Update the workflow in `agent.py`
4. Add the new field to `LegalCaseState` in `format.py`

### Modifying Prompts

Edit the prompts in `prompts.py` to change how the AI processes each task.

### Changing Models

Update the model configuration in `nodes.py`:

```python
model = ChatOpenAI(model="gpt-4", temperature=0)  # Change model here
```

## Troubleshooting

### Common Issues

1. **API Key Errors** - Ensure your `.env` file contains the correct OpenAI API key
2. **Import Errors** - Make sure all dependencies are installed
3. **CSV File Not Found** - Update the file path in `run_langgraph_workflow.py`

### Debug Mode

The workflow includes extensive logging. Check the console output for detailed information about each step.

## Performance

- **Sequential Processing** - Tasks run one after another (not parallel)
- **API Calls** - Each task makes one API call to OpenAI
- **Memory Usage** - State is maintained throughout the workflow
- **Error Recovery** - Failed cases are logged and can be reprocessed

## Future Enhancements

- **Parallel Processing** - Run independent tasks in parallel
- **Conditional Logic** - Add decision points based on case content
- **Human-in-the-Loop** - Add manual review steps
- **Batch Optimization** - Process multiple cases more efficiently 