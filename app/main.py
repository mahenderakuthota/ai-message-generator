from fastapi import FastAPI, HTTPException
from openai.types.beta import VectorStoreListParams

from app.models.schemas import MessageRequest, GeneratedMessage
from app.services.ai_service import generate_message
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

from app.services.db.astra_vector_db_service import AstraVectorStoreService
from app.services.db.vector_store_service import VectorStoreService
from app.services.message_service import MessageService
from app.services.message_generators import MessageGenerator
from app.services.freetier_message_gen import FreeTierMessageGenerator
from app.services.rag_message_gen import RagMessageGenerator
from app.services.transformers.deepseek_transformer import DeepseekTransformer
from loguru import logger

app = FastAPI()

#message_service: MessageService = MessageService(FreeTierMessageGenerator(DeepseekTransformer()))
vector_store_service: VectorStoreService = AstraVectorStoreService()
message_service: MessageService = MessageService(RagMessageGenerator(vector_store_service, DeepseekTransformer()))
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


@app.get("/load")
async def load_data():
    print("load data")
    vector_store_service.load_data(
        "d:/personal projects/message-generator/ai-message-generator/app/data/flirt_messages.csv")


@app.post("/generate-message", response_model=GeneratedMessage)
async def create_message(message_data: MessageRequest):
    try:
        print("Generate Message in rest api")
        logger.info("message request ")
        return message_service.generate_message(message_data)

    except Exception as e:
        logger.error("Error while generating message", extra={"exception": e})
        raise HTTPException(
            status_code=500,
            detail=f"Message generation failed: {str(e)}"
        )
