import gradio as gr

from .chat_service import generate_response
from .conversation_history import ConversationHistory

def chat(message, history):
    conversation =  ConversationHistory()

    for user_msg, assistant_msg in history:
            conversation.add_user_message(user_msg)
            conversation.add_assistant_message(assistant_msg)

    conversation.add_user_message(message)
    response = generate_response(conversation.get_messages())
    conversation.add_assistant_message(response)
    print(f"Conversation messages: {conversation.get_messages()}")
    return response


if __name__ == "__main__":
    gr.ChatInterface(
        fn=chat,
        title="🤖 AI Chatbot",
        description="Powered by Groq",
    ).launch()
