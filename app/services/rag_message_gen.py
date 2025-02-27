from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from app.services.transformers.message_transformers import  MessageTransformer
from app.services.transformers.deepseek_transformer import  DeepseekTransformer

from app.models.schemas import MessageRequest
from app.services.db.vector_store_service import VectorStoreService
from app.services.message_generators import MessageGenerator, FlirtMessage
from langchain.chat_models import init_chat_model
from app.config import settings
import traceback


class RagMessageGenerator(MessageGenerator):
    system_prompt: str = """
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
    prompt_template: str = """
              Generate a {tone} flirtatious message for {name} for {context} based on provided sample messages:
              <sample_messages>
              {sample_messages}
              </sample_messages>
            """

    def __init__(self, vector_store_service: VectorStoreService, message_transformer: MessageTransformer):
        super().__init__()
        self.message_transformer = message_transformer
        self.vector_store = vector_store_service.get_vector_store()
        self.model = init_chat_model(settings.ai_model, model_provider=settings.ai_model_provider)

        self.chatPrompt: ChatPromptTemplate = ChatPromptTemplate([
            ('system', self.system_prompt),
            ('user', self.prompt_template)
            ]
        )

        print("RagMessageGenerator initialized")

    def generate_message(self, message_request: MessageRequest) -> FlirtMessage:
        try:
            print(message_request)
            print("Generating FlirtMessage")
            filter = {
                "$or": [
                    {"hobby": {"$eq": message_request.hobbies}},
                    {"tone": {"$eq": message_request.tone}}
                ]
            }
            docs: list = self.vector_store.similarity_search_with_score(message_request.context, 2, filter)
            print(f"no of docs got {len(docs)}")
            sample_messages: str = ",".join(doc[0].page_content for doc in docs)
            sample_messages = sample_messages.strip(',')
            print(f"sample messages: {sample_messages}")

            result = self.model.invoke(self.chatPrompt.format(name=message_request.recp_name,
                                                          tone=message_request.tone,
                                                          context=message_request.context,
                                                          sample_messages=sample_messages))

            message = self.message_transformer.transform_message(result.content)
            print(f"message generated {message}")
        except Exception as e:
            traceback.print_exc()
            message = f"Fallback: Hey {message_request.recp_name}, your x {message_request.hobbies} vibes are irresistible!"
        print(message)
        return FlirtMessage(message)
