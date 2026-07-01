import gradio as gr

from .chat_service import generate_response

from .conversation_service import (
    create_conversation,
    get_messages,
    add_message,
    list_conversations,
    get_conversation,
    update_title
)


def load_chat(conversation_id):
    """
    Load a conversation from MongoDB and convert it to
    Gradio Chatbot message format.
    """

    if not conversation_id:
        return []

    messages = get_messages(conversation_id)

    history = []

    for message in messages:

        if message["role"] == "system":
            continue

        history.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )

    return history


def select_conversation(conversation_id):
    """
    Called when user clicks a conversation in sidebar.
    """

    history = load_chat(conversation_id)

    return conversation_id, history


def new_chat():
    """
    Create a new conversation.
    """

    conversation_id = create_conversation()

    return (
        conversation_id,
        [],
        gr.update(
            choices=list_conversations(),
            value=conversation_id
        )
    )


def chat(message, history, conversation_id):

    if not message.strip():
        return (
            "",
            history,
            conversation_id,
            gr.update()
        )

    if conversation_id is None:
        conversation_id = create_conversation()

    add_message(
        conversation_id,
        "user",
        message
    )

    conversation = get_conversation(conversation_id)

    if conversation["title"] == "New Chat":

        title = generate_title(message)

        update_title(
            conversation_id,
            title
        )

    messages = get_messages(conversation_id)

    response = generate_response(messages)

    add_message(
        conversation_id,
        "assistant",
        response
    )

    history = load_chat(conversation_id)

    return (
        "",
        history,
        conversation_id,
        gr.update(
            choices=list_conversations(),
            value=conversation_id
        )
    )


def generate_title(first_message):

    messages = [
        {
            "role": "system",
            "content": (
                "Generate a concise conversation title in at most 5 words. "
                "Return only the title."
            )
        },
        {
            "role": "user",
            "content": first_message
        }
    ]

    return generate_response(messages).strip()



with gr.Blocks(title="AI Chatbot") as demo:

    conversation_state = gr.State(None)

    gr.Markdown("# 🤖 AI Chatbot")

    with gr.Row():

        with gr.Column(scale=2):

            new_button = gr.Button(
                "➕ New Chat",
                variant="primary"
            )

            conversations = gr.Radio(
                label="Conversations",
                choices=list_conversations(),
                value=conversation_state.value
            )


        with gr.Column(scale=8):

            chatbot = gr.Chatbot(
                type="messages",
                height=600
            )

            with gr.Row():

                message = gr.Textbox(
                    placeholder="Type your message...",
                    scale=8,
                    show_label=False
                )

                send = gr.Button(
                    "Send",
                    scale=1,
                    variant="primary"
                )


    send.click(
        fn=chat,
        inputs=[
            message,
            chatbot,
            conversation_state
        ],
        outputs=[
            message,
            chatbot,
            conversation_state,
            conversations
        ]
    )

    message.submit(
        fn=chat,
        inputs=[
            message,
            chatbot,
            conversation_state
        ],
        outputs=[
            message,
            chatbot,
            conversation_state,
            conversations
        ]
    )

    new_button.click(
        fn=new_chat,
        outputs=[
            conversation_state,
            chatbot,
            conversations
        ]
    )

    conversations.change(
        fn=select_conversation,
        inputs=conversations,
        outputs=[
            conversation_state,
            chatbot
        ]
    )


if __name__ == "__main__":
    demo.launch()