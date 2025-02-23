from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chat_models import init_chat_model
from app.config import settings

load_dotenv()
model = init_chat_model("llama3-8b-8192", model_provider="groq")

def generate_message(prompt_data: dict) -> dict:

    print(prompt_data)
    print(prompt_data['hobbies'])

    system_prompt="""
    You are a charismatic AI that generates direct, shareable flirtatious messages. Craft SHORT, playful messages (1-2 sentences max) using ONLY these inputs:
    - Recipient's name
    - Specified tone
    - Contextual situation
    - Their interests/hobbies

    Rules:
    1. Never include explanations/reasoning - ONLY the final message
    2. Use 1-2 relevant emojis maximum
    3. Always end with a playful question
    4. Keep language contemporary and natural
    5. Avoid clichés/metaphors that require interpretation
    """
    prompt_template="""
    Generate a {tone} flirtatious message for {name} using this context: "{context}". Incorporate their interests in {interests} and hobby of {hobbies}. Message must be self-contained, direct, and immediately shareable.
    
    """


    chat_prompt = ChatPromptTemplate(
        [
            ('system',system_prompt),
            ('user',prompt_template)
        ]
    )

    message = model.invoke(chat_prompt.format(name=prompt_data["recp_name"],hobbies=prompt_data["hobbies"], context=prompt_data["context"],interests=prompt_data["interests"], tone=prompt_data["tone"] ))

    print(message)

    return {
        "message_content": message.content
    }
