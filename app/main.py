from fastapi import FastAPI, HTTPException
from app.models.schemas import MessageRequest, GeneratedMessage
from app.services.ai_service import generate_message
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate-message", response_model=GeneratedMessage)
async def create_message(request: MessageRequest):
    try:
        prompt_data = {
            "tone": request.tone,
            "context": request.context,
            "interests": request.interests,
            "hobbies": request.hobbies,
            "recp_name": request.recp_name
        }
        
        result = generate_message(prompt_data)
        return GeneratedMessage(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Message generation failed: {str(e)}"
        )

