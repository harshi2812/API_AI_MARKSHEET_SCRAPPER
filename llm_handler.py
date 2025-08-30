import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

import schemas

# --- Configuration ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_structured_data_from_llm(text: str) -> dict:
    """
    Extracts structured data including confidence scores in a single API call.
    """
    schema_for_prompt = schemas.MarksheetData.model_json_schema()
    
    prompt = f"""
    Analyze the raw OCR text from a marksheet and extract the information into a JSON object that strictly adheres to the following JSON schema.

    For each field, you must provide both the extracted 'value' and a 'confidence' score from 0.0 to 1.0, representing how certain you are about the accuracy of the value based on the source text.

    If a field's value is not found in the text, the entire field object should be null.

    JSON Schema:
    {json.dumps(schema_for_prompt, indent=2)}

    Raw OCR Text:
    ---
    {text}
    ---
    
    Provide ONLY the valid JSON object as your response.
    """
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        
        # Clean up potential markdown formatting from the response
        json_string = response.text.strip().replace("```json", "").replace("```", "")
        
        data = json.loads(json_string)
        return data
        
    except Exception as e:
        # Return a structured error if the LLM call fails
        return {"error": f"LLM data extraction failed: {e}"}
