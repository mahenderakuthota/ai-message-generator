from app.services.message_generators import MessageGenerator, FlirtMessage
from app.models.schemas import MessageRequest, GeneratedMessage
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chat_models import init_chat_model
from app.config import settings
from app.services.transformers.message_transformers import MessageTransformer

class FreeTierMessageGenerator(MessageGenerator):
    

    def __init__(self, message_transformer: MessageTransformer):
        super().__init__()
        self.system_prompt:str = """
        You are a charismatic AI that generates direct, shareable flirtatious messages. Craft SHORT, playful messages (1-2 sentences max) using ONLY these inputs:
    - Recipient's name
    - Specified tone
    - Contextual situation
    - Their interests/hobbies

    Rules:
    1. Never include explanations/reasoning/note or anything else ONLY the final message
    2. Use 1-2 relevant emojis maximum
    3. Always end with a playful question
    4. Keep language contemporary and natural
    5. Avoid clichés/metaphors that require interpretation
        """
        self.prompt_template:str = """
          Generate a {tone} flirtatious message for {name} using :  
    - Context: "{context}"  
    - Interests: {interests}  
    - Hobby: {hobbies}
    if provided
        """
        self.message_transformer=message_transformer
        self.model=None
        self.chat_prompt=None
        self.initialize_ai_model()
    
 


    def initialize_ai_model(self):
        load_dotenv()
        self.model = init_chat_model(settings.ai_model, model_provider=settings.ai_model_provider)
        self.chat_prompt = ChatPromptTemplate(
        [
            ('system',self.system_prompt),
            ('user',self.prompt_template)
        ]
         )


    def generate_message(self, message_request: MessageRequest) -> FlirtMessage:
        message = self.model.invoke(self.chat_prompt.format(name=message_request.recp_name,hobbies=message_request.hobbies, 
                                                            context=message_request.context,interests=message_request.interests, 
                                                            tone=message_request.tone ))
        if self.message_transformer:
            message_content = self.message_transformer.transform_message(message.content)
        else:
            message_content = message.content

        return FlirtMessage(message_content)
