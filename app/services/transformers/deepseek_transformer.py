from app.services.transformers.message_transformers import MessageTransformer
from app.services.message_generators import FlirtMessage
import re

class DeepseekTransformer(MessageTransformer):

    def transform_message(self, flirt_message:str) -> str:
        message =  re.sub(r'<think>.*?</think>', '', flirt_message, flags=re.DOTALL)
        message = message.lstrip('\n')
        message = message.lstrip('"')
        message = message.rstrip('"')
        return message
    

