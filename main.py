import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

# --- CONFIGURATION ---
API_KEY = "AIzaSyAUzeC1F2uGpE4-wP-DWQe0a4vRGMG1IxM"
client = genai.Client(api_key=API_KEY)
model_name = "gemini-2.5-flash"

# Keep your exact Regex pattern!
log_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ERROR (.*)"

# 1. Initialize the FastAPI application
app = FastAPI(title="AI Log Auditor API", version="1.0")

# 2. Define the expected incoming data payload
class LogRequest(BaseModel):
    server_name: str
    raw_log_line: str

# 3. Create the POST Endpoint
@app.post("/api/v1/audit-log")
async def audit_server_log(request: LogRequest):
    # Step A: Run your Regex on the incoming log line
    match = re.search(log_pattern, request.raw_log_line)
    
    if not match:
        raise HTTPException(status_code=400, detail="Invalid log format or no ERROR detected.")
        
    timestamp = match.group(1)
    message = match.group(2)
    
    # Step B: Pass the extracted error to the Google Gemini GenAI API
    try:
        if len(API_KEY) > 20:
            ai_prompt = f"Categorize this error. Then provide a 1-sentence explanation and 1 suggested remediation step to fix it: {message}"
            
            response = client.models.generate_content(
                model=model_name,
                contents=ai_prompt
            )
            ai_explanation = response.text
        else:
            ai_explanation = "AI Error: Valid API Key Required"
            
        # Step C: Return the structured JSON response
        return {
            "status": "Success",
            "server": request.server_name,
            "timestamp": timestamp,
            "extracted_error": message,
            "ai_analysis": ai_explanation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Service Failure: {str(e)}")