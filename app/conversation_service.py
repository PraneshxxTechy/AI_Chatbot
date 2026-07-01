from datetime import datetime
from bson import ObjectId

from .database import conversations

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful assistant."
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

