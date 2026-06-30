from .llm import client
from .chat_service import generate_response
from .conversation_history import ConversationHistory


if __name__ == "__main__":
    conversation_history = ConversationHistory()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        conversation_history.add_user_message(user_input)
        response = generate_response(conversation_history.get_messages())
        conversation_history.add_assistant_message(response)
        print(f"Assistant: {response}")
