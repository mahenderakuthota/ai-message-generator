from fastapi import FastAPI, HTTPException
from app.models.schemas import MessageRequest, GeneratedMessage
from app.services.ai_service import generate_message
from app.config import settings

app = FastAPI()

@app.post("/generate-message", response_model=GeneratedMessage)
async def create_message(request: MessageRequest):
    try:
        prompt_data = {
            "tone": request.tone,
            "context": request.context,
            "interests": request.interesets,
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

