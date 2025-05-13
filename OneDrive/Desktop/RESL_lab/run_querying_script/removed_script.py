    # ### SIMPLIFIED QUERYING SCRIPT TO CHECK WHETHER QUERY GOES THROUGH ###
    # try:
    #     response = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=[{"role": "user", "content": prompt}],
    #         temperature=0.0
    #           )  # Use 0 temperature for more consistent results
    #     return json.loads(response.choices[0].message.content)

    # except json.JSONDecodeError:
    #     logging.error("Invalid JSON response from OpenAI.")
    #     with open("output/failure_output.txt", "w") as file:
    #         print(str(response), file=file)
    #     return {"code": "Error: invalid JSON", "quoted_evidence": "", "opposition_or_support": ""}

    # except Exception as e:
    #     error_msg = str(e)[:100] + "..."
    #     return {"code": f"Unexpected error: {error_msg}", "quoted_evidence": "", "opposition_or_support": ""} 
