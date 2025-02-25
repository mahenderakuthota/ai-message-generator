from pydantic import BaseModel

class MessageRequest(BaseModel):
    tone: str
    context: str
    interests: str | None = None
    hobbies: str | None = None
    recp_name: str

class GeneratedMessage(BaseModel):
    message_content: str
