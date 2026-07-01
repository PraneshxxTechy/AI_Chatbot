from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

llm_api = os.getenv("llm_api")

client = Groq(api_key=llm_api)