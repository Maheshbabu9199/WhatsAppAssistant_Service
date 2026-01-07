from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    profilename: str = Field(..., description="Profile name of the user")
    message: str = Field(..., description="Message content")
    message_type: str = Field(
        ..., description="Type of the message"
    )  # e.g., text, image, video
    sender_id: str = Field(..., description="Unique identifier for the sender")
    message_id: str = Field(..., description="Unique identifier for the message")
