#!/usr/bin/env python3
"""
Main script to run the LangGraph legal case classification workflow
This script replaces the functionality of summary_chunked_instructor.py with a LangGraph-based approach
"""

import os
import csv
import json
import sys
from pathlib import Path
from langgraph_files.agent import run_legal_case_workflow, run_batch_legal_cases

# Increase CSV field size limit to handle large text fields
csv.field_size_limit(2**31 - 1)  # Use a reasonable large value

def create_filename_to_id_mapping(mapping_csv_path: str) -> dict:
    """
    Create a mapping from filename to ID using the Pre-processed_all_decisions3937.csv file
    
    Args:
        mapping_csv_path: Path to the mapping CSV file
        
    Returns:
        dict: Mapping from filename to ID
    """
    filename_to_id = {}
    
    try:
        with open(mapping_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = row.get("file_name", "").strip()
                case_id = row.get("ID", "").strip()
                if filename and case_id:
                    filename_to_id[filename] = case_id
                    
        print(f"✅ Created filename to ID mapping with {len(filename_to_id)} entries")
        
    except FileNotFoundError:
        print(f"❌ Mapping CSV file not found: {mapping_csv_path}")
        return {}
    except Exception as e:
        print(f"❌ Error creating mapping: {str(e)}")
        return {}
    
    return filename_to_id

def load_csv_data(csv_file_path: str, filename_to_id_mapping: dict, limit: int = None) -> list:
    """
    Load case data from CSV file and map to proper IDs
    
    Args:
        csv_file_path: Path to the CSV file
        filename_to_id_mapping: Mapping from filename to ID
        limit: Maximum number of cases to process (for testing)
        
    Returns:
        list: List of dicts with 'decision_text' and 'decision_id' keys
    """
    cases = []
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if row.get("text") == "NA":
                    continue
                    
                # Get the filename from the current CSV
                filename = row.get("file_name", "").strip()
                
                # Get the real ID from the mapping
                decision_id = filename_to_id_mapping.get(filename, filename)
                decision_text = row["text"]
                
                cases.append({
                    "decision_text": decision_text,
                    "decision_id": decision_id,
                    "original_filename": filename  # Keep for reference
                })
                
                if limit and len(cases) >= limit:
                    break
                    
        print(f"✅ Loaded {len(cases)} cases from {csv_file_path}")
        
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_file_path}")
        return []
    except Exception as e:
        print(f"❌ Error loading CSV: {str(e)}")
        return []
    
    return cases

def save_results(results: list, output_dir: str = "langgraph_output"):
    """
    Save workflow results to files
    
    Args:
        results: List of LegalCaseState objects
        output_dir: Directory to save output files
    """
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Save individual JSON files
    json_dir = Path(output_dir) / "json_outputs"
    json_dir.mkdir(exist_ok=True)
    
    for result in results:
        if result.get("final_output"):
            # Use the decision_id for the filename (which should be the proper ID from the mapping)
            filename = f"{result['decision_id']}.json"
            filepath = json_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result['final_output'], f, indent=2, ensure_ascii=False)
    
    # Save summary CSV
    csv_file = Path(output_dir) / "summary_results.csv"
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            "ID", 
            "Summary of legal conflict",
            "Summary of plaintiff arguments", 
            "Summary of defendant arguments",
            "Summary of judge arguments"
        ]
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            if result.get("final_output"):
                writer.writerow({
                    "ID": result["decision_id"],
                    "Summary of legal conflict": result["final_output"].get("Summary of legal conflict", ""),
                    "Summary of plaintiff arguments": result["final_output"].get("Summary of plaintiff arguments", ""),
                    "Summary of defendant arguments": result["final_output"].get("Summary of defendant arguments", ""),
                    "Summary of judge arguments": result["final_output"].get("Summary of judge arguments", "")
                })
    
    print(f"✅ Results saved to {output_dir}/")
    print(f"  - JSON files: {json_dir}/")
    print(f"  - Summary CSV: {csv_file}")

def main():
    """Main function to run the legal case classification workflow"""
    print("🚀 LangGraph Legal Case Classification Workflow")
    print("=" * 60)
    
    # Configuration
    engo_csv_file = "Pre-processed_ENGO_con.csv"  # CSV with case text
    mapping_csv_file = "Pre-processed_all_decisions3937.csv"  # CSV with filename to ID mapping
    output_dir = "langgraph_output"
    case_limit = 3  # Set to None to process all cases, or set to a number to limit for testing
    
    # Check if required files exist
    if not os.path.exists(engo_csv_file):
        print(f"❌ ENGO CSV file not found: {engo_csv_file}")
        print("Please update the engo_csv_file path in the script or place the CSV file in the correct location.")
        return
        
    if not os.path.exists(mapping_csv_file):
        print(f"❌ Mapping CSV file not found: {mapping_csv_file}")
        print("Please update the mapping_csv_file path in the script or place the CSV file in the correct location.")
        return
    
    # Create filename to ID mapping
    print(f"📖 Creating filename to ID mapping from {mapping_csv_file}...")
    filename_to_id_mapping = create_filename_to_id_mapping(mapping_csv_file)
    
    if not filename_to_id_mapping:
        print("❌ Failed to create filename to ID mapping. Exiting.")
        return
    
    # Load case data with proper ID mapping
    print(f"📖 Loading cases from {engo_csv_file}...")
    cases = load_csv_data(engo_csv_file, filename_to_id_mapping, limit=case_limit)
    
    if not cases:
        print("❌ No cases loaded. Exiting.")
        return
    
    # Run the workflow
    print(f"\n🔄 Running LangGraph workflow for {len(cases)} cases...")
    results = run_batch_legal_cases(cases)
    
    # Save results
    print(f"\n💾 Saving results...")
    save_results(results, output_dir)
    
    # Summary
    print(f"\n🎉 Workflow completed!")
    print(f"📊 Processed {len(results)} cases")
    print(f"📁 Results saved to {output_dir}/")
    
    # Show some statistics
    successful_cases = sum(1 for r in results if r.get("final_output"))
    failed_cases = len(results) - successful_cases
    
    print(f"✅ Successful: {successful_cases}")
    if failed_cases > 0:
        print(f"❌ Failed: {failed_cases}")

if __name__ == "__main__":
    main() 