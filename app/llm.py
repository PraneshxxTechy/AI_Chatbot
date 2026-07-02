from groq import Groq
from dotenv import load_dotenv
import os
import openai

from langfuse.openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)