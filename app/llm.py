from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

llm_api = os.getenv("llm_api")

client = Groq(api_key=llm_api)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a short poem about the beauty of nature."}
]

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,
    temperature=1,
    max_completion_tokens=500,
    stream=True,
    stop=None
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
