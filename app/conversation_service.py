from datetime import datetime
from bson import ObjectId

from .database import conversations

SYSTEM_PROMPT = {
    "role": "system",
    "content": """
##Role
You are a helpful, knowledgeable, and friendly AI assistant.

##Instructions
- Answer user questions accurately and clearly.
- Explain concepts in a simple and structured manner.
- Ask clarifying questions when the user's request is ambiguous.
- Keep responses short and to the point.
- Expand only if the user asks for more details.
- If you don't know something, say so instead of making up information.
- Provide step-by-step guidance when appropriate.
- Adapt your response to the user's level of expertise.
- Use markdown formatting for better readability when useful.
- Be concise for simple questions and detailed for complex ones.
- Maintain a polite, professional, and conversational tone.
- When providing code:
  - Use best practices.
  - Include comments when they improve understanding.
  - Explain the code if needed.
- Prioritize helpfulness, correctness, and safety in every response.
"""
}


def create_conversation(title="New Chat"):

    conversation = {
        "title": title,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "messages": [SYSTEM_PROMPT]
    }

    result = conversations.insert_one(conversation)

    return str(result.inserted_id)


def get_conversation(conversation_id):
    """
    Returns the entire conversation document.
    """

    return conversations.find_one(
        {"_id": ObjectId(conversation_id)}
    )


def get_messages(conversation_id):
    """
    Returns all messages in the conversation.
    """

    conversation = get_conversation(conversation_id)

    if conversation:
        return conversation["messages"]

    return []


def add_message(conversation_id, role, content):

    conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$push": {
                "messages": {
                    "role": role,
                    "content": content
                }
            },
            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )


def update_title(conversation_id, title):
    """
    Updates the title of a conversation.
    """

    conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$set": {
                "title": title,
                "updated_at": datetime.utcnow()
            }
        }
    )


def list_conversations(limit=10):

    docs = conversations.find().sort(
        "updated_at",
        -1
    ).limit(limit)

    return [
        (
            doc["title"],
            str(doc["_id"])
        )
        for doc in docs
    ]

