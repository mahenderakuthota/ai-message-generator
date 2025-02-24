from pydantic import BaseModel

class MessageRequest(BaseModel):
    tone: str
    context: str
    interests: str
    hobbies: str
    recp_name: str

class GeneratedMessage(BaseModel):
    message_content: str