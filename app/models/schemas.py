from pydantic import BaseModel

class MessageRequest(BaseModel):
    tone: str
    context: str
    interesets: str
    hobbies: str
    recp_name: str

class GeneratedMessage(BaseModel):
    message_content: str