from fastapi import FastAPI, HTTPException
from app.models.schemas import MessageRequest, GeneratedMessage
from app.services.ai_service import generate_message
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.services.message_service import MessageService
from app.services.message_generators import MessageGenerator
from app.services.freetier_message_gen import FreeTierMessageGenerator
from app.services.transformers.deepseek_transformer import DeepseekTransformer


app = FastAPI()

message_service: MessageService = MessageService( FreeTierMessageGenerator(DeepseekTransformer()))

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
async def create_message(message_data: MessageRequest):
    try:
        return message_service.generate_message(message_data)
        
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, 
            detail=f"Message generation failed: {str(e)}"
        )

