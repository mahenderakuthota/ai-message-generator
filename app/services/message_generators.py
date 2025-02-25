from abc import ABC, abstractmethod
from app.models.schemas import MessageRequest
from app.models.schemas import GeneratedMessage

class FlirtMessage:

    def __init__(self, message):
        self.message = message

class MessageGenerator(ABC):

    @abstractmethod
    def generate_message(self, message_request: MessageRequest) -> FlirtMessage:
        pass



