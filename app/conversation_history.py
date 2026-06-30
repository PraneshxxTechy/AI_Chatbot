class ConversationHistory:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    def add_user_message(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

    def add_assistant_message(self, assistant_response):
        self.messages.append({"role": "assistant", "content": assistant_response})

    def get_messages(self):
        return self.messages