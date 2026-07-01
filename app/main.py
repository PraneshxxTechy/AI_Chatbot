import gradio as gr

from .chat_service import generate_response
from .conversation_history import ConversationHistory

def chat(message, history):
    history = history or []
    conversation_history = ConversationHistory()
    messages = conversation_history.get_messages()

    for msg in history:
        if msg["role"] == "user":
            conversation_history.add_user_message(msg["content"])
        elif msg["role"] == "assistant":
            conversation_history.add_assistant_message(msg["content"])

    conversation_history.add_user_message(message)
    response = generate_response(conversation_history.get_messages())
    conversation_history.add_assistant_message(response)
    return response


if __name__ == "__main__":
    gr.ChatInterface(
        fn=chat,
        title="🤖 AI Chatbot",
        description="Powered by Groq",
    ).launch()
