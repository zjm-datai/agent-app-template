


import re
from typing import List, Literal
from pydantic import BaseModel, Field, field_validator


class Message(BaseModel):
    """Message model for chat endpoint.
    
    Attributes:
        role: The role of the message sender (user or assistant).
        content: The content of message.
    """

    # 会忽略额外添加的字段，但是不会将字段加入实例中
    # 此外还有属性为 forbid allow 
    # allow 会将字段加入实例中
    model_config = {
        "extra": "ignore"    
    }

    role: Literal["user", "assistant", "system"] = Field(
        ..., description="The role of the message sender"
    )
    content: str = Field(
        ..., description="The content of the message", min_length=1, max_length=3000    
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, content: str) -> str:
        """Validate the message content."""

        # Check for potentially handful content
        if re.search(r"<script.*?>.*?</script>", content, re.IGNORECASE | re.DOTALL):
            raise ValueError("Content contains potentially harmful scripts tags.")
        
        # Check for null bytes
        if "\0" in content:
            raise ValueError("Content contains null bytes.")
        
        return content

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    messages: List[Message] = Field(
        ...,
        description="List of messages in the conversation",
        min_length=1       
    )

class ChatResponse(BaseModel):
    """Response model for chat endpoint.

    Attributes:
        messages: List of messages in the conversation.
    """

    messages: List[Message] = Field(..., description="List of messages in the conversation")


class StreamResponse(BaseModel):
    """Response model for streaming chat endpoint.

    Attributes:
        content: The content of the current chunk.
        done: Whether the stream is complete.
    """

    content: str = Field(default="", description="The content of the current chunk")
    done: bool = Field(default=False, description="Whether the stream is complete")