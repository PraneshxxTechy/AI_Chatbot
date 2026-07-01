from .llm import client

def generate_response(messages):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=1
    )

    assistant_response = completion.choices[0].message.content
    return assistant_response