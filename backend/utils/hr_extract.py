from fastapi import FastAPI, HTTPException, UploadFile, File, Query
import regex as re
import json
from . import text_extract
from ..config import config

#function for extracting skills from hr job description
def extract_hr_skills(file:UploadFile):
    system_prompt=("""you are a required skills extractor machine from job description from college students resume
                  Extract the required skills from the given job description which are according for college student. 
            Provide the skills as a list of words or short phrases in JSON format as follows -
                   "{\"required_skills\": [\"skill1\", \"skill2\", \"skill3\"]}. "
                   """)
    extracted_text=text_extract.extract_pdf_text(file)
    response=config.client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":extracted_text}
        ],
        temperature=0.7,
        max_tokens=300
    )
    llm_output=response.choices[0].message.content.strip("```json\n")
    reponse=clean_hr_skills_response(llm_output)
    return reponse

#function for cleaning the llm response 
def clean_hr_skills_response(llm_output: str) -> dict:
    try:
        # Extract JSON content 
        json_match = re.search(r"\{.*\}", llm_output, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response.")
        
        json_text = json_match.group()

        # Removing trailing commas inside JSON objects/arrays
        json_text = re.sub(r",\s*([\]}])", r"\1", json_text)
        
        data = json.loads(json_text)

        # Ensure extracted skills are formatted correctly
        cleaned_data = {
            "required_skills": list(set(data.get("required_skills", []))) if isinstance(data.get("required_skills"), list) else []
        }

        return cleaned_data

    except (json.JSONDecodeError, ValueError) as e:
        return {
            "error": f"Failed to parse JSON: {str(e)}",
            "raw_response": llm_output  
        }

