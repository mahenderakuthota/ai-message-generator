from abc import abstractmethod
from app.services.message_generators import FlirtMessage


class MessageTransformer:
    
    @abstractmethod
    def transform_message(message: str) -> str:
        pass