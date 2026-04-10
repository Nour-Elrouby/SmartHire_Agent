from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent
import shutil
import os
import json

app = FastAPI(
    title="SmartHire AI Agent",
    description="AI-powered recruitment agent for SmartHire",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "SmartHire AI Agent is running",
        "version": "1.0.0",
        "endpoints": [
            "POST /score-resume",
            "POST /rank-candidates",
            "POST /chat"
        ]
    }

@app.post("/score-resume")
async def score_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    #Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    #Run agent
    result = run_agent(
        "score",
        file_path=temp_path,
        job_description=job_description
    )
    
    #Delete temp file
    os.remove(temp_path)
    
    return result

@app.post("/rank-candidates")
async def rank_candidates(
    candidates: str = Form(...),
    top_n: int = Form(5)
):
    candidates_list = json.loads(candidates)
    
    result = run_agent(
        "rank",
        candidates=candidates_list,
        top_n=top_n
    )
    
    return result

@app.post("/chat")
async def chat(
    job_description: str = Form(...),
    question: str = Form(...)
):
    result = run_agent(
        "chat",
        job_description=job_description,
        question=question
    )
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)