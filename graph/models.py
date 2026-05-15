import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# environment variables
load_dotenv()

# initialize of model
llm = init_chat_model("groq:llama-3.1-8b-instant")