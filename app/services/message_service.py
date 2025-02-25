from app.models.schemas import MessageRequest, GeneratedMessage
from app.services.message_generators import MessageGenerator, FlirtMessage

class MessageService:

    def __init__(self, message_generator: MessageGenerator):
        self.message_generator = message_generator
    

    def generate_message(self, message_request: MessageRequest) -> GeneratedMessage:
       flirt_message: FlirtMessage = self.message_generator.generate_message(message_request)
       return GeneratedMessage(message_content=flirt_message.message)
