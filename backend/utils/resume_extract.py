from fastapi import UploadFile, File
from . import text_extract
from backend.config import config
import regex as re
import json


#function for extracting entities from resume
def generate_response(file: UploadFile):
    system_prompt=("You are a resume entities extraction machine"
                    "Extract name, college name, 10th percentage, 12th percentage, CGPA, and skills from this resume text. "
            "Provide the output strictly in JSON format as follows: "
            "{\"name\": \"name\",\"college name\": \"name of the college\", \"10th percentage\": \"percentage\", \"12th or diploma percentage\": \"percentage\", \"CGPA\": \"value\", \"skills\": [\"skill1\", \"skill2\", \"skill3\"]}. "
            "For skills, include both explicitly mentioned skills and inferred skills based on projects and internships in the resume. "
            "In the resume either 12th percentage is present or diploma percentage will be present , extract one of the percentage present. Don't confuse diploma percentage with 10th percentage"
            "for 12th percentage in resume , 12th may also be written as HSC so extract the percentage of hsc if 12th not written . Don't write the '%' symbol "
            "for 10th percentage in resume , 10th may also be written as SSC so extract the percentage of ssc if 10th not written . Don't write the '%' symbol"
            "Ensure valid JSON output and do not include duplicates or additional information. If the specified detail is not present, write it as null or an empty list."
    )
    extracted_text = text_extract.extract_pdf_text(file)
    response = config.client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": extracted_text}
        ],
        temperature=0.7,
        max_tokens=300
    )
    
    llm_output = response.choices[0].message.content.strip("```json\n")  
    response=clean_llm_response(llm_output)
    return response  

#function for cleaning the llm response
def clean_llm_response(llm_output: str) -> dict:
    try:
        # Extract JSON content 
        json_match = re.search(r"\{.*\}", llm_output, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response.")
        
        json_text = json_match.group()

        # Removing trailing commas
        json_text = re.sub(r",\s*([\]}])", r"\1", json_text)

        # Parse JSON
        data = json.loads(json_text)

        default_response = {
            "name": None,
            "college name": None,
            "10th percentage": None,
            "12th or diploma percentage": None,
            "CGPA": None,
            "skills": []
        }

        # Ensure keys exist and sanitize values
        cleaned_data = {}
        for key in default_response:
            value = data.get(key)

            if key == "skills":
                cleaned_data[key] = list(set(value)) if isinstance(value, list) else []
            else:
                cleaned_data[key] = str(value).strip() if value else None

        return cleaned_data

    except (json.JSONDecodeError, ValueError) as e:
        return {
            "error": f"Failed to parse JSON: {str(e)}",
            "raw_response": llm_output  
        }
