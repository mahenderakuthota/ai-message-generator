from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chat_models import init_chat_model
from app.config import settings
from app.models.schemas import MessageRequest

load_dotenv()
model = init_chat_model(settings.ai_model, model_provider=settings.ai_model_provider)

def generate_message(prompt_data: MessageRequest) -> dict:

    print(prompt_data)
    if prompt_data.hobbies is None:
        prompt_data.hobbies = ''
    if prompt_data.interests is None:
        prompt_data.interests = ''

    system_prompt="""
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
    prompt_template="""
    Generate a {tone} flirtatious message for {name} using :  
    - Context: "{context}"  
    - Interests: {interests}  
    - Hobby: {hobbies}
    if provided
    """


    chat_prompt = ChatPromptTemplate(
        [
            ('system',system_prompt),
            ('user',prompt_template)
        ]
    )

    message = model.invoke(chat_prompt.format(name=prompt_data.recp_name,hobbies=prompt_data.hobbies, context=prompt_data.context,interests=prompt_data.interests, tone=prompt_data.tone ))

    print(message)

    return {
        "message_content": message.content
    }
