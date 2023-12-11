from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    """
    An enumeration representing the different roles a user can have in a conversation.
    """
    system = 'system'
    user = 'user'
    assistant = 'assistant'

class Message(BaseModel):
    """
    Represents a message in a conversation.

    Attributes:
        role (Role): The role of the sender of the message.
        content (str): The content of the message.
    """
    role: Role
    content: str

class Request(BaseModel):
    """
    Represents a request to the chat API.

    Attributes:
        api_key (str): The API key used for authentication.
        prompt (str): The prompt for the chat session.
        history (list[Message]): The list of previous messages in the conversation.
        service (str): Service field.
    """
    api_key: str
    prompt: str
    history: list[Message]
    service: str | None = None

class Response(BaseModel):
    """
    Represents a response from the chat API.

    Attributes:
        answer (str): The answer generated by the API.
    """
    answer: str

class Error(BaseModel):
    """
    Represents an error response from the chat API.
    
    Attributes:
        error (str): The error message.
    """
    error: str
